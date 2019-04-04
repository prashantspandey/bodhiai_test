from django.shortcuts import render
from django.core.urlresolvers import reverse
from .models import Questions,Choices,KlassTest
from basicinformation.models import *
from basicinformation.marksprediction import *
import datetime
import os.path
from .forms import *
from django.utils import timezone
from django.http import Http404, HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User,Group
import re
import pickle
import random
import urllib.request
from more_itertools import unique_everseen 
from random import randint
from decimal import *
import sys
from basicinformation.tasks import *
from celery.result import AsyncResult
from django.core.mail import send_mail


# Create your views here.
def create_test_Initial(request):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name= 'Teachers').exists():
            me = Teach(user)
            quest_file_name = 'question_paper'+str(user.teacher)+'.pkl'
            all_klasses = me.my_classes_names_cache()
            context = {'klasses':all_klasses}
            return render(request,'questions/createTest.html',context)

def create_test(request):
    user = request.user
    quest_file_name = 'question_paper'+str(user.teacher)+'.pkl'
    me = Teach(user)
    if 'klass_test' in request.GET:
        try:
            if os.path.exists(quest_file_name):
                os.remove(quest_file_name)
        except:
            pass

        ttt = request.GET['klass_test']
        quest = SSCquestions.objects.filter(school=
                                            me.profile.school)
        if len(quest)!=0:
            unique_chapters = me.my_subjects_names()
            
            test_type = 'SSC'
            return render(request, 'questions/klass_available.html',
                      {'fin':
                       unique_chapters,'which_klass':ttt,'test_type':test_type})
        else:
            noTest = 'Not Questions for this class'
            context = {'noTest':noTest}
            return
        render(request,'questions/klass_available.html',context)
    if 'category_test' in request.GET:
        category_klass = request.GET['category_test']
        split_category = category_klass.split(',')[0]
        split_klass = category_klass.split(',')[1]
        quest = SSCquestions.objects.filter(section_category =
                                            split_category,school
                                            =me.profile.school)
        print('{} number of questiosn in subject'.format(len(quest)))
        all_categories = []
        for i in quest:
            all_categories.append(i.topic_category)
        all_categories = list(unique_everseen(all_categories))
        print('{} all categories'.format(all_categories))
        #all_categories = me.return_TopicNames(split_category)
        all_categories = \
        me.change_topicNumbersNames(all_categories,split_category)
        print('{} all categories'.format(all_categories))
        all_categories.sort()
        print('%s all_categories' %all_categories)
        context = \
                {'categories':all_categories,'which_klass':split_klass,'section_category':split_category}
        return \
        render(request,'questions/klass_categories.html',context)
        

    if 'chapter_test' in request.GET:
        quest_file_name = 'question_paper'+str(user.teacher)+'.pkl'
        which_chap = request.GET['chapter_test']
        splitChap = which_chap.split(",")[0]
        splitClass = which_chap.split(",")[1]
        splitSection = which_chap.split(",")[2]
        if os.path.exists(quest_file_name):
            with open(quest_file_name,'rb') as fi:
                questions_list = pickle.load(fi)
            idlist = []
            for qq in questions_list:
                idlist.append(qq.id)

            klass_question = \
            SSCquestions.objects.filter(topic_category = splitChap,school =
                                            me.profile.school,section_category=splitSection)
            context = \
            {'que':klass_question,'idlist':idlist,'which_class':splitClass }
            return render(request,'questions/klass_questions.html',context)
        else:
            klass_question =\
            SSCquestions.objects.filter(topic_category =
                                        splitChap,school =
                                        me.profile.school,section_category=splitSection)
            context = \
            {'que':klass_question,'which_class':splitClass }
            return render(request,'questions/klass_questions.html',context)


def add_questions(request):
    user = request.user
    me = Teach(user)
    quest_file_name = 'question_paper'+str(user.teacher)+'.pkl'
    if 'question_id' in request.GET:
        if os.path.exists(quest_file_name):
            with open(quest_file_name,'rb') as lql:
                questions_list = pickle.load(lql)
        else:
            questions_list = []
        question_id = request.GET['question_id']
        which_klass = question_id.split(',')[1]
        question_id = question_id.split(',')[0]
        questions_list.append(SSCquestions.objects.get(id=question_id))
        questions_list = list(unique_everseen(questions_list))
        with open(quest_file_name,'wb') as ql:
            pickle.dump(questions_list,ql)
        total_marks = []
        for l in questions_list:
            total_marks.append(l.max_marks)
        total = 0
        for k in total_marks:
            total = total + k
        num_questions = len(total_marks)
        context = \
                {'questions':questions_list,'total_marks':total,'num_questions':num_questions,'which_klass':which_klass }
        return render(request,'questions/addedQuestions.html',context)
    if 'remove_id' in request.GET:
        if os.path.exists(quest_file_name):
            with open(quest_file_name,'rb') as rid:
                questions_list = pickle.load(rid)
        else:
            questions_list = []
        questions = []
        rem_id = request.GET['remove_id']
        which_klass = rem_id.split(',')[1]
        rem_id  = rem_id.split(',')[0]
        if rem_id == None:
            return HttpResponse('No questions in question paper')
        for tbr in questions_list:
            if not int(tbr.id) == int(rem_id):
                questions.append(tbr)
        total_marks = []
        questions_list = questions
        with open(quest_file_name,'wb') as ql:
            pickle.dump(questions_list,ql)
        for j in questions_list:
            total_marks.append(j.max_marks)
        total = 0
        for k in total_marks:
            total = total + k
        num_questions = len(total_marks)
        context = \
        {'questions':questions,'total_marks':total,'num_questions':num_questions
         }
        return render(request,'questions/addedQuestions.html',context)
    if request.POST:
        if os.path.exists(quest_file_name):
            with open(str(quest_file_name),'rb') as ql:
                questions_list= pickle.load(ql)

            which_klass = request.POST['which_klass']
            if len(questions_list)!=0:
                klass = me.my_classes_objects(which_klass)
                tot = 0 
                for i in questions_list:
                    tot = tot + i.max_marks
                newClassTest = SSCKlassTest()
                newClassTest.max_marks = tot
                newClassTest.published = timezone.now()
                newClassTest.name = str(me.profile) + str(timezone.now())
                newClassTest.klas = klass
                newClassTest.creator = user
                newClassTest.save()
                for zz in questions_list:
                    zz.ktest.add(newClassTest)
                teacher_type = "SSC"

            context = {'test':newClassTest,'teacher_type':teacher_type}
            return render(request,'questions/publish_test.html',context)
        else:
            return HttpResponse('Please select at-least one question')


def publish_test(request):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name= 'Teachers').exists():
            if 'publishTest' in request.POST:
                testid = request.POST['testid']
                date = request.POST['dueDate']
                time = request.POST['timePicker']
                publish_test =\
                publish_NormalTest.delay(user.id,testid,date,time)
                return \
            render(request,'questions/teacher_successfully_published.html')
            if 'pdfTest' in request.POST:
                me = Teach(user)
                testid = request.POST['testid']
                if me.institution == 'School':
                    teacher_type = 'School'
                    myTest = KlassTest.objects.get(id = testid)
                    for sub in myTest.questions_set.all():
                        subject = sub.sub
                        break
                    myTest.sub = subject
                elif me.institution == 'SSC':
                    teacher_type = 'SSC'
                    myTest = SSCKlassTest.objects.get(id = testid)
                    subs = []
                    for sub in myTest.sscquestions_set.all():
                        timesus = TimesUsed.objects.filter(teacher =
                                                          me.profile,quest =
                                                          sub)
                        if len(timesus) == 1:
                            for i in timesus:
                                i.numUsed = i.numUsed + 1
                                i.save()
                        else:
                            tused = TimesUsed()
                            tused.numUsed = 1
                            tused.teacher = me.profile
                            tused.quest = sub
                            tused.save()

                        subs.append(sub.section_category)
                    subs = list(unique_everseen(subs))
                    if len(subs)==1:
                        myTest.sub = subs[0]
                    elif me.profile.school.name == "JITO":
                        if '10' in str(subs[0]): 
                            myTest.sub = "IITJEE10-MultipleSubjects"
                        if '11' in str(subs[0]): 
                            myTest.sub = "IITJEE11-MultipleSubjects"
                        if '12' in str(subs[0]): 
                            myTest.sub = "IITJEE12-MultipleSubjects"

                    else:
                        myTest.sub = 'SSCMultipleSections'

                myTest.mode = 'BodhiSchool'
                myTest.save()
                context = {'test':myTest,'teacher_type':teacher_type}
                return\
            render(request,'questions/teacher_school_createdTest.html',context)
                #pdf =\
                #render_to_pdf('questions/teacher_school_createdTest.html',context)
                #return HttpResponse(pdf,content_type= 'application/pdf')

# create a one click test
def create_oneclick_test(request):
    user = request.user
    if user.is_authenticated:
        me = Teach(user)
        if user.groups.filter(name= 'Teachers').exists():
            testholder = TemporaryOneClickTestHolder.objects.filter(teacher= me.profile)
            if testholder:
                testholder.delete()
            #num_quests = [10,25,30,35,40,45,50]
            my_batches = me.my_classes_names_cache()
            context = {'myBatches':my_batches}
            return render(request,'questions/oneclick_test1.html',context)
def oneclick_test(request):
    user = request.user
    me = Teach(user)
    if user.is_authenticated:
        if 'oneclickbatches' in request.GET:
            testholder = TemporaryOneClickTestHolder.objects.filter(teacher= me.profile)
            if testholder:
                testholder.delete()
            clickBatch = request.GET['oneclickbatches']
            print('%s first one click ' %clickBatch)
            my_subs = me.my_subjects_names()
            context = {'subjects': my_subs,'oneClickBatch':clickBatch}
            return render(request,'questions/oneclick_test2.html',context)
        if 'questionsubjects' in request.GET:
            subandbatch = request.GET['questionsubjects']
            print('%s second one click ' %subandbatch)
            sub = subandbatch.split(',')[0]
            batch = subandbatch.split(',')[1]
            school = me.my_school()
            all_topics = []
            sub_topics = SSCquestions.objects.filter(section_category =
                                                     sub,school = school)
            for i in sub_topics:
                all_topics.append(i.topic_category)
            all_topics = list(unique_everseen(all_topics))
            topics = me.change_topicNumbersNames(all_topics,sub)
            topics = np.array(topics)
            print(topics)

            context = {'topics':topics,'subject':sub,'oneclickbatch':batch}
            return render(request,'questions/oneclick_test3.html',context)
        if 'oneclicktopicsnum' in request.GET:
            topicnumber = request.GET.getlist('oneclicktopicsnum');
            print('%s third one click ' %topicnumber)
            print(type(topicnumber))
            tnum = str(topicnumber).split('and')[0]
            tnum = tnum.replace('[','')
            tnum = tnum.replace('\'','')
            tnum_list = tnum.split(',')
            tname  = str(topicnumber).split('and')[1]
            tname_list = tname.split(',')

            subject = str(topicnumber).split('and')[2]
            batch = str(topicnumber).split('and')[3]
            batch = batch.replace(']','')
            batch = batch.replace('\'','')

            topics_total = list(zip(tnum_list,tname_list))
            topics_total = np.array(topics_total)

            final_num = []
            final_name = []
            for num,cat in topics_total:
                if int(num) != 0:
                    final_num.append(int(num))
                    final_name.append(cat)
            final_topic = list(zip(final_num,final_name))
            if len(final_topic)==0:
                return HttpResponse('Please fill in the number of questions from a\
                              topic')

            # creation of one click paper
            
            # class object to find out how many times has the teacher used a
            # question for that certain class
            kl = klass.objects.get(school = me.my_school(),name= batch)
            test_quest = []  # the question containing list

            for num,cat in final_topic:
                questions = SSCquestions.objects.filter(topic_category =
                                                        cat,section_category =
                                                        subject,school=me.my_school())
                cat_quest = []
                used_quests = [] # used question containing list
                for count,quest in enumerate(questions):
                    # get the number of times used object associated with the
                    # question

                    t_used=\
                    TimesUsed.objects.filter(teacher=me.profile,quest=quest,batch=kl)

                    #if quest has not been used in the batch before then add that
                    #question

                    if len(t_used) == 0 and count < num:
                        cat_quest.append(quest)
                    # otherwise add used questions to the used_quest list
                    if len(t_used) != 0:
                        used_quests.append(quest)
                # check if there are not enough new(unused) questions 
                if len(cat_quest) < num:
                    try:
                        # if yes then add already used questions to list until
                        # list is equal to number of required questions
                        for count,q in enumerate(used_quests):
                            if count < len(cat_quest):
                                cat_quest.append(q)
                    except Exception as e:
                        print(str(e))
                # finally add all questions to final questions list
                test_quest.extend(cat_quest)
            # setting up the test
            test = SSCKlassTest()
            test.name=str('oneclick')+str(me.profile)+str(batch)+str(timezone.now())
            test.mode = 'BodhiOnline'
            marks = 0
            for qu in test_quest:
                marks += qu.max_marks
            test.max_marks = marks
            test.course = 'SSC'
            test.creator = user
            test.sub = subject
            kl = klass.objects.get(school = me.my_school(),name= batch)
            test.klas = kl
            totalTime = len(test_quest)*0.6 # one question requires 36 secs

            test.totalTime = totalTime
            test.save()
            # add questions to testpaper
            for q in test_quest:
                try:
                    # modify times used object associated with each question as
                    # they are added to the test paper
                    times_used = TimesUsed.objects.get(batch =
                                                   kl,quest=q,teacher=me.profile)
                    times_used.numUsed += 1
                    times_used.save()
                except:
                    # if new question then create the TimesUsed object for that
                    # question
                    times_used = TimesUsed()
                    times_used.batch = kl
                    times_used.numUsed =1
                    times_used.quest = q
                    times_used.teacher = me.profile
                    times_used.save()
                
                # add many to many field of question to specific test
                q.ktest.add(test)

            # getting all the students in a specific class to be given the test
            # to
            students = Student.objects.filter(klass = kl,school =
                                              me.my_school())
            # add testtakers(students of a specific batch) to test paper
            for st in students:
                # looks for common subject between student and teacher
                subs = Subject.objects.filter(student=st,teacher =
                                              me.profile,name=subject)
                # if common subject found that means student is connected to
                # teacher and he should be added to test
                if subs:
                    stu = Student.objects.get(subject = subs)
                    test.testTakers.add(stu)
                    test.save()
            return render(request,'questions/oneclick_test4.html')

        if 'oneclickcreated' in request.POST:
            return render(request,'questions/oneclick_test5.html')

#def oneclick_test(request):
#    user = request.user
#    me = Teach(user)
#    if user.is_authenticated:
#        if 'subquestions' in request.GET:
#            testholder = TemporaryOneClickTestHolder.objects.filter(teacher= me.profile)
#            if testholder:
#                testholder.delete()
#            numQuests = request.GET['subquestions']
#            my_subs = me.my_subjects_names()
#            context = {'subjects': my_subs,'numquests':numQuests}
#            return render(request,'questions/oneclick_test2.html',context)
#        if 'questionsubjects' in request.GET:
#            subsandnumquests = request.GET['questionsubjects']
#            subs = subsandnumquests.split(',')[0]
#            numquests = subsandnumquests.split(',')[1]
#            all_topics = []
#            sub_topics = SSCquestions.objects.filter(section_category = subs)
#            for i in sub_topics:
#                all_topics.append(i.topic_category)
#            all_topics = list(unique_everseen(all_topics))
#            topics = me.change_topicNumbersNames(all_topics,subs)
#            topics = np.array(topics)
#            context =\
#            {'topics':topics[:,0],'subject':subs,'numquests':numquests}
#            return render(request,'questions/oneclick_test3.html',context)
#        if 'createTest' in request.GET:
#            topics = request.GET['createTest']
#            # get topics in string format
#            # count commas to know how many topics are selected
#            # last two commas are for subject and number of questions
#            commacounter = 0
#            for tp in topics:
#                if ',' == str(tp):
#                    commacounter += 1
#            # add topics to separate list (splitting by the commas)
#            tps = []
#            for i in range(commacounter-1):
#                top = topics.split(',')[i]
#                tps.append(top)
#            sub = topics.split(',')[-2]  # get subject
#            numquests = topics.split(',')[-1]  #get number of questions
#            if len(tps)==0:
#                context = {'noneselected':'none'}
#                return render(request,'questions/oneclick_test3.html',context)
#            all_questions = []
#            # change topics names to topics numbers
#            tp = me.change_topicNamesNumber(tps,sub)
#            all_topics = []
#            # get questions topic wise and put them in lists
#            for topic in tp:
#                name = eval("'cat'+topic")
#                questions = SSCquestions.objects.filter(section_category = sub,
#                                                    topic_category = topic)
#                name = []
#                for quest in questions:
#                    all_questions.append(quest)
#                    name.append(quest)
#                all_topics.append(name)
#            all_topics = np.array(all_topics)
#            # get old questions created by the users
#            old_questions = SSCKlassTest.objects.filter(creator = user)
#            oldquestions_list = []
#            for oq in old_questions:
#                for quest in oq.sscquestions_set.all():
#                    oldquestions_list.append(quest)
#            # count number of times questions have been repeated in the past by
#            # the teacher
#            quest_freq = []
#            quest_f = []
#            for quest in all_questions:
#                freq = 0
#                for oq in oldquestions_list:
#                    if quest ==  oq:
#                        freq += 1
#                quest_freq.append(quest.id)
#                quest_f.append(freq)
#            total_freq = list(zip(quest_freq,quest_f))
#            possible = True
#            if (len(all_questions) < int(numquests)):
#                possible = False
#                text = "Sorry choose more categories to have " +\
#                                    numquests + " questions. Currently only " +\
#                                    str(len(all_questions)) + ' questions can\
#                           be added.'
#                context = {'notpossible':text}
#                return render(request,'questions/oneclick_test4.html',context)
#            else:
#                meannumber = int(int(numquests)/len(all_topics))
#                final_list = []
#                for i in range(len(tp)):
#                    for j in range(meannumber):
#                        try:
#                            if len(all_topics[i])==0:
#                                break
#                            topicquestion = random.choice(all_topics[i])
#                            all_topics[i].remove(topicquestion)
#                            if topicquestion in final_list:
#                                pass
#                            else:
#                                final_list.append(topicquestion)
#                        except Exception as e:
#                            topicquestion = random.choice(all_topics[i])
#                            final_list.append(topicquestion)
#                            print(str(e))
#                final_list = list(unique_everseen(final_list))
#                if len(final_list) < int(numquests):
#                    meannumber = int(numquests)
#                    for i in range(len(tp)):
#                        for j in range(meannumber):
#                            try:
#                                if len(final_list) == int(numquests):
#                                    break
#                                if len(all_topics[i])==0:
#                                    break
#                                topicquestion = random.choice(all_topics[i])
#                                all_topics[i].remove(topicquestion)
#                                if topicquestion in final_list:
#                                    pass
#                                else:
#                                    final_list.append(topicquestion)
#                            except Exception as e:
#                                topicquestion = random.choice(all_topics[i])
#                                final_list.append(topicquestion)
#                                print(str(e))
#
#                final_list = list(unique_everseen(final_list))
#                final_id_list = []
#                for i in final_list:
#                    final_id_list.append(i.id)
#                testholder = TemporaryOneClickTestHolder()
#                testholder.teacher = me.profile
#                testholder.quests = final_id_list
#                testholder.save()
#                batches = me.my_classes_names()
#                context =\
#                {'batches':batches,'subject':sub,'numquests':numquests}
#                return render(request,'questions/oneclick_test4.html',context)
#        if 'finalTest' in request.GET:
#            numquests = request.GET['numquests']
#            subject = request.GET['whichsubject']
#            kl = request.GET['classoneclicktest']
#            myTest = TemporaryOneClickTestHolder.objects.get(teacher= me.profile)
#            oneClickTest = SSCKlassTest()
#            oneClickTest.mode = 'BodhiOnline'
#            quest_list = myTest.quests
#            maxMarks = 0
#            for quest in quest_list:
#                question = SSCquestions.objects.get(id = quest)
#                maxMarks += question.max_marks
#
#            kla = klass.objects.get(name = kl, level= 'SSC', school =
#                                   user.teacher.school)
#            print(type(maxMarks))
#            print('%s max marks' %maxMarks)
#
#            kla = me.my_classes_objects(kl)
#            oneClickTest.max_marks =maxMarks
#            oneClickTest.klas = kla
#            oneClickTest.creator = user
#            oneClickTest.totalTime = int(float(0.6)*int(numquests))
#            oneClickTest.published = timezone.now()
#            oneClickTest.name = str(request.user.teacher) + str(timezone.now())
#            oneClickTest.sub = subject
#            oneClickTest.save()
#            for zz in quest_list:
#                q = SSCquestions.objects.get(id = zz)
#                q.ktest.add(oneClickTest)
#            students = Student.objects.filter(klass = kla)
#            for i in students:
#                oneClickTest.testTakers.add(i)
#            oneClickTest.save()
#            return render(request,'questions/teacher_successfully_published.html')



def create_pattern_test(request):
    user = request.user
    if user.is_authenticated:
        me = Teach(user)
        if user.groups.filter(name= 'Teachers').exists():
            testholder = TemporaryOneClickTestHolder.objects.filter(teacher = me.profile)
            if testholder:
                testholder.delete()
            my_batches = me.my_classes_names_cache()
            context = {'batches':my_batches}
            return render(request,'questions/create_pattern_test1.html',context)
def pattern_test(request):
    user = request.user
    me = Teach(user)
    if 'batch_test' in request.GET:
        batch = request.GET['batch_test']
        #subject = me.my_subjects_names()
        subject = me.test_taken_subjects(user)
        context = {'mySubs':subject,'batch':batch}
        return render(request,'questions/create_pattern_test2.html',context)
    if 'batchandsub' in request.GET:
        batchandsub = request.GET['batchandsub']
        sub = batchandsub.split(',')[0]
        batch = batchandsub.split(',')[1]
        school_name = me.my_school()
        kl = klass.objects.get(school = school_name,name = str(batch))
        course = kl.level
        all_tests = SSCKlassTest.objects.filter(sub = sub,course =
                                                course,creator =user, pattern_test = True)
        context = {'alltests':all_tests,'subject':sub,'batch':batch}
        return render(request,'questions/create_pattern_test3.html',context)
    if 'patterntestnumber' in request.GET:
        test_name = request.GET['patterntestnumber']
        testid = test_name.split(',')[0]
        testsubject = test_name.split(',')[1]
        testbatch = test_name.split(',')[2]
        test = SSCKlassTest.objects.get(id=testid)
        print('%s test' %test)
        quests = []
        for qu in test.sscquestions_set.all():
            quests.append(qu)
        print(len(quests))
        context = {'que':quests,'testbatch':testbatch,'testid':testid}
        return render(request,'questions/create_pattern_test4.html',context)
    if 'patternBatch' and 'patternTestid' and 'patternTest' in request.POST:
        batch = request.POST['patternBatch']
        testid = request.POST['patternTestid']
        students = []
        school_name = me.my_school()
        kl = klass.objects.get(school = school_name,name = str(batch))
        test = SSCKlassTest.objects.get(id = testid)
        test.patternTestBatches.add(kl)
        studs = Student.objects.filter(klass=kl)
        for i in studs:
            test.testTakers.add(i)
        test.save()
        return render(request,'questions/create_pattern_test5.html')



def student_smart_tests(request):
    user = request.user
    if user.is_authenticated:
        me = Studs(user)
        subjects = me.my_subjects_names()
        context = {'subjects':subjects}
        return\
    render(request,'questions/student_smart_test1.html',context)

def student_smart_tests2(request):
    if 'which_sub' in request.GET:
        me = Studs(request.user)
        subject = request.GET['which_sub']
        test_taken = SSCOnlineMarks.objects.filter(student =
                                                   me.profile,test__sub=subject)
        if len(test_taken) == 0:
            print('no tests taken')
            context = {'no_test':'Please take at-least one test so that we\
                       can generate a Smart Test for you.'}
        else:
            quest_nums = ['10','15','20','25']
            context = {'subject':subject,'quest_num':quest_nums}
        return\
    render(request,'questions/student_smart_test2.html',context)
    if 'what_number' in request.GET:
        quest_num = request.GET['what_number']
        # subject that student has selected
        subject = quest_num.split(',')[0]
        # number of questions that student has selected
        numQuestions = int(quest_num.split(',')[1])
        # get weak topics of student of a specifict subject that student has
        # chosen
        weakAreas = me.weakAreas_IntensityAverage(subject)
        # order weak areas according to their intensity
        ordered_weakAreas = sorted(weakAreas, key= lambda wa:wa[1],
                                   reverse=True)
        if numQuestions <= 15:
            numTopics = 2
        elif numQuestions > 15:
            numTopics = 4
        # choose topics to incude in test according to number of questions
        chosen_topics = ordered_weakAreas[:numTopics]
        number_questofTopics = int(numQuestions /numTopics)
        print('%d number quest of topics' %number_questofTopics)
        #choose questions according to topics chosen
        all_questions = []
        topic_counter = 1
        max_marks = 0
        for topic,weakness in chosen_topics:
            deficient_by = 0
            if topic_counter == numTopics + 1:
                break
            if numQuestions - len(all_questions) == 0:
                break
           

            questions = SSCquestions.objects.filter(section_category =
                                                    subject,topic_category =
                                                    topic)

            quest_count = 0
            for num,quest in enumerate(questions):
                if topic_counter == len(chosen_topics) and num == 0:
                    number_questofTopics = numQuestions - len(all_questions)

                if quest_count == number_questofTopics:
                    break
                taken = me.isQuestionTaken(quest)
                if taken:
                    continue
                all_questions.append(quest)
                max_marks = max_marks + quest.max_marks
                quest_count += 1
            topic_counter += 1

        smartTest = SSCKlassTest()
        smartTest.creator = User.objects.get(username = 'BodhiAI')
        smartTest.mode = 'BodhiOnline'
        smartTest.name = 'SmartTest' + " " + str(chosen_topics)
        smartTest.sub = subject
        smartTest.max_marks = max_marks
        smartTest.totalTime = len(all_questions) * 0.6
        smartTest.save()
        smartTest.testTakers.add(me.profile)
        for quest in all_questions:
            quest.ktest.add(smartTest)
        print('%s chosen topics' %chosen_topics)
        weak_names = me.changeTopicNumbersNames(chosen_topics,subject)
        print('%s topics' %weak_names)
        weakar = []
        for i,j in weak_names:
            weakar.append(i)
        print(weakar)
        context = {'weakAreas':weakar,'testid':smartTest.id}
        return render(request,"questions/student_smart_test3.html",context)




def student_topic_test(request):
    user = request.user
    me = Studs(user)
    subjects = me.my_subjects_names()
    context = {'subjects':subjects}
    return render(request,'questions/student_topic_test1.html',context)





def see_Test(request):
    user = request.user
    tests = KlassTest.objects.filter(creator = user)
    context = {'tests':tests}
    return render(request, 'questions/seeCreatedTest.html',context)

def student_my_tests(request):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name= 'Students').exists():
            me = Studs(user)
            subjects = me.subjects_OnlineTest()
            subjects = me.subjects_NotTakenTests()
            context = {'subjects':subjects}
            return render(request,'questions/student_my_tests.html',context)


def student_show_onlineTests(request):
    user = request.user
    me = Studs(user)
    if 'onlineTestSubject' in request.GET:
        my_sub = request.GET['onlineTestSubject']
        tests = me.OnlineTestsSubwise(my_sub)
        vtests = []
        for i in tests:
            vt = visible_tests(i.id)
            if vt == None:
                pass
            else:
                vtests.append(vt)
        context = {'tests':tests}
        return render(request,'questions/student_onlinetests_subjectwise.html',context)
    if 'onlineTestid' in request.GET:
        testid = request.GET['onlineTestid']
        old_test = me.is_onlineTestTaken(testid)
        if old_test:
            student_type = 'SSC'
            context = {'marks':old_test,'student_type':student_type}
            return render(request,'questions/student_evaluated_test.html',context)
        else:
            test = SSCKlassTest.objects.get(id = testid)
            quest = []
            for q in test.sscquestions_set.all():
                    quest.append(q.topic_category)
            lenquest = len(quest)
            nums = []
            for i in range(lenquest):
                nums.append(i)
            context = {'questPosition':nums,'te_id':testid}
            return \
            render(request,'questions/student_individual_questionTest.html',context)

    if request.POST:
        all_answers = []
        right_answers = []
        right_answers2 = []
        wrong_answers = []
        wrong_answers2 = []
        skipped_answers = []
        skipped_answers2 = []
        num_of_quests = 0
        testid = request.POST['submitTest']
        test = SSCKlassTest.objects.get(id = testid)
        for j in test.sscquestions_set.all():
            num_of_quests += 1

        for i in range(num_of_quests+1):
            try:
                answerChoice = eval("'answerChoice'+str(i)")
                ans = request.POST[answerChoice]
                all_answers.append(int(ans))
            except:
                pass
        test_marks  = 0
        for qu in test.sscquestions_set.all():
            for ch in qu.choices_set.all():
                if not ch.id in all_answers:
                    skipped_answers.append(qu.id)
                elif ch.id in all_answers and ch.predicament == "Correct":
                    right_answers.append(qu.id)
                    right_answers2.append(ch.id)
                    test_marks += int(qu.max_marks)
                elif ch.id in all_answers and ch.predicament == "Wrong":
                    wrong_answers.append(qu.id)
                    wrong_answers2.append(ch.id)
                    test_marks -= int(qu.negative_marks)
        skipped_answers = list(unique_everseen(skipped_answers))
        for an in skipped_answers:
            if not an in right_answers and not an in wrong_answers:
                skipped_answers2.append(an)
        my_marks = SSCOnlineMarks()
        my_marks.test = test
        my_marks.student = request.user.student
        my_marks.rightAnswers = right_answers2
        my_marks.wrongAnswers = wrong_answers2
        my_marks.skippedAnswers = skipped_answers2
        my_marks.allAnswers = all_answers
        my_marks.marks = test_marks
        my_marks.testTaken = timezone.now()
        my_marks.save()
        context = {'marks':my_marks}
        return render(request,'questions/student_answered_paper.html',context)

def conduct_Test(request):
    user = request.user
    if user.is_authenticated:
        me = Studs(user)
        if '' in request.GET:
            raise Http404('You are not supposed to be here')
        if '' in request.POST:
            raise Http404('You are not supposed to be here')

        if 'onlineTestid' in request.GET:
            testid = request.GET.get('onlineTestid',None)
            if testid is not None:
                testid = int(testid)
            else:
                return HttpResponseRedirect(reverse('basic:home'))
            TemporaryAnswerHolder.objects.filter(stud=me.profile,test__id=testid).delete()
            taken =\
            SSCOnlineMarks.objects.filter(student=me.profile,test__id=testid)
            if len(taken) > 0:
                student_type = 'SSC'
                taken = taken[0]
                total_time = taken.timeTaken
                hours = int(total_time/3600)
                t = int(total_time%3600)
                mins = int(t/60)
                seconds =int(t%60)
                if hours == 0:
                    tt = '{} minutes and {} seconds'.format(mins,seconds)
                if hours == 0 and mins == 0:
                    tt = '{} seconds'.format(seconds)
                if hours > 0:
                    tt = '{} hours {} minutes and {}\
                    seconds'.format(hours,mins,seconds)
            
                context = \
                {'marks':taken,'student_type':student_type,'timetaken':tt}
                return render(request,'questions/student_evaluated_test.html',context)
            else:
                test = SSCKlassTest.objects.get(id=testid)
                if test.totalTime:
                    timeTest = test.totalTime
                else:
                    timeTest = 10000
                mins = timeTest %60
                hours = int(timeTest /60)
                if hours ==1:
                    timer = '{} hour and {} minutes'.format(hours,mins)
                elif hours == 0:
                    timer = '{} minutes'.format(mins)
                else:
                    timer = '{} hours and {} minutes'.format(hours,mins)
                if hours >4:
                    timer = 'Unlimited (no time boundation)'

                quest = []
                for q in test.sscquestions_set.all():
                    quest.append(q)
                num_questions = len(quest)
                context = \
                        {'num_questions':num_questions,'testid':testid,'student_type':'SSC','timer':timer}
                return \
                render(request,'questions/student_startoftest.html',context)


        if 'takeTest' in request.POST:
            testid = request.POST['takeTest']
            testid = int(testid)
            already_taken =\
            SSCOnlineMarks.objects.filter(student=me.profile,test__id =
                                          testid)
            if len(already_taken)>0:
                raise Http404('You have already taken this test, Sorry!!\
                              retakes are not allowed.')

            quest = []
            test = SSCKlassTest.objects.get(id = testid)
            try:
                test_detail = TestDetails.objects.get(test = test)
                lenquest = test_detail.num_questions
            except:
                for q in test.sscquestions_set.all():
                    quest.append(q.topic_category)

                lenquest = len(quest)
            if test.totalTime:
                timeTest = test.totalTime
            else:
                timeTest = 1000
            nums = []
            for i in range(lenquest):
                nums.append(i)
            current_test = StudentCurrentTest()
            current_test.student = me.profile
            current_test.test = SSCKlassTest.objects.get(id=testid)
            current_test.save()
            context =\
                    {'questPosition':nums,'te_id':testid,'how_many':lenquest,'testTime':timeTest}
            return \
            render(request,'questions/student_individual_questionTest.html',context)
        if 'IndividualTestQuestPos' in request.GET:
            # this method gets the value of button pressed and sends the
            # question that is in that place
            questPos = request.GET['IndividualTestQuestPos']
            pos = questPos.split(',')[0]
            testid = questPos.split(',')[1]
            get_place = test_get_QuestionPosition.delay(user.id,int(testid),pos)
            t_id = get_place.task_id
            res = AsyncResult(t_id)
            tosend,test_id,answer_sel,how_many = res.get()
            tosend = SSCquestions.objects.get(id = tosend)
            if answer_sel != -5:
                context = {'question':tosend,'testid':testid,'sel':answer_sel}
            else:
                context =\
                {'question':tosend,'testid':testid,'how_many':how_many}
            return \
        render(request,'questions/student_individual_questionTestquestion.html',context)

        if 'questionid'  in  request.POST:
            # gets the values of choice id and time taken to choose that value
            try:
                choice_id = request.POST['choiceid']
                questTime = request.POST['questTimer']
            except Exception as e:
                choice_id = -1
            # runs when next button is pressed rather than selecting a
            # choice(skipped)
            question_id = request.POST['questionid']
            test_id = request.POST['testid']
            if choice_id == -1:
                questTime = -1
            save_quest =\
            test_get_next_question.delay(user.id,test_id,question_id,choice_id,questTime)
            return HttpResponse(test_id)
        if 'testSub' in request.POST:
            test_id = request.POST['testSub']
            time_taken = request.POST['timeTaken']
            res = evaluate_test.delay(user.id,int(test_id),time_taken)
            test_id = res.get()
            return\
        HttpResponseRedirect(reverse('QuestionsAndPapers:showFinishedTest',args=[test_id]))


def show_finished_test(request,testid):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name= 'Students').exists():
            me = Studs(user)
            if testid != None or testid != '':
                test_details =\
                SSCOnlineMarks.objects.get(student=me.profile,test__id = testid)
            else:
                test_stu =\
                StudentCurrentTest.objects.filter(student=me.profile).order_by('-time')
                test_stu = test_stu[0]
                test_id = test_stu.test.id
                test_details =\
                SSCOnlineMarks.objects.get(student=me.profile,test__id = testid)
            total_time = test_details.timeTaken
            hours = int(total_time/3600)
            t = int(total_time%3600)
            mins = int(t/60)
            seconds =int(t%60)
            try:
                if hours == 0:
                    tt = '{} minutes and {} seconds'.format(mins,seconds)
                if hours == 0 and mins == 0:
                    tt = '{} seconds'.format(seconds)
                if hours > 0:
                    tt = '{} hours {} minutes and {}\
                    seconds'.format(hours,mins,seconds)
            except:
                pass
            try:
                custom_profile = StudentCustomProfile.objects.get(student =
                                                              request.user)
                print('%s found coustom profile' %custom_profile.fullName)
                subject = 'BodhiAI score'
                
                res =\
                student_score_email.delay(subject,test_details.marks,custom_profile.fullName,request.user.email,tt,custom_profile.fatherName,custom_profile.phone,custom_profile.address)
            except Exception as e:
                print(str(e))

            #subject = 'BodhiAI score'
            #from_email = 'bodhiaiindia@gmail.com'
            #to_email = 'prashantbodhi@gmail.com'
            #contact_message = '''
            #Hello %s , Welcome to BodhiAI. 
            #You recently took a test for JITO. 
            #Here is your result:
            #You got  %s
            #Total time taken : %s
            #'''%(me.profile,test_details.marks,tt)
            #send_mail(subject,contact_message,from_email,[to_email],fail_silently
            #          = False)
            student_type='SSC'
            try:
                context = \
                {'student_type':student_type,'marks':test_details,'timetaken':tt}
            except:
                context = \
                {'student_type':student_type,'marks':test_details,'timetaken':'unliimited'}


            return render(request,'questions/student_finished_test.html',context)


def teacher_create_time_table(request):
    print('in create time table')
    form = CreateTimeTableForm(request.POST or None)
    context = {'form':form}
    if request.POST:
        me = Teach(request.user)
        batch = request.POST['batch']
        sub = request.POST['sub']
        date = request.POST['date']
        time = request.POST['time']
        note = request.POST['note']
        time_table = TimeTable()
        print(batch,sub,date,time,note)
        subs = me.my_subjects_names()
        if sub in subs:
            batch = klass.objects.get(id = batch)
            time_table.batch = batch
            time_table.teacher = me.profile
            time_table.sub = sub
            time_table.time = time
            time_table.date = datetime.strptime(date,"%d/%m/%Y")
            time_table.note = note
            time_table.save()
            return HttpResponseRedirect(reverse('basic:home'))
    print('returning form')
    return render(request, 'questions/CreateTimeTable.html', context)
