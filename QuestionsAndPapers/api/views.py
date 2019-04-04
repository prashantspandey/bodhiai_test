from rest_framework import generics
from basicinformation.tasks import *
from celery.result import AsyncResult
from rest_framework.decorators import api_view 
from rest_framework.views import APIView
from basicinformation.models import *
from django.http import Http404, HttpResponse 
from .serializers import *
from basicinformation.marksprediction import *
from QuestionsAndPapers.models import *
import json
from more_itertools import unique_everseen
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated
)
from basicinformation.tasks import *
from django.utils import timezone
from django.utils.timezone import localdate
import numpy as np
import math
# ALL STUDENT APIs

#---------------------------------------------------------------------------------------

# returns information about test papers yet to be taken by the student 
# only returns 3 topics in a test 
class StudentPaperDetailsAPIView(APIView):

    def get(self,request,format=None):
        user = self.request.user
        me = Studs(user)
        my_tests = SSCOnlineMarks.objects.filter(student = me.profile)
        taken_ids = []
        for test in my_tests:
            taken_ids.append(test.test.id)
        new_tests = SSCKlassTest.objects.filter(testTakers =
                                                me.profile).order_by('-id')[:10]
        tests = []
        test_details = {}
        for te in new_tests:
            if te.id not in taken_ids:
                tests.append(te.id)
                topics,num_questions = self.find_topics(te)
                try:
                    subject_logo = SubjectLogo.objects.get(name=te.sub)
                    logo_url = subject_logo.logo2
                except:
                    logo_url = None
                test_details[te.id] =\
                        {'topics':topics[:2],'num_questions':num_questions,'subject':te.sub,'published':te.published,'creator':te.creator.teacher.name,'logo':logo_url}

        return Response(test_details)

    def find_topics(self,test):
        topics = []
        tp_num = []
        for quest in test.sscquestions_set.all():
            tp_number = quest.topic_category
            try:
                tp_name = changeIndividualNames(tp_number,quest.section_category)
            except:
                tp_name = 'Topics'
            topics.append(tp_name)
        topics = list(unique_everseen(topics))
        num_questions = len(test.sscquestions_set.all())
        return topics,num_questions


#---------------------------------------------------------------------------------------
class StudentPaperDetailsAndroidAPIView(APIView):

    def get(self,request,format=None):
        user = self.request.user
        me = Studs(user)
        my_tests = SSCOnlineMarks.objects.filter(student = me.profile)
        taken_ids = []
        for test in my_tests:
            taken_ids.append(test.test.id)

        new_tests = SSCKlassTest.objects.filter(testTakers =
                                                me.profile).order_by('-id')

        tests = []
        test_details = {}
        details = []
        counter = 0
        for te in new_tests:
            if te.id not in taken_ids:
                if counter == 6:
                    break
                counter += 1
                tests.append(te.id)
                topics,num_questions = self.find_topics(te)
                try:
                    subject_logo = SubjectLogo.objects.get(name=te.sub)
                    logo_url = subject_logo.logo2
                except:
                    logo_url = None

                test_details =\
                        {'id':te.id,'topics':topics[:3],'num_questions':num_questions,'subject':te.sub,'published':te.published,'creator':te.creator.teacher.name,'logo':logo_url}
                details.append(test_details)

        return Response(details)

    def find_topics(self,test):
        topics = []
        tp_num = []
        for quest in test.sscquestions_set.all():
            tp_number = quest.topic_category
            try:
                subject_chapter =\
                SubjectChapters.objects.get(subject=quest.section_category,code=float(tp_number))
                tp_name = subject_chapter.name
            except:
                tp_name = 'Topics'
            topics.append(tp_name)
        topics = list(unique_everseen(topics))
        num_questions = len(test.sscquestions_set.all())
        return topics,num_questions

class StudentPaperDetailsAndroidPaginatedAPIView(APIView):
    def post(self,request,*args,**kwargs):
        user = self.request.user
        me = Studs(user)
        page = request.POST['page']
        current = int(page) * int(10)
        end = current + 10
        my_tests = SSCOnlineMarks.objects.filter(student = me.profile)
        taken_ids = []
        for test in my_tests:
            taken_ids.append(test.test.id)
        new_tests = SSCKlassTest.objects.filter(testTakers =
                                                me.profile).order_by('-id')
        total_pages_final = (len(new_tests) /10)
        if total_pages_final % 10 == 0:
            total_pages_final = total_pages_final
        else:
            total_pages_final = math.ceil(total_pages_final)

        tests = []
        test_details = {}
        details = []
        print('{} from to {} -- {} total'.format(current,end,total_pages_final))
        for te in new_tests[int(current):int(end)]:
            if te.id not in taken_ids:
                tests.append(te.id)
                topics,num_questions = self.find_topics(te)
                test_details =\
                        {'id':te.id,'topics':topics[:2],'num_questions':num_questions,'subject':te.sub,'published':te.published,'creator':te.creator.teacher.name,'page':page,'total_pages':total_pages_final}
                details.append(test_details)
        
        return Response(details)

    def find_topics(self,test):
        topics = []
        tp_num = []
        for quest in test.sscquestions_set.all():
            tp_number = quest.topic_category
            tp_name = changeIndividualNames(tp_number,quest.section_category)
            topics.append(tp_name)
        topics = list(unique_everseen(topics))
        num_questions = len(test.sscquestions_set.all())
        return topics,num_questions



class StudentPaperDetailsFilter(APIView):

    def post(self,request,format=None):
        data = request.data
        typeTest = data['typeTest']
        user = self.request.user
        me = Studs(user)
        my_tests = SSCOnlineMarks.objects.filter(student = me.profile)
        taken_ids = []
        for test in my_tests:
            taken_ids.append(test.test.id)


        if typeTest == 'MockTest':
            new_tests = SSCKlassTest.objects.filter(testTakers =
                                                    me.profile).order_by('-id')

            tests = []
            test_details = {}
            details = []
            counter = 0
            for te in new_tests:
                if te.id not in taken_ids:
                    if 'multiple' in te.sub or 'Multiple' in te.sub:
                        tests.append(te.id)
                        try:
                            subject_logo = SubjectLogo.objects.get(name=te.sub)
                            logo_url = subject_logo.logo2
                        except:
                            logo_url = None

                        test_details =\
                                {'id':te.id,'topics':[],'num_questions':None,'subject':te.sub,'published':te.published,'creator':te.creator.teacher.name,'logo':logo_url}
                        details.append(test_details)

            return Response(details)
        elif typeTest == 'SubjectTest':
            new_tests = SSCKlassTest.objects.filter(testTakers =
                                                    me.profile).order_by('-id')

            tests = []
            test_details = {}
            details = []
            counter = 0
            for te in new_tests:
                if te.id not in taken_ids:
                    if 'multiple' not in te.sub or 'Multiple' not in te.sub:
                        tests.append(te.id)
                        topics,num_questions = self.find_topics(te)
                        try:
                            subject_logo = SubjectLogo.objects.get(name=te.sub)
                            logo_url = subject_logo.logo2
                        except:
                            logo_url = None

                        test_details =\
                                {'id':te.id,'topics':topics[:3],'num_questions':num_questions,'subject':te.sub,'published':te.published,'creator':te.creator.teacher.name,'logo':logo_url}
                        details.append(test_details)

            return Response(details)
 

    def find_topics(self,test):
        topics = []
        tp_num = []
        for quest in test.sscquestions_set.all():
            tp_number = quest.topic_category
            try:
                subject_chapter =\
                SubjectChapters.objects.get(subject=quest.section_category,code=float(tp_number))
                tp_name = subject_chapter.name
            except:
                tp_name = 'Topics'
            topics.append(tp_name)
        topics = list(unique_everseen(topics))
        num_questions = len(test.sscquestions_set.all())
        return topics,num_questions

class GetMockTests(APIView):

    def get(self,request,format=None):
        user = self.request.user
        me = Studs(user)
        my_tests = SSCOnlineMarks.objects.filter(student = me.profile)
        taken_ids = []
        for test in my_tests:
            taken_ids.append(test.test.id)


        new_tests = SSCKlassTest.objects.filter(testTakers =
                                                    me.profile,mock_test=True).order_by('id')

        tests = []
        test_details = {}
        details = []
        counter = 0
        for te in new_tests:
            if te.id not in taken_ids:
                    tests.append(te.id)
                    try:
                        subject_logo = SubjectLogo.objects.get(name=te.sub)
                        logo_url = subject_logo.logo2
                    except:
                        logo_url = None

                    test_details =\
                            {'id':te.id,'topics':topics,'num_questions':num_questions,'subject':te.sub,'published':te.published,'creator':te.creator.teacher.name,'logo':logo_url}
                    details.append(test_details)

        return Response(details)


    def find_topics(self,test):
        topics = []
        tp_num = []
        for quest in test.sscquestions_set.all():
            tp_number = quest.topic_category
            try:
                subject_chapter =\
                SubjectChapters.objects.get(subject=quest.section_category,code=float(tp_number))
                tp_name = subject_chapter.name
            except:
                tp_name = 'Topics'
            topics.append(tp_name)
        topics = list(unique_everseen(topics))
        num_questions = len(test.sscquestions_set.all())
        return topics,num_questions

class GetSubjectTests(APIView):
    def get(self,request):
        user = self.request.user
        me = Studs(user)

        new_tests = SSCKlassTest.objects.filter(testTakers =
                                                me.profile).order_by('-id')

        tests = []
        test_details = {}
        details = []
        counter = 0
        for te in new_tests:
            if te.id not in taken_ids:
                if 'multiple' not in te.sub or 'Multiple' not in te.sub:
                    tests.append(te.id)
                    topics,num_questions = self.find_topics(te)
                    try:
                        subject_logo = SubjectLogo.objects.get(name=te.sub)
                        logo_url = subject_logo.logo2
                    except:
                        logo_url = None

                    test_details =\
                            {'id':te.id,'topics':topics[:3],'num_questions':num_questions,'subject':te.sub,'published':te.published,'creator':te.creator.teacher.name,'logo':logo_url}
                    details.append(test_details)

        return Response(details)
 

    def find_topics(self,test):
        topics = []
        tp_num = []
        for quest in test.sscquestions_set.all():
            tp_number = quest.topic_category
            try:
                subject_chapter =\
                SubjectChapters.objects.get(subject=quest.section_category,code=float(tp_number))
                tp_name = subject_chapter.name
            except:
                tp_name = 'Topics'
            topics.append(tp_name)
        topics = list(unique_everseen(topics))
        num_questions = len(test.sscquestions_set.all())
        return topics,num_questions


#---------------------------------------------------------------------------------------

# When student clicks on show more topics then this api returns all the topcis
# of a particular test
class StudentShowAllTopicsOfTest(APIView):

    def post(self,request,*args,**kwargs):
        te_id = request.POST['test_id']
        test = SSCKlassTest.objects.get(id = te_id)
        topics = []
        for quest in test.sscquestions_set.all():
            number = quest.topic_category
            name = changeIndividualNames(number,quest.section_category)
            topics.append(name)
        topics = list(unique_everseen(topics))
        return Response(topics)



#---------------------------------------------------------------------------------------

# Get all the details of a test (post: test_id)

class  IndividualTestDetailsAPIView(APIView):

    def post(self,request,*args,**kwargs):
        data = request.data

        test_id = data['testid']
        test = SSCKlassTest.objects.get(id= test_id)
        topics = []
        images = []
        for quest in test.sscquestions_set.all():
            number = quest.topic_category
            subject_chapter =\
            SubjectChapters.objects.get(subject=quest.section_category,code=float(number))
            try:
                quest_image = quest.picture
                if quest_image is not None:
                    images.append(quest_image)
            except:
                pass
            options = quest.choices_set.all()
            for opt in options:
                try:
                    opt_image = opt.picture
                    if opt_image is not None:
                        images.append(opt_image)
                except:
                    pass
            
            name = subject_chapter.name
            topics.append(name)
        topics = list(unique_everseen(topics))
        subject = test.sub
        num_questions = len(test.sscquestions_set.all())
        totalTime = test.totalTime
        maxMarks = test.max_marks
        published = test.published
        details = \
                {'id':test_id,'topics':topics,'numQuestions':num_questions,'subject':subject,'time':totalTime,'maxMarks':maxMarks,'publised':published,'images':images}
        return Response(details)


#-------------------------------------------------------------------------------------
# All test taking APIs

#When Start test button is clicked ('TakeTest') post request

class ConductTestFirstAPIview(APIView):
    def post(self,request,*args,**kwargs):
        me = Studs(self.request.user)
        testid = request.POST['takeTest']
        testid = int(testid)
        already_taken =\
        SSCOnlineMarks.objects.filter(student=me.profile,test__id =
                                      testid)

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
        return Response(context)


class TeacherOneClickTestOneAPIView(APIView):
    def get(self,request,format=None):
        me = Teach(self.request.user)
        testholder = TemporaryOneClickTestHolder.objects.filter(teacher= me.profile)
        if testholder:
            testholder.delete()
        my_batches = me.my_classes_names_cache()
        context = {'myBatches':my_batches}
        return Response(context)


class TeacherOneClickTestSubjectsAPIView(APIView):
    def post(self,request,*args,**kwargs):
        clickBatch = request.POST['oneclickbatches']
        print('%s click batch' %clickBatch)
        me = Teach(self.request.user)
        testholder = TemporaryOneClickTestHolder.objects.filter(teacher= me.profile)
        if testholder:
            testholder.delete()
        my_subs = me.my_subjects_names()
        context = {'subjects': my_subs,'oneClickBatch':clickBatch}
        return Response(context)
 
class TeacherOneClickTestChaptersAPIView(APIView):
    def post(self,request,*args,**kwargs):
        subandbatch = request.POST['questionsubjects']
        me = Teach(self.request.user)
        sub = subandbatch.split(',')[0]
        batch = subandbatch.split(',')[1]
        print('{} one click chapters'.format(subandbatch))
        school = me.my_school()
        all_topics = []
        sub_topics = SSCquestions.objects.filter(section_category =
                                                 sub,school = school)
        topics = SubjectChapters.objects.filter(subject=sub)
        all_categories = []
        category_code = []
        for tp in topics:
            all_categories.append(tp.name)
            category_code.append(tp.code)
        cats_final = list(zip(all_categories,category_code))
        context = \
                {'chapters':cats_final,'oneclickbatch':batch,'subject':sub}

        #for i in sub_topics:
        #    all_topics.append(i.topic_category)
        #all_topics = list(unique_everseen(all_topics))
        #topics = me.change_topicNumbersNames(all_topics,sub)
        #topics = np.array(topics)
        #print('{} onel click topics'.format(topics))
        #context = {'chapters':topics,'subject':sub,'oneclickbatch':batch}
        return Response(context)

class TeacherOneClickConfirmAPIView(APIView):
    def post(self,request,*args,**kwargs):
        user = request.user
        me = Teach(user)
        topicnumber = request.POST['chapters'];
        subject = request.POST['subject']
        batch = request.POST['batch']
        kl = klass.objects.get(school = me.my_school(),name=batch)
        tps = topicnumber.split(',')
        inner = []
        outer = []
        tot = 0
        for n,a in enumerate(tps):
            a = a.replace('[','')
            a = a.replace(']','')
            inner.append(a)
            if (n+1)%2 == 0:
                outer.append(list(inner))
                inner = []


        topics_total = np.array(outer)
        final_num = []
        final_name = []
        # creation of one click paper
        
        # class object to find out how many times has the teacher used a
        # question for that certain class
        test_quest = []  # the question containing list
        print('{} total topics in test'.format(topics_total))
        for cat,num in topics_total:
            cat = cat.strip()
            num = int(num)
            if num == 0:
                continue
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

                if len(t_used) == 0 and count < int(num):
                    cat_quest.append(quest)
                # otherwise add used questions to the used_quest list
                if len(t_used) != 0:
                    used_quests.append(quest)
            # check if there are not enough new(unused) questions 
            if len(cat_quest) < int(num):
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
        serializer = SSCQuestionSerializerNew(test_quest,many=True)
        return Response(serializer.data)
   
class TeacherOneClickFinalAPIView(APIView):
    def post(self,request,*args,**kwargs):
        print('in one click final')
        subject = request.POST['subject']
        batch = request.POST['batch']
        quest_ids = request.POST['quest_ids']
        CreateOneClickTestFinal.delay(self.request.user.id,batch,subject,quest_ids)
        context = {'success':'Test successfully created'}
        return Response(context)


# For all normal create test apis

class CreateTestBatchesAPIView(APIView):
    def get(self,request,format=None):
        user = self.request.user
        me = Teach(user)
        all_klasses = me.my_classes_names_cache()
        my_batches = {'myBatches':all_klasses}
        return Response(my_batches)

class CreateTestSubjectsAPIView(APIView):
    def post(self,request,*args,**kwargs):
        user = self.request.user
        me = Teach(user)
        ttt = request.POST['batch']
        
        quest = SSCquestions.objects.filter(school=
                                            me.profile.school)
        if len(quest)!=0:
            my_subs = me.my_subjects_names()

            context = {'subjects':
                       my_subs,'klass':ttt}
            return Response(context)
        else:
            noTest = 'Not Questions for this class'
            context = {'noTest':noTest}
            return Response(context)


class CreateTestChaptersAPIView(APIView):
    def post(self,request,*args,**kwargs):
        category_klass = request.POST['getChapters']
        user = self.request.user
        me = Teach(user)

        split_category = category_klass.split(',')[0]
        split_klass = category_klass.split(',')[1]
        quest = SSCquestions.objects.filter(section_category =
                                            split_category,school
                                            =me.profile.school)
        topics = SubjectChapters.objects.filter(subject=split_category)
        all_categories = []
        category_code = []
        for tp in topics:
            all_categories.append(tp.name)
            category_code.append(tp.code)
        #all_categories = []
        #for i in quest:
        #    all_categories.append(i.topic_category)
        #all_categories = list(unique_everseen(all_categories))
        cats_final = list(zip(all_categories,category_code))
        #all_categories = \
        #me.change_topicNumbersNames(all_categories,split_category)
        #all_categories.sort()
        context = \
                {'chapters':cats_final,'klass':split_klass,'subject':split_category}
        return Response(context)

class CreateTestQuestionsAPIView(APIView):
    def post(self,request,*args,**kwargs):
        me = Teach(self.request.user)
        which_chap = request.POST['chapter_test']
        print('{} which chap'.format(which_chap))
        questions_list = []
        splitChap = which_chap.split(",")[0]
        splitClass = which_chap.split(",")[1]
        splitSection = which_chap.split(",")[2]
        print('{},{},{} --splitchap,splitclass,splicsection'.format(splitChap,splitClass,splitSection))
        qu = \
    SSCquestions.objects.filter(topic_category=splitChap,school=me.profile.school,section_category=splitSection)
        print('{} number of questions in test'.format(len(qu)))
        serializer = SSCQuestionSerializerNew(qu,many=True)
        return Response(serializer.data)


class CreateTestFinalAPIView(APIView):
    def post(self,request,*args,**kwargs):
        print('in last test api')
        me = Teach(self.request.user)
        quest_list  = request.POST['questions_list']
        all_questions = []
        total_marks = 0
        print('{} quest_list'.format(quest_list))
        if ',' in quest_list:
            quest_list = quest_list.split(',')
            for qu in quest_list:
                print('this is qu {}'.format(qu))
                questions = SSCquestions.objects.get(id = int(qu))
                total_marks = total_marks + questions.max_marks
                all_questions.append(questions)

        else:
                questions = SSCquestions.objects.get(id = int(quest_list))
                total_marks = total_marks + questions.max_marks
                all_questions.append(questions)

        serializer = SSCQuestionSerializerNew(all_questions,many=True)
        title = 'Test can be created for you'
        body = 'Number of questions: '+ str(len(all_questions))+ ' '+ 'of '+\
        str(total_marks)


        context =\
        {'totalMarks':total_marks,'questions':serializer.data,'number_questions':len(all_questions)}
        return Response(context)

class CreateTestAPIView(APIView):
    def post(self,request,*args,**kwargs):
        quest_list = request.POST['quest_list']
        date = request.POST['date']
        time = request.POST['time']
        klass = request.POST['batch']
        create_test_api.delay(self.request.user.id,quest_list,date,time,klass)
        context = {'success':'Successfully created'}
        return Response(context)
        


class StudentSubjectsAPIView(APIView):
    def get(self,request):
        me = Studs(self.request.user)
        return response(me.my_subjects_names)


class StudentTakeTestAPIView(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        me = Studs(self.request.user)
        test_id = data['test_id']
        test = SSCKlassTest.objects.get(id = int(test_id))
        #questions = test.sscquestions_set.all()
        serializer = TestSerializer(test)
        return Response(serializer.data)

class StudentEvaluateTestAPIView(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        test_id = data['test_id']
        answers = data['answers']
        total_time = data['total_time']
        answers = answers.split(',')
        inner = []
        outer = []
        tot = 0
        for n,a in enumerate(answers):
            a = a.replace('[','')
            a = a.replace(']','')
            val = int(a)
            inner.append(val)
            if (n+1)%3 == 0:
                outer.append(list(inner))
                inner = []




        outer = np.array(outer)
        me = Studs(self.request.user)
        test = SSCKlassTest.objects.get(id = test_id)
        subject = test.sub
        online_marks = SSCOnlineMarks()
        online_marks.test = test
        online_marks.testTaken = localdate()
        online_marks.testTakenTime = timezone.now()
        online_marks.student = me.profile
        total_marks = 0
        right_answers = []
        wrong_answers = []
        skipped_answers = []
        all_answers = []
        details = []
        subjects_in_test_list = []
        for qid,chid,time in outer:
            question = SSCquestions.objects.get(id = qid)
            subjects_in_test_list.append(question.section_category)
            all_answers.append(chid)
            if chid == -1:
                skipped_answers.append(qid)
            for ch in question.choices_set.all():
                if chid == ch.id:
                    pred = ch.predicament
                    if pred =='Correct':
                        total_marks += question.max_marks
                        right_answers.append(chid)
                    if pred == 'Wrong':
                        total_marks -= question.negative_marks
                        wrong_answers.append(chid)
            answered_detail = eval('"detail",chid')
            answered_detail = SSCansweredQuestion()
            answered_detail.quest = question
            answered_detail.time = time
            details.append(answered_detail)
        all_answers = list(unique_everseen(all_answers))
        online_marks.allAnswers = all_answers
        online_marks.marks = total_marks
        online_marks.test = test
        online_marks.rightAnswers = right_answers
        online_marks.wrongAnswers = wrong_answers
        online_marks.skippedAnswers = skipped_answers
        online_marks.timeTaken = total_time
        online_marks.save()
        for i in details:
            i.onlineMarks = online_marks
            i.save()

        serializer = SSCOnlineMarksSerializer(online_marks)
        context = {'marks':serializer.data}
        subjects_in_test_list = list(unique_everseen(subjects_in_test_list))
        try:
            fill_subjects.delay(me.profile.id,subject)
        except Exception as e:
            print(str(e))
        try:
            track_progress_cache.delay(me.profile.id,subject,online_marks.id)
        except Exception as e:
            print(str(e))
        try:
            CreateUpdateStudentWeakAreas.delay(me.profile.id,subject,online_marks.id)
        except Exception as e:
            print(str(e))
        try:
            CreateUpdateStudentAverageTimingDetail.delay(me.profile.id,subject,online_marks.id)
        except Exception as e:
            print(str(e))
        try:
            saveTestRank.delay(test_id)
        except Exception as e:
            print(str(e))
        for sub in subjects_in_test_list:
            try:
                saveSubjectWiseAccuracyCache.delay(self.request.user.id,test_id,sub)
            except Exception as e:
                print(str(e))
        for sub in subjects_in_test_list:
            try:
                saveSubjectWiseAccuracyRanking.delay(self.request.user.id,sub)
            except Exception as e:
                print('error in subject accuracy rank {}'.format(str(e)))
        for sub in subjects_in_test_list:
            try:
                saveChapterWiseAccuracyCache.delay(self.request.user.id,test_id,sub)
            except Exception as e:
                print('error in chapter accuracy rank {}'.format(str(e)))
        try:
            send_notification_challenged.delay(me.profile.id,str(total_marks))
        except Exception as e:
            print(str(e))
        try:
            updateStudyPlan.delay(me.profile.id,online_marks.id)
        except Exception as e:
            print(str(e))


        return Response(context)

class StudentSmartTestSubjectAPIView(APIView):
    def get(self,request,format=None):
        me = Studs(self.request.user)
        #subjects = me.already_takenTests_Subjects()
        subjects = me.my_taken_subjects()
        context = {'subjects':subjects}
        return Response(context)

class StudentSmartTestCreationAPIView(APIView):
    def post(self,request,*args,**kwargs):
        me = Studs(self.request.user)
        data = request.data
        subject = data['subject']
        #weakAreas = me.weakAreas_IntensityAverage(subject)
        weakAreasCache = StudentWeakAreasChapterCache.objects.filter(student =
                                                                    me.profile,subject
                                                                    = subject)
        chapters = []
        all_chapters = []
        all_accuracies = []
        for wac in weakAreasCache:
            if wac.totalAttempted != 0:
                all_chapters.append(wac.chapter)
                all_accuracies.append(wac.accuracy)
        all_weakness = list(zip(all_chapters,all_accuracies))
        ordered_chapters = sorted(all_weakness,key=lambda x: x[1])




        # order weak areas according to their intensity
        #ordered_weakAreas = sorted(weakAreas, key= lambda wa:wa[1],
        #                           reverse=True)
        numTopics = 2
        numQuestions = 10
        # choose topics to incude in test according to number of questions
        chosen_topics = ordered_chapters[:numTopics]
        print(chosen_topics)
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
        weak_names = me.changeTopicNumbersNames(chosen_topics,subject)
        weakar = []
        for i,j in weak_names:
            weakar.append(i)
        context = {'weakAreas':weakar,'test':smartTest.id}
        return Response(context)

class GetAllQuestions(APIView):
    def get(self,request):
        me = Teach(self.request.user)
        quests = SSCquestions.objects.filter(section_category
                                             ='LocoPilot_Diesel')
        serializer = SSCQuestionSerializer(quests,many=True)
        return Response(serializer.data)

class test_json(APIView):
    def get(self,request):
        quests = SSCquestions.objects.all()[:100]
        serializer = SSCQuestionSerializerNew(quests,many=True)
        return Response(serializer.data)


class getSubjectChapterTestAPIView(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        test_sub = data['subject']
        test_chapter = data['chapter']
        user = self.request.user
        me = Studs(user)
        my_tests = SSCOnlineMarks.objects.filter(student = me.profile)
        taken_ids = []
        for test in my_tests:
            taken_ids.append(test.test.id)
        new_tests = SSCKlassTest.objects.filter(testTakers =
                                                me.profile,sub=test_sub).order_by('-id')

        tests = []
        test_details = {}
        details = []
        for te in new_tests:
            if te.id in taken_ids:
                taken = 'True'
            else:
                taken = 'False'
                tests.append(te.id)
                num_questions,isChapter =\
                self.find_topics(te,test_chapter)


                if isChapter == False:
                    continue
                else:
                    test_details =\
                            {'id':te.id,'topics':test_chapter,'num_questions':num_questions,'subject':te.sub,'published':te.published,'creator':te.creator.teacher.name,'taken':taken}
                    details.append(test_details)

        return Response(details)

    def find_topics(self,test,chapter_cat):
        topics = []
        tp_num = []
        for quest in test.sscquestions_set.all():
            tp_number = quest.topic_category
            try:
                subject_chapter =\
                SubjectChapters.objects.get(subject=quest.section_category,code=float(tp_number))
                tp_name = subject_chapter.name
            except:
                tp_name = 'Topics'
            topics.append(tp_name)
 

        topics = list(unique_everseen(topics))
        isChapter = False
        num_questions = len(test.sscquestions_set.all())
        if len(topics) == 1 and chapter_cat == topics[0]:
            isChapter = True
            return num_questions,isChapter
        else:
            return num_questions,isChapter

class CreatePatternTestCheckExam(APIView):
    def get(self,request):
        user = request.user
        me = Teach(user)
        existing_pattern = PatternTestPattern.objects.all()
        exams = []
        for ep in existing_pattern:
            exams.append(ep.exam_name)
        context = {'exam':exams}
        return Response(context)
 
class CreatePatternTestFinal(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        user = request.user
        me = Teach(user)
        exam = request.POST['exam']
        batch = request.POST['batch']
        # get the existing pattern of subject 
        existing_pattern = PatternTestPattern.objects.get(exam_name=exam)
        pattern_subject = existing_pattern.subjects
        pattern_number_questions = existing_pattern.numberQuestions
        final_pattern = list(zip(pattern_subject,pattern_number_questions))
        kl = klass.objects.get(school = me.my_school(),name=batch)
        test_questions_list_all = []  # all questions that will appear in test
        # choose number of questions in pattern from existing questions in
        print('the final pattern {}'.format(final_pattern))
        for sub,number_questions in final_pattern:
            test_questions_list_subject = []
            subject_chapters = SubjectChapters.objects.filter(subject =sub)
            perChapterQuestions = number_questions / len(subject_chapters)
            if perChapterQuestions >= 1:
                perChapterQuestions = math.ceil(perChapterQuestions)
            else:
                perChapterQuestions = 1
            print('per chapter questions {}'.format(perChapterQuestions))

            for ch in subject_chapters:
                questions = SSCquestions.objects.filter(topic_category =
                                                    str(ch.code),section_category =
                                                    sub,school=me.my_school())
                test_questions_list = [] # questions to be in test list
                used_questions_list = [] # already used questions containing list
                # get the number of times used object associated with the
                # question
                pattern_tests = SSCKlassTest.objects.filter(pattern_test =
                                                        True,klas=kl)
                used_questions_id = []
                for pt in pattern_tests:
                    test_questions = pt.sscquestions_set.all()
                    for tq in test_questions:
                        used_questions_id.append(tq.id)
                for count_chapter_question,chapter_question in\
                enumerate(questions):
                    if chapter_question.id in used_questions_id:
                        used_questions_list.append(chapter_question)
                    elif count_chapter_question < perChapterQuestions and\
                    number_questions > len(test_questions_list_subject):
                        test_questions_list.append(chapter_question)
               

            # check if there are not enough new(unused) questions 
                if len(test_questions_list) < int(perChapterQuestions) and\
                number_questions > len(test_questions_list_subject):
                    try:
                        # if yes then add already used questions to list until
                        # list is equal to number of required questions
                        for used_count,used_question in enumerate(used_questions_list):
                            if used_count < len(perChapterQuestions) and\
                            number_questions > len(test_questions_list_subject):
                                test_questions_list.append(used_question)
                    except Exception as e:
                        print(str(e))
                # finally add all questions to final questions list
                print('subject - {}, chapter - {}, number of questions -\
                      {}'.format(sub,ch.name,len(test_questions_list)))
                test_questions_list_subject.extend(test_questions_list)
            test_questions_list_all.extend(test_questions_list_subject)
        # setting up the test
        # getting all the ids of questions to be used in test
        final_questions_id = []
        for quest in test_questions_list_all:
            final_questions_id.append(quest.id)
        CreateOneClickTestFinal.delay(user.id,batch,'SSCMultipleSections',final_questions_id,patternTest
                                     = True)

        #serializer = SSCQuestionSerializerNew(test_quest,many=True)
        context = {'success':'success',"quetion id":final_questions_id}
        return Response(context)

class TeacherGetSubjects(APIView):
    def get(self,request):
        me = Teach(self.request.user)
        my_subs = me.my_subjects_names()

        context = {'subjects':my_subs}
        return Response(context)

 
