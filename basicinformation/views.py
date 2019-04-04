from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
import os.path
from django.contrib.auth import (
                                logout,
                                 )

import pickle
from django.http import Http404, HttpResponse
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from random import randint
from django.views.decorators.csrf import ensure_csrf_cookie
from datetime import timedelta
import math
from datetime import date
import numpy as np
import pandas as pd
import urllib.request
from more_itertools import unique_everseen
from django.contrib.auth.models import User, Group
from .models import *
from django.utils import timezone
from django.contrib.staticfiles.templatetags.staticfiles import static
from Recommendations.models import *
from .marksprediction import *
from operator import itemgetter
from io import BytesIO as IO
import timeit
from PIL import Image
import requests
from django.contrib import messages
from celery.result import AsyncResult
from django.core import serializers
from time import sleep
from membership.forms import StudentInformationForm,StudentForm
from .tasks import *


def jitoData(request):
    user = request.user
    if user.is_authenticated:
        try:
            student_information = StudentCustomProfile.objects.get(student = user)
            return HttpResponse('hello')
        except:
            if request.POST:
                form = StudentInformationForm(request.POST or None)
                if form.is_valid():
                    address = form.cleaned_data['address']
                    phone = form.cleaned_data['phone']
                    kl = form.cleaned_data['kl']
                    fatherName = form.cleaned_data['fatherName']
                    fullName = form.cleaned_data['fullName']
                    student_info = StudentCustomProfile()
                    student_info.fatherName = fatherName
                    student_info.kl = kl
                    student_info.fullName = fullName
                    student_info.address = address
                    student_info.phone = phone
                    student_info.student = user
                    student_info.save()
                    school = School.objects.get(name='JITO')
                    jito_teacher = Teacher.objects.get(name='JITO')
                    print('%s kl'  %kl)
                    if str(kl) == str(10):
                        cl = klass.objects.get(name = '10th')
                    elif str(kl) == str(11):
                        cl = klass.objects.get(name = '11th')
                    elif str(kl) == str(12):
                        cl = klass.objects.get(name = '12th')
                    stu = Student(studentuser = user,klass=cl,name =
                                  fullName,school = school)

                    stu.save()
                    if str(kl) == str(10):
                        submaths = Subject(name='MathsIITJEE10',student =
                                           stu,teacher=jito_teacher)
                        subphy = Subject(name='PhysicsIITJEE10',student =
                                           stu,teacher=jito_teacher)
                        subchem = Subject(name='ChemistryIITJEE10',student =
                                           stu,teacher=jito_teacher)
                        subability = Subject(name='MentalAbilityIITJEE10',student =
                                           stu,teacher=jito_teacher)
                        subintelligence = Subject(name='General-Intelligence',student =
                                           stu,teacher=jito_teacher)



                    elif str(kl) == str(11):
                        submaths = Subject(name='MathsIITJEE11',student =
                                           stu,teacher=jito_teacher)
                        subphy = Subject(name='PhysicsIITJEE11',student =
                                           stu,teacher=jito_teacher)
                        subchem = Subject(name='ChemistryIITJEE11',student =
                                           stu,teacher=jito_teacher)
                        subability = Subject(name='MentalAbilityIITJEE11',student =
                                           stu,teacher=jito_teacher)
                        subintelligence = Subject(name='General-Intelligence',student =
                                           stu,teacher=jito_teacher)



                    elif str(kl) == str(12):
                        submaths = Subject(name='MathsIITJEE12',student =
                                           stu,teacher=jito_teacher)
                        submaths = Subject(name='MathsIITJEE12',student =
                                           stu,teacher=jito_teacher)
                        subphy = Subject(name='PhysicsIITJEE12',student =
                                           stu,teacher=jito_teacher)
                        subchem = Subject(name='ChemistryIITJEE12',student =
                                           stu,teacher=jito_teacher)
                        subability = Subject(name='MentalAbilityIITJEE12',student =
                                           stu,teacher=jito_teacher)
                        subintelligence = Subject(name='General-Intelligence',student =
                                           stu,teacher=jito_teacher)


                    submaths.save()
                    subphy.save()
                    subchem.save()
                    subability.save()
                    subintelligence.save()


                    print(fullName,fatherName,kl,phone,address)
                    return HttpResponseRedirect(reverse('basic:home'))
                else:
                    context = {'form':form}
                    return\
                render(request,'basicinformation/student_information.html',context)
            else:
                form = StudentInformationForm()
                context = {'form':form}
                return render(request,'basicinformation/student_information.html',context)


def studentInformation(request):
    user = request.user
    if user.is_authenticated:
        try:
            student_information = StudentProfile.objects.get(student = user)
            return HttpResponse('hello')
        except:
            if request.POST:
                form = StudentForm(request.POST or None)
                if form.is_valid():
                    phone = form.cleaned_data['phone']
                    code = form.cleaned_data['code']
                    student_info = StudentProfile()
                    student_info.phone = phone
                    student_info.student = user
                    student_info.code = code
                    student_info.save()
                    confirmation = StudentConfirmation()
                    confirmation.student = user
                    if code.lower() == "siel":
                        school = School.objects.get(name = "SIEL")
                        confirmation.school = school
                        confirmation.name = user.first_name
                        confirmation.phone = phone
                        confirmation.save()
                        mail_at =\
                        signup_mail.delay(user.email,user.first_name,institute='SIEL')
                    elif code.lower() == "jen":
                        school = School.objects.get(name="JEN")
                        confirmation.school = school
                        confirmation.name = user.first_name
                        confirmation.phone = phone
                        confirmation.save()
                        mail_at =\
                        signup_mail.delay(user.email,user.first_name,institute='JEN')
                    else:
                        return HttpResponseRedirect(reverse('basic:home'))
                    logout(request)

                    return\
                render(request,'basicinformation/confirmation_student.html')
                else:
                    context = {'form':form}
                    return\
                render(request,'basicinformation/student_info.html',context)
            else:
                form = StudentForm()
                context = {'form':form}
                return render(request,'basicinformation/student_info.html',context)

    else:
        return HttpResponseRedirect(reverse('basic:home'))

def teacher_student_confirmation(request):
    user = request.user
    if user.is_authenticated:
        me = Teach(user)
        confirmations = StudentConfirmation.objects.filter(school =
                                                           me.profile.school,confirm=None)
        batches = klass.objects.filter(school=me.profile.school)
        context = {'confirmations':confirmations,'batches':batches}
        return\
    render(request,'basicinformation/confirmation_teacher.html',context)
    else:
        return HttpResponseRedirect(reverse('basic:home'))
def teacher_confirmation(request):
    if 'batchChoice' in request.POST:
        me = Teach(request.user)
        batch_id = request.POST['batchChoice']
        confirmation_id = request.POST['confirmationId']
        batch = klass.objects.get(id = batch_id)
        confirmation = StudentConfirmation.objects.get(id = confirmation_id)
        confirmation.batch = batch
        #confirmation.teacher = me.profile
        confirmation.confirm = True
        confirmation.save()
        try:
            stud = Student(studentuser = confirmation.student,klass = batch,name =
                           confirmation.student.first_name,school =
                           confirmation.school)
            stud.save()
        except:
            return HttpResponse('Either student is already registered or there\
                                was some error.')
        print('in locopilit {}'.format(str(confirmation.school).strip()))
        if confirmation.school == "SIEL":
            subenglish = Subject(name='English',student = stud,teacher =
                             me.profile)
            subenglish.save()
        elif str(confirmation.school).strip() == "JEN":
            if batch.name == 'RailwayGroupD':
                subGenInte = Subject(name="General-Intelligence",student=stud,teacher=me.profile)
                subGenInte.save()
                subMaths = Subject(name="Quantitative-Analysis",student=stud,teacher=me.profile)
                subGenKnow = Subject(name="General-Knowledge",student=stud,teacher=me.profile)
                subGenSci = Subject(name="General-Science",student=stud,teacher=me.profile)
                subMaths.save()
                subGenSci.save()
                subGenKnow.save()

            if batch.name == 'LocoPilot':
                subGenInte = Subject(name="General-Intelligence",student=stud,teacher=me.profile)
                subGenInte.save()
                subMaths = Subject(name="Quantitative-Analysis",student=stud,teacher=me.profile)
                subEnglish = Subject(name="English",student=stud,teacher=me.profile)
                subGenKnow = Subject(name="General-Knowledge",student=stud,teacher=me.profile)
                subGenSci = Subject(name="General-Science",student=stud,teacher=me.profile)
                subMaths.save()
                subEnglish.save()
                subGenSci.save()
                subGenKnow.save()

                subLocoPilot = Subject(name="ElectricalLocoPilot",student=stud,teacher=me.profile)
                subLocoPilot.save()
            if batch.name == 'SSC':
                subGenInte = Subject(name="General-Intelligence",student=stud,teacher=me.profile)
                subGenInte.save()
                subMaths = Subject(name="Quantitative-Analysis",student=stud,teacher=me.profile)
                subEnglish = Subject(name="English",student=stud,teacher=me.profile)
                subGenKnow = Subject(name="General-Knowledge",student=stud,teacher=me.profile)
                subGenSci = Subject(name="General-Science",student=stud,teacher=me.profile)
                subMaths.save()
                subGenSci.save()
                subEnglish.save()
                subGenKnow.save()


            print('subLocoPilot_saved')
        elif str(confirmation.school).strip() == "YSM":
            print('creating subject for YSM coaching')
            subGenInte = Subject(name="General-Intelligence",student=stud,teacher=me.profile)
            subGenInte.save()
            subMaths = Subject(name="Quantitative-Analysis",student=stud,teacher=me.profile)
            subEnglish = Subject(name="English",student=stud,teacher=me.profile)
            subGenKnow = Subject(name="General-Knowledge",student=stud,teacher=me.profile)
            subGenSci = Subject(name="General-Science",student=stud,teacher=me.profile)
            subGenSci.save()
            subMaths.save()
            subEnglish.save()
            subGenKnow.save()
            print('4 subjects saved')
        elif str(confirmation.school).strip() == "OJAS":
            print('creating subject for OJAS coaching')
            subMaths = Subject(name="Quantitative-Analysis",student=stud,teacher=me.profile)
            subMaths.save()
            print('math subjects saved')


        return HttpResponseRedirect(reverse('basic:addStudents'))

    else:
        return HttpResponse('Please choose a batch for student')


@ensure_csrf_cookie
def home(request):
    user = request.user
    if user.is_authenticated:
        # if user is from management this code fires up
        if user.groups.filter(name='Management').exists():
            all_students = Student.objects.filter(school =
                                                  user.schoolmanagement.school)
            all_teachers =\
            Teacher.objects.filter(school=user.schoolmanagement.school)
            klasses = klass.objects.filter(school=user.schoolmanagement.school)
            test_teachers ={}
            for te in all_teachers:
                all_tests = SSCKlassTest.objects.filter(creator =
                                                        te.teacheruser)
                test_teachers[te] = {all_tests}
            new_test_teachers = {}
            new_test_teachers = {}
            for key,value in test_teachers.items():
                n_tests = []
                for qs in value:
                    for te in qs:
                        if te.published <=\
                        datetime.strptime('2018-01-27','%Y-%m-%d').date():
                            pass
                        else:
                            n_tests.append(te)
                    new_test_teachers[key] = {'test':n_tests}


            context =\
                    {'students':all_students,'teachers':all_teachers,'all_classes':klasses,'tests_created':new_test_teachers}
            return render(request,'basicinformation/managementHomePage.html',context)
        if user.is_staff:
            print('yes i am in user staff')
            #sheet_links =\
            #['age.csv','alligations.csv','average.csv','boat_and_stream.csv','discount.csv','fraction.csv','lcm_lcf.csv','number_system.csv','percentage.csv','pipe_cistern.csv','ratio_proportions.csv','simple_compound_interest.csv','simplification.csv','speed_distance.csv','square_cube_roots.csv','surds.csv','time_work.csv','train.csv','volume.csv',]
            sheet_links = \
                    ['reasoningremain.csv']

            #student_user = User.objects.get(username = 'prashant_pandey')
            #student = Student.objects.get(studentuser = student_user)
            #weak_area = StudentWeakAreasChapterCache.objects.filter(student
            #                                                        =student)
            #recommendation_list = []        
            #for wa in weak_area:
            #    sub = wa.subject
            #    chap = wa.chapter
            #    print(sub,chap)
            #    try:
            #        subject_chapter = SubjectChapters.objects.get(subject =
            #                                                  sub,code =
            #                                                  float(chap))
            #        chap_name = subject_chapter.name
            #        try:
            #            youtube_video = YoutubeExternalVideos.objects.filter(subject =
            #                                                          sub,chapter =                   
            #                                                          chap_name)                      
            #            for num,yv in enumerate(youtube_video):
            #                if num == 2:
            #                    break

            #                recommendation_dict = \
            #                    {'link':yv.link,'title':yv.title,'chapter':chap_name,'subject':sub}
            #                recommendation_list.append(recommendation_dict)
            #        except Exception as e:          
            #            print(str(e))
            #    except Exception as e:
            #        print(str(e))
            #print(recommendation_list)




            #sub = 'English'
            #chap = SubjectChapters.objects.filter(subject = sub)
            #chapters = []
            #for i in chap:
            #    chapters.append(i.name)
            #try:
            #    for i in chapters:
            #        get_youtube_videos(sub,i)
            #except Exception as e:
            #    print(str(e))
            #add_jobs.delay('/home/prashant/Desktop/programming/projects/bodhiai/bodhiai/scraped/pickles/freejobs.pickle')
            #delete_questions.delay('/app/scraped/pickles/freejobs.pickle')
            #fill_taken_subjects.delay()
            #create_timing_cache_detail.delay()
            #start_caching_prgress.delay()
            #create_Subject_topics.delay(sheet_links)
            #delete_timing_cache.delay()
            #cache = StudentAverageTimingDetailCache.objects.all()
            #print('{} len of cache'.format(cache))
            #for i in cache:
            #    i.delete()
            #    print('i deleted')

            #create_timing_cache_detail.delay()
            #sheet_links2 = \
            #        ['1f.csv']
            #adding_quest =\
            #allquestions_institute.delay('Quantitative-Analysis',"JEN")
            #delete_repeat_questions.delay()
            #delete_nan_text.delay()
            #delete_questions.delay()
            #delete_directions.delay()
            #add_to_database_questions.delay(sheet_links,'BodhiAI',production=True,onlyImage=True)
            #add_new_subject_student('Engineering-Drawing')
            #add_new_subject_student('Environment-Study')
            #add_new_subject_student('Basic-Science')
            #students = Student.objects.filter(school__name = "JEN")
            #jen_teacher = Teacher.objects.get(school__name = "JEN")
            #for stud in students:
            #    add_subjects_new.delay("PhysicsIITJEE11",stud.id,jen_teacher.id)
            #add_png.delay()
            #school_name = 'JEN'
            #batch = 'LocoPilot'
            #school = School.objects.get(name=school_name)
            #teacher = Teacher.objects.get(school=school)
            #addsubjects.delay(school_name,batch,teacher.name)
            #add_questions('JEN','ElectricalLocoPilot')
            #quest_added = add_to_database_questions.delay(sheet_links,'Swami Reasoning World',onlyImage=True,production =\
            #                          True)

            #def add_to_database_questions(sheet_link,extra_info=False,production=False,onlyImage =
            #                  False,fiveOptions=False,explanation_quest=False):

            #add_questions.delay('Competition_Qualifiers','English')
            #add_questions.delay('JEN','Engineering-Drawing')
            #add_questions.delay('JEN','Environment-Study')
            #add_questions.delay('YSM','Quantitative-Aptitude')
            #add_questions.delay('YSM','General-Knowledge')
            #add_questions('Aravali Defence Academy','GroupX-Maths')
            #add_questions('Aravali Defence Academy','Defence-Physics')
            #add_questions('Aravali Defence Academy','Defence-English')
            #add_questions('Aravali Defence Academy','Defence-GK-CA')
            #add_questions('KR Defence Coaching','Defence-English')
            #add_questions('KR Defence Coaching','Defence-Physics')
            #add_questions('KR Defence Coaching','GroupX-Maths')
            #add_student_subject('Colonel Defence Academy','Defence-Physics',None,allTeacers=True)
            
            #questions = SSCquestions.objects.filter(section_category = 'GroupX-English')
            #print(len(questions))
            # add cache weak areas to all students and subjects
            #caches = StudentWeakAreasChapterCache.objects.all()
            #for i in caches:
            #    i.delete()
            #    print('deleted')
            #students = Student.objects.all().order_by('id')[:1000]
            #for stud in students:
            #    subjects = stud.subject_set.all()
            #    for sub in subjects:
            #        chapters = get_chapters(sub)
            #        for chap in chapters:
            #            createProgressCache.delay(stud.id,sub,chap)
            #subject_chapters = SubjectChapters.objects.all()
            #course_cgl = Course.objects.get(course_name='SSC CGL')
            #course_je = Course.objects.get(course_name='SSC JE')
            #for sc in subject_chapters:
            #    if 'General-Intelligence' or 'Quantitative-Analysis' or\
            #    'English' or 'General-Knowledge' == sc.subject:
            #        sc.course.add(course_cgl)
            #        sc.course.add(course_je)
            #        print('course added in specified subject')
            #    else:
            #        sc.course.add(course_je)
            #        print('course added')
            #delete_duplicate_marks.delay()
            #automatic_test_creation.delay('Chemistry_NEET',10)
            #create_fake_users()
            #create_fake_users.delay()
            #fakes_users_test.delay()
            #delete_chapter_ranking.delay()
            add_to_database_questions.delay(sheet_links,'BodhiAI',production=True,onlyImage=True)
            #replicate_questions_course()
            #edit_wrong_question(sheet_links)
            #delete_allQuestions.delay("BodhiAI")
            return HttpResponse('done')

        if user.groups.filter(name='Students').exists():
            #storage = messages.get_messages(request)
            me = Studs(request.user)
            deleteBadTests.delay()
            teacher_user = Teacher.objects.get(school__name = me.school)
            me.studentOldTests(teacher_user)

            ## if B2C customer then add tests  to profile
            #if me.profile.school.name == 'BodhiAI':
            #    # checks if test is legitimate, if not then delete the test
            #    bad_tests = SSCKlassTest.objects.filter(Q(sub='')| Q(totalTime
            #                                                        = 0))
            #    if bad_tests:
            #        try:
            #            for i in bad_tests:
            #                i.delete()
            #        except Exception as e:
            #            print(str(e))
            #    
            #    me.subjects_OnlineTest()
            #elif profile.school.name == 'JITO':
            #    me.subjects_OnlineTest(schoolName = 'JITO',klas =me.profile.klass)

            ##subjects = user.student.subject_set.all()

            ## gets marks of all the tests taken by student to be displayed on home page
            ##subject_marks = me.test_information(subjects)

           ## get new tests to take (practise tests on the student page) 
            ##new_tests = me.toTake_Tests(6)

            ## sending all values to template based on type of student
            ##if me.profile.school.name == "BodhiAI":
            ##    context = \
            ##            {'subjects':subjects,'subjectwiseMarks':subject_marks,'newTests':new_tests}
            ##else:
            ##    context = \
            ##        {'subjects':subjects,'subjectwiseMarks':subject_marks,'newTests':new_tests}

            return render(request, 'basicinformation/student_home_page.html')


        elif user.groups.filter(name='Teachers').exists():
            #ai_tukka_questions.delay(user.id)
            #ai_sharedTask.delay(user.id)
            me = Teach(user)
            profile = user.teacher
            #marks = SSCOnlineMarks.objects.filter(test__creator= user)
            #questions = []

            #for mark in marks:
            #    for chid in mark.rightAnswers:
            #        question = SSCquestions.objects.get(choices__id = chid)
            #        questions.append(question.id)
            #    for chid in mark.wrongAnswers:
            #        question = SSCquestions.objects.get(choices__id = chid)
            #        questions.append(question.id)
            #    for quid in mark.skippedAnswers:
            #        questions.append(quid)

            #unique,counts = np.unique(questions,return_counts=True)
            #cat_quests = np.asarray((unique,counts)).T
            #right_answers = []
            #wrong_answers = []
            #skipped_answers = []
            #for i,j in cat_quests:
            #    right = 0
            #    wrong = 0
            #    skipped = 0
            #    qu = SSCOnlineMarks.objects.filter(test__creator = user)
            #    for ma in qu:
            #        for chid in ma.rightAnswers:
            #            quest_obj = SSCquestions.objects.get(choices__id = chid)
            #            quid = quest_obj.id
            #            if i == quid:
            #                right = right + 1
            #        for chid in ma.wrongAnswers:
            #            quest_obj = SSCquestions.objects.get(choices__id = chid)
            #            quid = quest_obj.id
            #            if i == quid:
            #                wrong = wrong + 1
            #        if i in ma.skippedAnswers:
            #            skipped = skipped + 1
            #    right_answers.append(right)
            #    wrong_answers.append(wrong)
            #    skipped_answers.append(skipped)
            #overall =\
            #list(zip(cat_quests,right_answers,wrong_answers,skipped_answers))
            #overall = np.array(overall)
            #df = pd.DataFrame(overall)
            #df.to_csv("questions.csv")


            subjects = Teacher_Classes.delay(user.id)
            weak_subs_areas_dict = []
            teach_klass = TeacherClasses.objects.filter(teacher=me.profile)
            klasses = []
            if len(teach_klass) != 0:
                for kl in teach_klass:
                    klasses.append(kl.klass)
            else:
                klasses = me.my_classes_names()
                try:
                    for kl in klasses:
                        new_teach_klass = TeacherClasses()
                        new_teach_klass.teacher = me.profile
                        new_teach_klass.klass = kl
                        new_teach_klass.numStudents = 0
                        new_teach_klass.save()
                except:
                    klasses = []


            #weak_ar = teacher_home_weak_areas.delay(user.id)
            #weak_ar = teacher_home_weak_areas(user.id)
            #print(weak_ar)
            #te_id = weak_ar.task_id
            #res = AsyncResult(te_id)

            #klasses,subjects = res.get()
            
            #weak_links = {}
            #weak_klass = []
            #weak_subs = []
            #subs = []
            #try:
            #    for sub in subjects:
            #        for i in klasses:
            #            try:
            #                print('%s this is i' %i)
            #                weak_links[i]= \
            #                me.online_problematicAreasNames(user,sub,i)
            #                kk = me.online_problematicAreasNames(user,sub,i)
            #                weak_subs.append(weak_links[i])

            #                weak_klass.append(i)
            #                subs.append(sub)


            #                #print(weak_links)
            #                #print(weak_subs)
            #            except Exception as e:
            #                print(str(e))
            #    weak_subs_areas = list(zip(subs,weak_klass,weak_subs))
            #    #weak_subs_areas = None
            #except:
            #    weak_subs_areas = None

            #num_klasses = len(klasses)
            #weak_subs_areas = list(zip(subs,weak_klass,weak_subs_areas))
            #print('This is the weak areas %s' %weak_subs_areas)
            #num_subjects = len(subjects)
            teacherName = me.profile
            context = {'profile': profile,
                       'klasses': klasses,
                       'isTeacher': True,'teacherName':teacherName}
            #return render(request, 'basicinformation/teacher1.html', context)
            return render(request, 'basicinformation/home_overview.html', context)
        else:

            return render(request, 'basicinformation/home.html')
    else:
        return HttpResponseRedirect(reverse('membership:login'))


# gets tests of selected topic by the student on home page

def student_select_topicTest(request):
    user = request.user
    if user.is_authenticated:
        if 'topicwisetest' in request.GET:
            topic = request.GET['topicwisetest']
            me = Studs(user)
            new_tests = me.toTake_Tests(0,allTests=True)
            topic_tests_id = []

            for k,v in new_tests.items():
                if topic in new_tests[k]['topics']:
                    topic_tests_id.append(k)
            newer_tests = []
            for i in topic_tests_id:
                topic_test = SSCKlassTest.objects.get(id = i)
                newer_tests.append(topic_test)
            ntest = {}
            for test in newer_tests:
                all_tp = []
                count = 0
                for quest in test.sscquestions_set.all():
                    count += 1
                    cat =\
                    me.changeIndividualNames(quest.topic_category,quest.section_category)
                    all_tp.append(cat)
                all_tp_unique = list(unique_everseen(all_tp))
                ntest[test.id] =\
                {'subject':test.sub,'topics':all_tp_unique,'num_questions':count}
            context = {'newTests':ntest}
            return render(request,'basicinformation/studentInstituteTopicTests.html',context)

def student_moreTests(request):
    user = request.user
    if user.is_authenticated:
        me = Studs(user)
        new_tests = me.toTake_Tests(0,allTests = True)
        context = {'newTests':new_tests}
        return render(request,'basicinformation/studentMoreTests.html',context)


def student_self_analysis(request):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name='Teachers').exists():
            raise Http404(" This page is only meant for student to see.")
        elif user.groups.filter(name='Students').exists():
            me = Studs(user)
            if me.profile.school.name == 'BodhiAI':
                allSubjects = me.subjects_OnlineTest() 
                allSubjects = me.already_takenTests_Subjects()
            else:
                allSubjects = me.already_takenTests_Subjects()
            
            context = {'subjects': allSubjects}
            return render(request, 'basicinformation/selfStudentAnalysis.html', context)


def student_subject_analysis(request):
    user = request.user
    me = Studs(user)
    if user.is_authenticated:
        if 'studentwhichsub' in request.GET:
            which_sub = request.GET['studentwhichsub']
            ana_type = ['Institute Tests', 'Online Tests']
            context = {'anatype': ana_type, 'sub': which_sub}
            return \
                render(request, 'basicinformation/student_analysis_subjects.html', context)
        if 'studentwhichana' in request.GET:
            which_one = request.GET['studentwhichana']
            mode = which_one.split(',')[1]
            sub = which_one.split(',')[0]
            subject = sub

            if mode == 'online':
                tests = SSCOnlineMarks.objects.filter(test__sub=subject,
                                                          student=me.profile).order_by('test__published')

                context = {'tests': tests,'subject':subject}
                return \
                    render(request, 'basicinformation/student_self_sub_tests.html', context)
            elif mode == 'offline':
                tests = SSCOfflineMarks.objects.filter(test__sub=subject,
                                                           student=me.profile)
                context = {'tests': tests,'subject':subject}
                return \
                    render(request, 'basicinformation/student_self_sub_tests.html', context)

        if 'studentTestid' in request.GET:
            idandsubject = request.GET['studentTestid']
            test_id = idandsubject.split(',')[0]
            #visible_tests(test_id)
            sub = idandsubject.split(',')[1]
            try:
                test = SSCOfflineMarks.objects.get(student=me.profile, test__id=test_id)
                mode = 'offline'
            except:
                test = SSCOnlineMarks.objects.get(student=me.profile, test__id=test_id)
                te = SSCKlassTest.objects.get(id = test_id)
                mode = 'online'

            student_type = 'SSC'
            if mode == 'online':
# Look for a cached test analyis , if found then show it 
# if there is a change in number of tests then just update a few things and
# show it
# If cache not found then calculate the fields, create a cached version and
# show it on front end.
                try:
                    te = SSCKlassTest.objects.get(id = test_id)
                    analysis = StudentTestAnalysis.objects.get(student =
                                                                  me.profile,test
                                                                  =te)
                    myPercent = analysis.myPercent
                    classAverage = analysis.klassAverage
                    classAveragePercent = analysis.klassAveragePercent
                    myPercentile = analysis.myPercentile
                    allKlassMarks = analysis.allKlassMarks
                    freqAnswerId = analysis.freqAnswerId
                    freqAnswer = analysis.freqAnswer
                    freq = list(zip(freqAnswerId,freqAnswer))
                    weakCategories = analysis.weakCategories
                    weakAccuracies = analysis.weakAccuracies
                    weak_areas = list(zip(weakCategories,weakAccuracies))
                    numRight = analysis.numRight
                    numWrong = analysis.numWrong
                    numSkipped = analysis.numSkipped
                    overallAccuracy = analysis.overallAccuracy
                    subjectwiseAccuracySub = analysis.subjectwiseAccuracySub
                    subjectwiseAccuracy = analysis.subjectwiseAccuracy
                    subjectwise_acc =\
                    list(zip(subjectwiseAccuracySub,subjectwiseAccuracy))
                    areaTimeCategory = analysis.areaTimeCategory
                    areaTime = analysis.areaTime
                    area_timing = list(zip(areaTimeCategory,areaTime))
                    hours = analysis.hour
                    mins = analysis.minute
                    seconds = analysis.second
                    if hours == 0:
                        tt = '{} minutes and {} seconds'.format(mins,seconds)
                    if hours == 0 and mins == 0:
                        tt = '{} seconds'.format(seconds)
                    if hours > 0:
                        tt = '{} hours {} minutes and {}\
                        seconds'.format(hours,mins,seconds)

                    if sub == 'SSCMultipleSections':
                        weak_names = weak_areas
                        timing = area_timing
                    else:
                        weak_names = me.changeTopicNumbersNames(weak_areas,sub)
                        timing = me.changeTopicNumbersNames(area_timing,sub)
                    if len(tests) != len(allKlassMarks):
                        percentile, all_marks = me.online_findPercentile(test_id)
                        average, percent_average = \
                            me.online_findAverageofTest(test_id, percent='p')
                        percentile = percentile * 100
                        all_marks = [((i / test.test.max_marks) * 100) for i in all_marks]
                        analysis.myPercentile = percentile
                        analysis.allKlassMarks = all_marks
                        analysis.klassAverage = average
                        analysis.klassAveragePercent = percent_average
                        analysis.save()
                        allKlassMarks = all_marks
                        myPercentile = percentile
                        classAverage = average
                        classAveragePercent = percent_average

                    context = \
                        {'test': test, 'average': classAverage,
                         'percentAverage': classAveragePercent,
                         'my_percent': myPercent, 'percentile': myPercentile,
                         'allMarks': allKlassMarks,
                         'freq':\
                         freq,'student_type':student_type,'topicWeakness':weak_names,'topicTiming':timing,
                         'numberRight':numRight,'numberWrong':numWrong,'numberSkipped':numSkipped,'accuracy':overallAccuracy,'subjectwise_accuracy':subjectwise_acc,'tt':tt}
                    return \
                        render(request, 'basicinformation/student_analyze_test.html', context)




                except Exception as e:
                    print(str(e))
                    analysis = StudentTestAnalysis()
                    my_marks_percent = (test.marks / test.test.max_marks) * 100
                    analysis.myPercent = my_marks_percent
                    average, percent_average = \
                        me.online_findAverageofTest(test_id, percent='p')
                    analysis.klassAverage = average
                    analysis.klassAveragePercent = percent_average
                    percentile, all_marks = me.online_findPercentile(test_id)
                    percentile = percentile * 100
                    analysis.myPercentile = percentile

                    all_marks = [((i / test.test.max_marks) * 100) for i in all_marks]
                    analysis.allKlassMarks = all_marks

                    freq = me.online_QuestionPercentage(test_id)
                    freq_id = []
                    freq_freq = []
                    for i,j in freq:
                        freq_id.append(i)
                        freq_freq.append(j)
                    analysis.freqAnswerId = freq_id
                    analysis.freqAnswer = freq_freq
                    # converting test time seconds to hours and minutes
                    test_totalTime = test.timeTaken
                    hours = int(test_totalTime/3600)
                    t = int(test_totalTime%3600)
                    mins = int(t/60)
                    seconds =int(t%60)
                    if hours == 0:
                        tt = '{} minutes and {} seconds'.format(mins,seconds)
                        analysis.hour = 0
                        analysis.minute = mins
                        analysis.second = seconds
                    if hours == 0 and mins == 0:
                        tt = '{} seconds'.format(seconds)
                        analysis.hour = 0
                        analysis.minute = 0
                        analysis.second = seconds

                    if hours > 0:
                        tt = '{} hours {} minutes and {}\
                        seconds'.format(hours,mins,seconds)
                        analysis.hour = hours
                        analysis.minute = mins
                        analysis.second = seconds

                    try:
                        if tt:
                            pass
                    except:
                        tt = None

                    ra,wa,sp,accuracy = me.test_statistics(test_id)
                    analysis.numRight = ra
                    analysis.numWrong = wa
                    analysis.numSkipped = sp
                    analysis.overallAccuracy = accuracy
                    weak_areas = me.weakAreas_Intensity(sub,singleTest = test_id)
                    weak_cat = []
                    weak_acc = []
                    for i,j in weak_areas:
                        weak_cat.append(i)
                        weak_acc.append(j)
                    analysis.weakCategories = weak_cat
                    analysis.weakAccuracies = weak_acc
                    sk_weak = me.skipped_testwise(test_id,me.profile)
                    area_timing,freq = me.areawise_timing(sub,test_id)
                    weak_time_cat = []
                    weak_time = []
                    for k,v in area_timing:
                        weak_time_cat.append(k)
                        weak_time.append(v)
                    analysis.areaTimeCategory = weak_time_cat
                    analysis.areaTime = weak_time
                    subjectwise_accuracy = me.test_SubjectAccuracy(test_id)
                    sub_weak = []
                    sub_weak_acc = []
                    for i,j in subjectwise_accuracy.items():
                        sub_weak.append(i)
                        sub_weak_acc.append(j)
                    analysis.subjectwiseAccuracySub = sub_weak
                    analysis.subjectwiseAccuracy = sub_weak_acc
                    analysis.student = me.profile
                    analysis.test = te
                    analysis.save()

                    if sub == 'SSCMultipleSections':
                        weak_names = weak_areas
                        timing = area_timing
                    else:
                        weak_names = me.changeTopicNumbersNames(weak_areas,sub)
                        timing = me.changeTopicNumbersNames(area_timing,sub)
                    context = \
                        {'test': test, 'average': average, 'percentAverage': percent_average,
                         'my_percent': my_marks_percent, 'percentile': percentile, 'allMarks': all_marks,
                         'freq':\
                         freq,'student_type':student_type,'topicWeakness':weak_names,'topicTiming':timing,
                         'numberRight':ra,'numberWrong':wa,'numberSkipped':sp,'accuracy':accuracy,'subjectwise_accuracy':subjectwise_accuracy,'tt':tt}
                    return \
                        render(request, 'basicinformation/student_analyze_test.html', context)

        # for offline tests conducted in institute (with OMR) (no timing in
        # these)

            elif mode == 'offline':
                my_marks_percent = (test.marks / test.test.max_marks) * 100
                average, percent_average = \
                    me.offline_findAverageofTest(test_id, percent='p')
                percentile, all_marks = me.offline_findPercentile(test_id)
                percentile = percentile * 100
                all_marks = [((i / test.test.max_marks) * 100) for i in all_marks]
                freq = me.offline_QuestionPercentage(test_id)
                ra,wa,sp,accuracy = me.offline_test_statistics(test_id)
                weak_areas = me.offline_weakAreas_Intensity(sub,singleTest = test_id)
                weak_names = me.changeTopicNumbersNames(weak_areas,sub)
                subjectwise_accuracy = me.offline_test_SubjectAccuracy(test_id)
                context = \
                    {'test': test, 'average': average, 'percentAverage': percent_average,
                     'my_percent': my_marks_percent, 'percentile': percentile, 'allMarks': all_marks,
                     'freq':
                     freq,'student_type':student_type,'topicWeakness':weak_names,
                     'numberRight':ra,'numberWrong':wa,'numberSkipped':sp,'accuracy':accuracy,'subjectwise_accuracy':subjectwise_accuracy,}
                return \
                    render(request, 'basicinformation/student_analyze_test.html', context)

def student_weakAreasSubject(request):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name='Students').exists():
           me = Studs(user)
           subs = me.my_subjects_names()
           context = {'subs':subs}
           return render(request,'basicinformation/student_weakAreas_subject.html',context)


def student_weakAreas(request):
    if 'studWA' in request.GET:
        me = Studs(request.user)
        subject = request.GET['studWA']
        timing_areawise,freq_timer = me.areawise_timing(subject)
        freq_timer = me.changeTopicNumbersNames(freq_timer,subject)

        freq = me.weakAreas_IntensityAverage(subject)
        strongAreas = []
        strongFreq = []
        try:
           for i,j in freq:
                strongAreas.append(i)
                strongFreq.append(float(100-j))
        except Exception as e:
            print(str(e))
        if freq == 0:
           context = {'noMistake':'noMistake'}
           return render(request,'basicinformation/student_weakAreas.html',context)
        # changing topic categories numbers to names
        timing_areawiseNames =\
        me.changeTopicNumbersNames(timing_areawise,subject)
        freq_Names = me.changeTopicNumbersNames(freq,subject)
        skills = list(zip(strongAreas,strongFreq))
        skills_names = me.changeTopicNumbersNames(skills,subject)
        context = \
               {'freq':freq_Names,'timing':timing_areawiseNames,'time_freq':freq_timer,'skills':skills_names}
        return render(request,'basicinformation/student_weakAreas.html',context)


def student_improvement(request):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name='Students').exists():
           me = Studs(user)
           subjects = me.my_subjects_names()
           context = {'subjects':subjects}
           return \
       render(request,'basicinformation/student_improvement1.html',context)

def student_improvement_sub(request):
    user = request.user
    if 'improvementSub' in request.GET:
        sub = request.GET['improvementSub']
        me = Studs(user)
        overall = me.section_improvement(sub)
        if overall == 0:
            context = {'overall':None}
        else:
            context = {'overall':overall,}
        return\
    render(request,'basicinformation/student_improvement2.html',context)







# teacher analysis methods

def current_analysis(request, grade):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name='Students').exists():
            raise Http404("You don't have the permissions to view this page.")
        elif user.groups.filter(name='Teachers').exists():

            klass_dict, all_klasses = teacher_get_students_classwise(request)

            klass_test1_dict, klass_test2_dict, klass_test3_dict = teacher_get_testmarks_classwise(request, klass_dict)
            # find out the average of class tests (all the classes separated by commas)

            av1 = []  # list to hold the averages of test1
            av2 = []
            av3 = []
            for i in klass_test1_dict.values():
                av_test1 = averageoftest(i)
                av1.append(av_test1)

            for i in klass_test2_dict.values():
                av_test2 = averageoftest(i)
                av2.append(av_test2)

            for i in klass_test3_dict.values():
                av_test3 = averageoftest(i)
                av3.append(av_test3)

            context = {'avtest1': av1, 'avtest2': av2, 'avtest3': av3, 'klass_dict': klass_dict}

            return render(request, 'basicinformation/analysis_current.html',
                          context)
    else:
        raise Http404("You don't have the permissions to view this page.")

def teacher_weakAreasinDetail(request):
    user = request.user
    if user.is_authenticated:
        if 'weakAreasButton' in request.GET:
            which_class = request.GET['weakAreasClass']
            which_sub = request.GET['weakAreasSub']
            print(which_class,which_sub)
            me = Teach(user)
            res = \
            me.online_problematicAreaswithIntensityAverage(user,which_sub,which_class)
            res = me.change_topicNumbersNamesWeakAreas(res,which_sub)
            timing,freq_timing = me.weakAreas_timing(user,which_sub,which_class)
            timing = me.change_topicNumbersNamesWeakAreas(timing,which_sub)
            context =\
            {'which_class':which_class,'probAreas':res,'timing':timing}
            #context =\
            #{'which_class':which_class,'probAreas':res}

            return render(request,'basicinformation/teacher_weakAreasinDetail.html',context)


def teacher_home_page(request):
    user = request.user
    me = Teach(user)
    if user.is_authenticated:
        if user.groups.filter(name='Teachers').exists():
            #klass_dict, all_klasses = teacher_get_students_classwise(request)
            #all_klasses = me.my_classes_names()
            #klasses = TeacherClasses.objects.filter(teacher=me.profile)
            #all_klasses = []
            #for ak in klasses:
            #    all_klasses.append(ak.klass)
            all_klasses = me.my_classes_names_cache()
            context = {'klasses': all_klasses}
            return render(request, 'basicinformation/teacherHomePage.html', context)
        else:
            raise Http404("You don't have the permissions to view this page.")
    else:
        raise Http404("You don't have the permissions to view this page.")


def teacher_update_page(request):
    user = request.user
    #institution = profile.school.category
    #klass_dict, all_klasses = teacher_get_students_classwise(request)
    me = Teach(user)
    if 'ajKlass' in request.GET:
        return HttpResponse('Choose from Above')
    elif 'schoolTestAnalysis' in request.GET:
        which_klass = request.GET['schoolTestAnalysis']
        which_class = which_klass.split(',')[0]
        subjects = me.my_subjects_names()
        context = {'subjects': subjects, 'which_class': which_class}
        return \
            render(request, 'basicinformation/teacher_school_analysis1.html', context)
    elif 'schoolSubject' in request.GET:
        schoolSubject = request.GET['schoolSubject']
        sub = schoolSubject.split(',')[0]
        which_class = schoolSubject.split(',')[1]
        offline_tests = SSCKlassTest.objects.filter(sub =
                                                    sub,mode='BodhiSchool')
        context = {'Tests':offline_tests}
        return \
    render(request,'basicinformation/teacher_school_analysis2.html',context)

    elif 'schoolTestid' in request.GET:
        test_class = request.GET['schoolTestid']
        test_id = test_class.split(',')[0]
        which_class = test_class.split(',')[1]
        offline_marks = SSCOfflineMarks.objects.filter(test__id=test_id)
        test = SSCKlassTest.objects.get(id = test_id)
        problem_quests = me.offline_problematicAreasperTest(test_id)
        max_marks = 0
        for i in offline_marks:
            max_marks = i.test.max_marks
        average,percent_average =\
        me.offline_findAverageofTest(test_id,percent='p')
        grade_s,grade_a,grade_b,grade_c,grade_d,grade_e,grade_f= \
        me.online_freqeucyGrades(test_id,mode='offline')
        freq = me.offline_QuestionPercentage(test_id)
        result = me.generate_rankTable(test_id,mode='offline')
        try:
            result = result[result[:,3].argsort()]
        except:
            result = None
        sq = me.online_skippedQuestions(test_id,mode='offline')
        context = {'om': offline_marks,'test':test,'average':average
                   ,'percentAverage':percent_average,'maxMarks':max_marks,
                   'grade_s':grade_s,'grade_a':grade_a,'grade_b':grade_b,'grade_c':grade_c,
                   'grade_d':grade_d,'grade_e':grade_e,'grade_f':grade_f,
                   'freq':freq,'sq':sq,'problem_quests':problem_quests,'ssc':True,'result':result}
        return render(request, 'basicinformation/teacher_school_analysis3.html', context)

    elif 'onlineTestAnalysis' in request.GET:
        which_klass = request.GET['onlineTestAnalysis']
        sub = bring_teacher_subjects_analysis.delay(user.id)
        te_id = sub.task_id
        res = AsyncResult(te_id)
        subs = res.get()
        context = {'subs': subs, 'which_class': which_klass}
        return \
            render(request, 'basicinformation/teacher_online_analysis.html', context)

    elif 'onlineschoolSubject' in request.GET:
        onlineSubject = request.GET['onlineschoolSubject']
        sub = onlineSubject.split(',')[0]
        which_class = onlineSubject.split(',')[1]
        trt = teacher_return_tests.delay(user.id,sub,which_class)
        te_id = trt.task_id
        res = AsyncResult(te_id)
        tests = res.get()
        o_tests = []
        for te in serializers.deserialize('json',tests):
            o_tests.append(te.object)
        context = {'tests': o_tests}
        return render(request, 'basicinformation/teacher_online_analysis2.html', context)

    elif 'onlinetestid' in request.GET:
        test_id = request.GET['onlinetestid']
        me = Teach(user)
        # get the number of students who took test
        online_marks =\
        SSCOnlineMarks.objects.filter(test__id=test_id,student__school =
                                      me.profile.school)
    # try to get result table associated with particular test
        try:
            result = TestRankTable.objects.get(test__id = test_id)
            print('at 885')
    # if no new student has taken the test then simply sort the old rank table 
            if len(result.names) == len(online_marks):
                result = me.combine_rankTable(result)
                print('at 889')

    # else generate new rank table, sort it and display it 
            else:
                asyn_rt = generate_testRankTable.delay(user.id,test_id)
                result = 'None'
                print('at 895')
                while result is 'None':
                    print('at 897')
                    try:
                        result = TestRankTable.objects.filter(test__id =\
                                                      test_id).order_by('-time')[0]
                        result = combine_rankTable(result)

                    except :
                        pass
    # if no result table is found associated to particular test then generate
    # new rank table, sort it and display it

        except:
            asyn_rt = generate_testRankTable.delay(user.id,test_id)
            result = 'None'
            while result is 'None':
                try:
                    result = TestRankTable.objects.filter(test__id =\
                                                  test_id).order_by('-time')[0]
                    result = me.combine_rankTable(result)
                except: pass

    # try if result loader exists for the given test
    # in case of except
        # if result_loader doesn't exist then-
    # case 1 : teacher is clicking on the analysis for this test for 1st time
    #   hence, create a new result loader with this test
    #   and show it in the template

        try:
            result_loader = SscTeacherTestResultLoader.objects.get(test__id = test_id)
        except:

            new_rl = teacher_test_analysis_new.delay(test_id,user.id)
            te_id = new_rl.task_id
            res = AsyncResult(te_id)
            new_rl = None
            while new_rl is None:
                try:
                    new_rl = SscTeacherTestResultLoader.objects.get(test__id = test_id)
                except SscTeacherTestResultLoader.DoesNotExist:
                    pass
            max_marks = new_rl.test.max_marks    
            average = new_rl.average
            percent_average = new_rl.percentAverage
            grade_s = new_rl.grade_s
            grade_a = new_rl.grade_a
            grade_b = new_rl.grade_b
            grade_c = new_rl.grade_c
            grade_d = new_rl.grade_d
            grade_e = new_rl.grade_e
            grade_f = new_rl.grade_f
            skipped_quests = new_rl.skipped
            skipped_freq = new_rl.skippedFreq
            sq = list(zip(skipped_quests,skipped_freq))
            freqQuests = new_rl.freqAnswersQuestions
            freqQuestsfreq = new_rl.freqAnswersFreq
            freq = list(zip(freqQuests,freqQuestsfreq))
            pro_quests = new_rl.problemQuestions
            pro_freq  = new_rl.problemQuestionsFreq
            problem_quests = list(zip(pro_quests,pro_freq))

            context = {'om':
                       online_marks,'test':new_rl.test,'average':new_rl.average
                       ,'percentAverage':new_rl.percentAverage,'maxMarks':max_marks,
                       'grade_s':new_rl.grade_s,'grade_a':new_rl.grade_a,'grade_b':new_rl.grade_b,'grade_c':new_rl.grade_c,
                       'grade_d':new_rl.grade_d,'grade_e':new_rl.grade_e,'grade_f':new_rl.grade_f,
                       'freq':freq,'sq':sq,'problem_quests':problem_quests,'ssc':True,'result':result}
            return render(request, 'basicinformation/teacher_online_analysis3.html', context)

# result loader is found but don't know if more students have taken
# the test, hence compare number of students in result loader with number of
# online marks calculated above 

        saved_marks = result_loader.onlineMarks.all()
        if len(online_marks) == len(saved_marks):
# case 2 : if no new student has taken the test then just load and display
# result_loder
            max_marks = result_loader.test.max_marks    
            pro_quests = result_loader.problemQuestions
            pro_freq  = result_loader.problemQuestionsFreq
            average = result_loader.average
            percent_average = result_loader.percentAverage
            problem_quests = list(zip(pro_quests,pro_freq))
            grade_s = result_loader.grade_s
            grade_a = result_loader.grade_a
            grade_b = result_loader.grade_b
            grade_c = result_loader.grade_c
            grade_d = result_loader.grade_d
            grade_e = result_loader.grade_e
            grade_f = result_loader.grade_f
            skipped_quests = result_loader.skipped
            skipped_freq = result_loader.skippedFreq
            sq = list(zip(skipped_quests,skipped_freq))
            freqQuests = result_loader.freqAnswersQuestions
            freqQuestsfreq = result_loader.freqAnswersFreq
            freq = list(zip(freqQuests,freqQuestsfreq))
            context = {'om':
                       online_marks,'test':result_loader.test,'average':result_loader.average
                       ,'percentAverage':result_loader.percentAverage,'maxMarks':max_marks,
                       'grade_s':result_loader.grade_s,'grade_a':result_loader.grade_a,'grade_b':result_loader.grade_b,'grade_c':result_loader.grade_c,
                       'grade_d':result_loader.grade_d,'grade_e':result_loader.grade_e,'grade_f':result_loader.grade_f,
                       'freq':freq,'sq':sq,'problem_quests':problem_quests,'ssc':True,'result':result}
            return render(request, 'basicinformation/teacher_online_analysis3.html', context)
# case 3 : if more students have taken the test then result_loader has to be
# updated and then displyed in the template
        else:
            new_rl = teacher_test_analysis_already.delay(test_id,user.id)
            rl_id = new_rl.task_id
            max_marks = result_loader.test.max_marks    
            pro_quests = result_loader.problemQuestions
            pro_freq  = result_loader.problemQuestionsFreq
            average = result_loader.average
            percent_average = result_loader.percentAverage
            problem_quests = list(zip(pro_quests,pro_freq))
            grade_s = result_loader.grade_s
            grade_a = result_loader.grade_a
            grade_b = result_loader.grade_b
            grade_c = result_loader.grade_c
            grade_d = result_loader.grade_d
            grade_e = result_loader.grade_e
            grade_f = result_loader.grade_f
            skipped_quests = result_loader.skipped
            skipped_freq = result_loader.skippedFreq
            sq = list(zip(skipped_quests,skipped_freq))
            freqQuests = result_loader.freqAnswersQuestions
            freqQuestsfreq = result_loader.freqAnswersFreq
            freq = list(zip(freqQuests,freqQuestsfreq))
            context = {'om':
                       online_marks,'test':result_loader.test,'average':result_loader.average
                       ,'percentAverage':result_loader.percentAverage,'maxMarks':max_marks,
                       'grade_s':result_loader.grade_s,'grade_a':result_loader.grade_a,'grade_b':result_loader.grade_b,'grade_c':result_loader.grade_c,
                       'grade_d':result_loader.grade_d,'grade_e':result_loader.grade_e,'grade_f':result_loader.grade_f,
                       'freq':freq,'sq':sq,'problem_quests':problem_quests,'ssc':True,'result':result}
            return render(request,
                          'basicinformation/teacher_online_analysis3.html', context)




    elif 'directtestid' in request.GET:
        print('1037')
        test_id = request.GET['directtestid']
        me = Teach(user)
        # get the number of students who took test
        online_marks =\
        SSCOnlineMarks.objects.filter(test__id=test_id,student__school =
                                      me.profile.school)
    # try to get result table associated with particular test
        try:
            result = TestRankTable.objects.get(test__id = test_id)
    # if no new student has taken the test then simply sort the old rank table 
            if len(result.names) == len(online_marks):
                result = me.combine_rankTable(result)

    # else generate new rank table, sort it and display it 
            else:
                asyn_rt = generate_testRankTable.delay(user.id,test_id)
                result = 'None'
                while result is 'None':
                    try:
                        result = TestRankTable.objects.filter(test__id =\
                                                      test_id).order_by('-time')[0]
                        result = combine_rankTable(result)

                    except :
                        pass
    # if no result table is found associated to particular test then generate
    # new rank table, sort it and display it

        except:
            asyn_rt = generate_testRankTable.delay(user.id,test_id)
            result = 'None'
            while result is 'None':
                try:
                    result = TestRankTable.objects.filter(test__id =\
                                                  test_id).order_by('-time')[0]
                    result = me.combine_rankTable(result)
                except: pass

    # try if result loader exists for the given test
    # in case of except
        # if result_loader doesn't exist then-
    # case 1 : teacher is clicking on the analysis for this test for 1st time
    #   hence, create a new result loader with this test
    #   and show it in the template

        try:
            result_loader = SscTeacherTestResultLoader.objects.get(test__id = test_id)
        except:

            new_rl = teacher_test_analysis_new.delay(test_id,user.id)
            te_id = new_rl.task_id
            res = AsyncResult(te_id)
            new_rl = None
            while new_rl is None:
                try:
                    new_rl = SscTeacherTestResultLoader.objects.get(test__id = test_id)
                except SscTeacherTestResultLoader.DoesNotExist:
                    pass
            max_marks = new_rl.test.max_marks    
            average = new_rl.average
            percent_average = new_rl.percentAverage
            grade_s = new_rl.grade_s
            grade_a = new_rl.grade_a
            grade_b = new_rl.grade_b
            grade_c = new_rl.grade_c
            grade_d = new_rl.grade_d
            grade_e = new_rl.grade_e
            grade_f = new_rl.grade_f
            skipped_quests = new_rl.skipped
            skipped_freq = new_rl.skippedFreq
            sq = list(zip(skipped_quests,skipped_freq))
            freqQuests = new_rl.freqAnswersQuestions
            freqQuestsfreq = new_rl.freqAnswersFreq
            freq = list(zip(freqQuests,freqQuestsfreq))
            pro_quests = new_rl.problemQuestions
            pro_freq  = new_rl.problemQuestionsFreq
            problem_quests = list(zip(pro_quests,pro_freq))

            context = {'om':
                       online_marks,'test':new_rl.test,'average':new_rl.average
                       ,'percentAverage':new_rl.percentAverage,'maxMarks':max_marks,
                       'grade_s':new_rl.grade_s,'grade_a':new_rl.grade_a,'grade_b':new_rl.grade_b,'grade_c':new_rl.grade_c,
                       'grade_d':new_rl.grade_d,'grade_e':new_rl.grade_e,'grade_f':new_rl.grade_f,
                       'freq':freq,'sq':sq,'problem_quests':problem_quests,'ssc':True,'result':result}
            return render(request,'basicinformation/teacher_online_analysis_direct.html', context)
 
# result loader is found but don't know if more students have taken
# the test, hence compare number of students in result loader with number of
# online marks calculated above 

        saved_marks = result_loader.onlineMarks.all()
        if len(online_marks) == len(saved_marks):
# case 2 : if no new student has taken the test then just load and display
# result_loder
            max_marks = result_loader.test.max_marks    
            pro_quests = result_loader.problemQuestions
            pro_freq  = result_loader.problemQuestionsFreq
            average = result_loader.average
            percent_average = result_loader.percentAverage
            problem_quests = list(zip(pro_quests,pro_freq))
            grade_s = result_loader.grade_s
            grade_a = result_loader.grade_a
            grade_b = result_loader.grade_b
            grade_c = result_loader.grade_c
            grade_d = result_loader.grade_d
            grade_e = result_loader.grade_e
            grade_f = result_loader.grade_f
            skipped_quests = result_loader.skipped
            skipped_freq = result_loader.skippedFreq
            sq = list(zip(skipped_quests,skipped_freq))
            freqQuests = result_loader.freqAnswersQuestions
            freqQuestsfreq = result_loader.freqAnswersFreq
            freq = list(zip(freqQuests,freqQuestsfreq))
            context = {'om':
                       online_marks,'test':result_loader.test,'average':result_loader.average
                       ,'percentAverage':result_loader.percentAverage,'maxMarks':max_marks,
                       'grade_s':result_loader.grade_s,'grade_a':result_loader.grade_a,'grade_b':result_loader.grade_b,'grade_c':result_loader.grade_c,
                       'grade_d':result_loader.grade_d,'grade_e':result_loader.grade_e,'grade_f':result_loader.grade_f,
                       'freq':freq,'sq':sq,'problem_quests':problem_quests,'ssc':True,'result':result}
            return render(request,
                          'basicinformation/teacher_online_analysis_direct.html', context)
# case 3 : if more students have taken the test then result_loader has to be
# updated and then displyed in the template
        else:
            new_rl = teacher_test_analysis_already.delay(test_id,user.id)
            rl_id = new_rl.task_id
            max_marks = result_loader.test.max_marks    
            pro_quests = result_loader.problemQuestions
            pro_freq  = result_loader.problemQuestionsFreq
            average = result_loader.average
            percent_average = result_loader.percentAverage
            problem_quests = list(zip(pro_quests,pro_freq))
            grade_s = result_loader.grade_s
            grade_a = result_loader.grade_a
            grade_b = result_loader.grade_b
            grade_c = result_loader.grade_c
            grade_d = result_loader.grade_d
            grade_e = result_loader.grade_e
            grade_f = result_loader.grade_f
            skipped_quests = result_loader.skipped
            skipped_freq = result_loader.skippedFreq
            sq = list(zip(skipped_quests,skipped_freq))
            freqQuests = result_loader.freqAnswersQuestions
            freqQuestsfreq = result_loader.freqAnswersFreq
            freq = list(zip(freqQuests,freqQuestsfreq))
            context = {'om':
                       online_marks,'test':result_loader.test,'average':result_loader.average
                       ,'percentAverage':result_loader.percentAverage,'maxMarks':max_marks,
                       'grade_s':result_loader.grade_s,'grade_a':result_loader.grade_a,'grade_b':result_loader.grade_b,'grade_c':result_loader.grade_c,
                       'grade_d':result_loader.grade_d,'grade_e':result_loader.grade_e,'grade_f':result_loader.grade_f,
                       'freq':freq,'sq':sq,'problem_quests':problem_quests,'ssc':True,'result':result}
            return render(request,
                          'basicinformation/teacher_online_analysis_direct.html', context)




    elif 'onlineIndividualPerformace' in request.GET:
        which_klass = request.GET['onlineIndividualPerformace']
        subjects = me.test_taken_subjects(user)
        context = {'subs': subjects, 'which_class': which_klass}
        return \
            render(request,
                   'basicinformation/teacher_online_individualPerformace.html', context)
    elif 'individualonlineschoolSubject' in request.GET:
        sub_class = request.GET['individualonlineschoolSubject']
        sub = sub_class.split(',')[0]
        klass = sub_class.split(',')[1]
        online_tests = SSCKlassTest.objects.filter(creator =
                                                       user,klas__name =
                                                       klass,sub=sub).order_by('published')
        context = {'tests': online_tests}
        return render(request,
                      'basicinformation/teacher_online_individualPerformance2.html', context)
    elif 'individualonlinetestid' in request.GET:
        test_id = request.GET['individualonlinetestid']
        offline_every_marks = SSCOfflineMarks.objects.filter(test__id =
                                                     test_id)
        if len(offline_every_marks)>0:
            studs = []
            for stu in offline_every_marks:
                studs.append(stu.student)
            context = {'students':studs,'test_id':test_id}
            return \
    render(request,'basicinformation/teacher_online_individualPerformance3.html',context)
        else:
            online_every_marks = SSCOnlineMarks.objects.filter(test__id =
                                                         test_id)
            studs = []
            for stu in online_every_marks:
                studs.append(stu.student)
            context = {'students':studs,'test_id':test_id}
            return \
    render(request,'basicinformation/teacher_online_individualPerformance3.html',context)
    elif 'individualStudentid' in request.GET:
        stude_test = request.GET['individualStudentid']
        test_id = stude_test.split(',')[1]
        student_id = stude_test.split(',')[0]
        try:
            his_marks = SSCOfflineMarks.objects.get(student__id = student_id,
                                            test__id = test_id)
        except:
            his_marks = SSCOnlineMarks.objects.get(student__id = student_id,
                                            test__id = test_id)
        student_type = 'SSC'

        context = {'test':his_marks,'student_type':student_type}
        return \
    render(request,'basicinformation/teacher_online_individualPerformance4.html',context)

def teacher_download_result(request):
    user = request.user
    me = Teach(user)
    if 'downloadresult' in request.GET:
        test_id = request.GET['downloadresult']
        result = TestRankTable.objects.filter(test__id =\
                                                  test_id).order_by('-time')[0]
        result = me.combine_rankTable(result)
       
        if len(result) == 0:
            result = me.generate_rankTable(test_id,mode='offline')
        try:
            result = result[result[:,3].argsort()]
        except:
            result = result
        df = pd.DataFrame(result)
        excel_result = IO()
        xlwriter = pd.ExcelWriter(excel_result, engine= 'xlsxwriter')
        df.to_excel(xlwriter,'result')
        xlwriter.save()
        xlwriter.close()
        excel_result.seek(0)
        response =\
        HttpResponse(excel_result.read(),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=results.xlsx'

        return response

def teacher_show_time_table(request):
    me = Teacher(request.user)
    time_table = TimeTable.objects.filter(teacher = me.profile)


        
# functions for school management
def management_information(request):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name='Management').exists():
            if 'managementBatchid' in request.GET:
               batchid = request.GET['managementBatchid']
               teachers = Teacher.objects.filter(Q(school =\
                                                  user.schoolmanagement.school) and
               Q(subBatch = None))
               if len(teachers) != 0:
                   context = {'SubBatch':True,'batch':batchid}
                   return\
               render(request,'basicinformation/management_Information2.html',context)
               else:
                   tests = SSCKlassTest.objects.filter(klas__id = batchid)
                   teachers = []
                   for te in tests:
                       teachers.append(te.creator)
                   teachers = list(unique_everseen(teachers)) 
                   context = {'teachers':teachers,'batch':batchid}
                   return\
                render(request,'basicinformation/management_Information3.html',context)
            if 'managementChoice' in request.GET:
                choiceandbatch = request.GET['managementChoice']
                choice = choiceandbatch.split(',')[0]
                batch_id = choiceandbatch.split(',')[1]

                if choice == 'chbatch':

                    context={'ho':'hello'} 
                    return\
                render(request,'basicinformation/management_Information3.html',context)
                else:
                   tests = SSCKlassTest.objects.filter(klas__id = batch_id)
                   teachers = []
                   for te in tests:
                       teachers.append(te.creator)
                   teachers = list(unique_everseen(teachers)) 
                   context = {'teachers':teachers}

                   return\
                render(request,'basicinformation/management_Information3.html',context)
            if 'managementTeacherid' in request.GET:
                teacher_id = request.GET['managementTeacherid']
                tests = SSCKlassTest.objects.filter(creator__id = teacher_id)
                context = {'tests':tests}
                return\
            render(request,'basicinformation/management_Information4.html',context)
            if 'managementTestid' in request.GET:
                test_id = request.GET['managementTestid']
                test = SSCKlassTest.objects.get(id= int(test_id))
                teacher_user = test.creator
                me = Teach(teacher_user)
                online_marks = SSCOnlineMarks.objects.filter(test__id=test_id)
                try:
                    result_loader = SscTeacherTestResultLoader.objects.get(test__id = test_id)
                except Exception as e:
                    print(str(e))

                    result_loader = SscTeacherTestResultLoader()
                    res_test = SSCKlassTest.objects.get(id=test_id)
                    result_loader.test = res_test
                    result_loader.teacher = me.profile
                    max_marks = res_test.max_marks
                    result_loader.average,result_loader.percentAverage =\
                    me.online_findAverageofTest(test_id,percent='p')
                    result_loader.grade_s,result_loader.grade_a,result_loader.grade_b,\
                    result_loader.grade_c,result_loader.grade_d,\
                    result_loader.grade_e,result_loader.grade_f,\
                     = me.online_freqeucyGrades(test_id)
                    skipped_loader = me.online_skippedQuestions(test_id)
                    result_loader.skipped = list(skipped_loader[:,0])
                    result_loader.skippedFreq = list(skipped_loader[:,1])
                    problem_loader = me.online_problematicAreasperTest(test_id)
                    result_loader.problemQuestions = list(problem_loader[:,0])
                    result_loader.problemQuestionsFreq = list(problem_loader[:,1])
                    freqAnswers = me.online_QuestionPercentage(test_id)
                    freqAnswerQuest = freqAnswers[:,0]
                    freqAnswersfreq = freqAnswers[:,1]
                    result_loader.freqAnswersQuestions = list(freqAnswerQuest)
                    result_loader.freqAnswersFreq = list(freqAnswersfreq)
                    result_loader.save()
                    for i in online_marks:
                        result_loader.onlineMarks.add(i)
                    result = me.generate_rankTable(test_id)
                    try:
                        result = result[result[:,3].argsort()]
                    except:
                        result = None
                    context = {'om':
                               online_marks,'test':result_loader.test,'average':result_loader.average
                               ,'percentAverage':result_loader.percentAverage,'maxMarks':max_marks,
                               'grade_s':result_loader.grade_s,'grade_a':result_loader.grade_a,'grade_b':result_loader.grade_b,'grade_c':result_loader.grade_c,
                               'grade_d':result_loader.grade_d,'grade_e':result_loader.grade_e,'grade_f':result_loader.grade_f,
                               'freq':freqAnswers,'sq':skipped_loader,'problem_quests':problem_loader,'ssc':True,'result':result}

                    return\
                    render(request,'basicinformation/management_Information5.html',context)
                saved_marks = result_loader.onlineMarks.all()
                if len(online_marks) == len(saved_marks):
                    max_marks = result_loader.test.max_marks    
                    pro_quests = result_loader.problemQuestions
                    pro_freq  = result_loader.problemQuestionsFreq
                    average = result_loader.average
                    percent_average = result_loader.percentAverage
                    problem_quests = list(zip(pro_quests,pro_freq))
                    grade_s = result_loader.grade_s
                    grade_a = result_loader.grade_a
                    grade_b = result_loader.grade_b
                    grade_c = result_loader.grade_c
                    grade_d = result_loader.grade_d
                    grade_e = result_loader.grade_e
                    grade_f = result_loader.grade_f
                    skipped_quests = result_loader.skipped
                    skipped_freq = result_loader.skippedFreq
                    sq = list(zip(skipped_quests,skipped_freq))
                    freqQuests = result_loader.freqAnswersQuestions
                    freqQuestsfreq = result_loader.freqAnswersFreq
                    freq = list(zip(freqQuests,freqQuestsfreq))
                    result = me.generate_rankTable(test_id)
                    try:
                        result = result[result[:,3].argsort()]
                    except:
                        result = None
                    context = {'om':
                               online_marks,'test':result_loader.test,'average':result_loader.average
                               ,'percentAverage':result_loader.percentAverage,'maxMarks':max_marks,
                               'grade_s':result_loader.grade_s,'grade_a':result_loader.grade_a,'grade_b':result_loader.grade_b,'grade_c':result_loader.grade_c,
                               'grade_d':result_loader.grade_d,'grade_e':result_loader.grade_e,'grade_f':result_loader.grade_f,
                               'freq':freq,'sq':sq,'problem_quests':problem_quests,'ssc':True,'result':result}
                    return render(request,
                                  'basicinformation/management_Information5.html', context)

                else:
                    result = me.generate_rankTable(test_id)
                    try:
                        result = result[result[:,3].argsort()]
                    except:
                        result = None
                    
                    
                    result_loader.average,result_loader.percentAverage =\
                    me.online_findAverageofTest(test_id,percent='p')
                    result_loader.grade_s,result_loader.grade_a,result_loader.grade_b,\
                    result_loader.grade_c,result_loader.grade_d,\
                    result_loader.grade_e,result_loader.grade_f,\
                     = me.online_freqeucyGrades(test_id)
                    skipped_loader = me.online_skippedQuestions(test_id)
                    result_loader.skipped = list(skipped_loader[:,0])
                    result_loader.skippedFreq = list(skipped_loader[:,1])
                    problem_loader = me.online_problematicAreasperTest(test_id)
                    result_loader.problemQuestions = list(problem_loader[:,0])
                    result_loader.problemQuestionsFreq = list(problem_loader[:,1])
                    freqAnswers = me.online_QuestionPercentage(test_id)
                    freqAnswerQuest = freqAnswers[:,0]
                    freqAnswersfreq = freqAnswers[:,1]
                    result_loader.freqAnswersQuestions = list(freqAnswerQuest)
                    result_loader.freqAnswersFreq = list(freqAnswersfreq)
                    result_loader.save()
                    max_marks = result_loader.test.max_marks
                    for i in online_marks:
                        result_loader.onlineMarks.add(i)
                    context = {'om':
                               online_marks,'test':result_loader.test,'average':result_loader.average
                               ,'percentAverage':result_loader.percentAverage,'maxMarks':max_marks,
                               'grade_s':result_loader.grade_s,'grade_a':result_loader.grade_a,'grade_b':result_loader.grade_b,'grade_c':result_loader.grade_c,
                               'grade_d':result_loader.grade_d,'grade_e':result_loader.grade_e,'grade_f':result_loader.grade_f,
                               'freq':freqAnswers,'sq':skipped_loader,'problem_quests':problem_loader,'ssc':True,'result':result}
                    return render(request,
                              'basicinformation/management_Information5.html', context)














               #batchid = request.GET['managementBatchid']
               #tests = SSCKlassTest.objects.filter(klas__id = batchid)
               #teachers = []
               #for te in tests:
               #    teachers.append(te.creator)
               #teachers = list(unique_everseen(teachers)) 
               #context = {'teachers':teachers}
               #return\
           #render(request,'basicinformation/management_Information2.html',context)

            if 'managementTeacherid' in request.GET:
                return HttpResponse('teacher')
            klasses = klass.objects.filter(school=user.schoolmanagement.school)
            context = {'klasses':klasses}
            return\
        render(request,'basicinformation/management_Information.html',context)



# functions for the admin


def create_entities(request):
    if request.POST:
        who = request.POST['deed']
        if who == 'teacher':
            create_teacher(5)
            return HttpResponse('done')
        elif who == 'student':
            create_student(100,request)
            return HttpResponse('done') 



def create_student(num, request):

    user = request.user
    school = School.objects.get(name='Swami Reasoning World')
    teacher = Teacher.objects.get(school__name = 'Swami Reasoning World')
    for i in range(1, num):
        try:
            us = User.objects.create_user(username='student' +
                                          str(i),
                                          email='studentss' + str(i) + '@gmail.com',
                                          password='dummypassword')
            us.save()
            gr = Group.objects.get(name='Students')
            gr.user_set.add(us)
            cl = klass.objects.filter(school__name='Not Dummy School')
            classes = []
            for cc in cl:
                classes.append(cc)
            stu = Student(studentuser=us, klass=np.random.choice(classes),
                              rollNumber=int(str(randint(7000,12000)) + '00'),
                              name='stud' + str(randint(800,4500)),
                              dob=timezone.now(),
                          pincode=int(str(405060)),school= school)
            stu.save()
            sub = Subject(name='Maths', student=stu, teacher=mathTeacher, test1
            =randint(3, 10), test2=randint(3, 9), test3=
                          randint(3, 9))
            sub1 = Subject(name='Science', student=stu, teacher=scienceTeacher, test1
            =randint(3, 10), test2=randint(3, 9), test3=
                          randint(3, 9))

            sub.save()
        except Exception as e:
            print(str(e))

def real_create_student(stu,schoolName,swami=False,multiTeacher
                        =False,delUsers=False):
    print('in process............')
    school = School.objects.get(name=schoolName)
    if delUsers == True:
        try:
            for na,bat,phone,te,em in stu:
                user = User.objects.get(username=phone)
                user.delete()
                print('deleted')
        except Exception as e:
            print('user delete error')
            print(str(e))

    if swami:
        for na,dob,batch,phone,password in stu:
            try:
                teacher = Teacher.objects.get(teacheruser__username =
                                              'rajeshkswamiadmin')
            except Exception as e:
                print(str(e))
            try:
                us = User.objects.create_user(username=phone,
                                                email=str(na)+'@swami.com',
                                              password=password)
                us.save()
                gr = Group.objects.get(name='Students')
                gr.user_set.add(us)
                if batch == 16:
                    cl = klass.objects.get(school__name='Swami Reasoning World',name='Batch16')
                elif batch == 17:
                    cl = klass.objects.get(school__name='Swami Reasoning World',name='Batch17')
                elif batch == 24:
                    cl = klass.objects.get(school__name='Swami Reasoning World',name='Batch24')
                elif batch == 15:
                    cl = klass.objects.get(school__name='Swami Reasoning World',name='Batch15')
                stu = Student(studentuser=us, klass=cl,
                                  rollNumber=us.id,
                                  name= str(na),
                                  dob=datetime.strptime(dob,'%d/%m/%Y').strftime('%Y-%m-%d'),
                              pincode=int(str(302018)),school= school)
                stu.save()
                sub = Subject(name='General-Intelligence', student=stu,
                              teacher=teacher)

                sub.save()
                print('%s -- saved' %na)

            except Exception as e:
                print(str(e))

    else:
        for na,batch,phone,teach,email in stu:
            try:
                if multiTeacher:
                    teacher = Teacher.objects.filter(school__name = schoolName)
                    print('%s num teacher' %len(teacher))
                else:
                    teacher = Teacher.objects.get(teacheruser__username = teach)
                    print(teacher)
            except Exception as e:
                print(str(e))
            try:
                pa = str(phone)
                pa = pa[::-1]
                us = User.objects.create_user(username=phone,
                                              email='',
                                              password=pa)
                us.save()
                gr = Group.objects.get(name='Students')
                gr.user_set.add(us)
                if schoolName == 'Swami Reasoning World':
                    if batch == 16:
                        cl = klass.objects.get(school__name='Swami Reasoning World',name='Batch16')
                    elif batch == 17:
                         cl = klass.objects.get(school__name='Swami Reasoning World',name='Batch17')
                    elif batch == 24:
                          cl = klass.objects.get(school__name='Swami Reasoning World',name='Batch24')
                    elif batch == 15:
                          cl = klass.objects.get(school__name='Swami Reasoning World',name='Batch15')
                elif schoolName =='JECRC':
                    if '4th' in batch:
                        cl =\
                        klass.objects.get(school__name=schoolName,name='IT-4th-semester')
                    if '6th' in batch:
                        cl =\
                        klass.objects.get(school__name=schoolName,name='IT-6th-semester')
                elif schoolName == 'Govindam Defence Academy':
                    cl = klass.objects.get(school__name =
                                           schoolName,name='DefenceBatch')
                elif schoolName == 'Colonel Defence Academy':
                    cl = klass.objects.get(school__name =
                                           schoolName,name='DefenceBatch')
                elif schoolName == 'Kartavya Defence Academy':
                    cl = klass.objects.get(school__name =
                                           schoolName,name='DefBatchKartavya')
                elif schoolName == 'KR Defence Coaching':
                    cl = klass.objects.get(school__name =
                                           schoolName,name='DefBatchKr')

                elif schoolName == 'Aravali Defence Academy':
                    cl = klass.objects.get(school__name=schoolName,name=batch)

                stu = Student(studentuser=us, klass=cl,
                                  rollNumber=us.id,
                                  name= str(na),
                                  dob=timezone.now(),
                              pincode=int(str(302018)),school= school)
                stu.save()
                if multiTeacher:
                    for te in teacher:
                        print('%s teacher name ' %te)
                        sub = Subject(name='Defence-Physics', student=stu,
                                      teacher=te)
                        sub1 = Subject(name='GroupX-Maths', student=stu,
                                      teacher=te)
                        sub2 = Subject(name='Defence-English', student=stu,
                                      teacher=te)
                        sub3 = Subject(name='Defence-GK-CA', student=stu,
                                      teacher=te)
                        sub4 = Subject(name='General-Intelligence', student=stu,
                                      teacher=te)

                        sub.save()
                        print('%s student-- %s subject -- %s teacher'
                              %(stu,sub.name,te))
                        sub1.save()
                        print('%s student-- %s subject -- %s teacher'
                              %(stu,sub1.name,te))
                        sub2.save()
                        print('%s student-- %s subject -- %s teacher'
                              %(stu,sub2.name,te))
                        sub3.save()
                        print('%s student-- %s subject -- %s teacher'
                              %(stu,sub3.name,te))
                        sub4.save()
                        print('%s student-- %s subject -- %s teacher'
                              %(stu,sub4.name,te))

                else:
                    sub = Subject(name='General-Intelligence', student=stu,
                                  teacher=teacher)
                    #sub1 = Subject(name='GroupX-Maths', student=stu,
                    #              teacher=teacher)
                    #sub2 = Subject(name='Defence-English', student=stu,
                    #              teacher=teacher)

                    sub.save()
                    #sub1.save()
                    #sub2.save()

                print('%s -- saved' %na)
            except Exception as e:
                print(str(e))


def create_teacher(num):
    school1 = School.objects.get(name='Dummy School')
    school2 = School.objects.get(name='Not Dummy School')
    schools = [school1,school2]
    for i in range():
        try:
            us = User.objects.create_user(username='teacher' + str(i),
                                          email='teacher' + str(i) + '@gmail.com',
                                          password='dummypassword')
            us.save()
            gr = Group.objects.get(name='Teachers')
            gr.user_set.add(us)

            teache = Teacher(teacheruser=us,
                             experience=randint(1, 20), name=us.username,
                             school=np.random.choice(schools))
            teache.save()
        except Exception as e:
            print(str(e))

def read_questions(fi):
    with open(fi,encoding='latin-1') as questFile:
        readcsv = csv.reader(questFile,delimiter=',')
        questText = []
        a = []
        b = []
        c = []
        d = []
        for row in questFile:
            text = row[1]
            questText.append(str(text))
    return questText


def write_passages(passages):
    for i in passages:
        new_passage = Comprehension()
        new_passage.text = str(i)
        new_passage.save()

def evaluate_offline_test(studentid,opt):
    test = SSCKlassTest.objects.get(creator__username = 'rajeshkswamiadmin')
    qid = []
    for q in test.sscquestions_set.all():
        qid.append(q.id)
    qans = list(zip(qid,opt))
    chid = []
    rightAnswer = []
    wrongAnswer = []
    allAnswer = []
    skippedAnswer = []
    total_marks = 0
    for j,k in qans:
        quest = SSCquestions.objects.get(id=j)
        for n,i in enumerate(quest.choices_set.all()):
            if k == '0':
                skippedAnswer.append(j)
                break
            if k == 'a' and n == 0:
                chid.append(i.id)
                if i.predicament == 'Correct':
                    rightAnswer.append(i.id)
                    allAnswer.append(i.id)
                    total_marks += 2
                elif i.predicament == 'Wrong':
                    wrongAnswer.append(i.id)
                    allAnswer.append(i.id)
                    total_marks -= 0.25
                break
            elif k == 'b' and n == 1:
                chid.append(i.id)
                if i.predicament == 'Correct':
                    rightAnswer.append(i.id)
                    allAnswer.append(i.id)
                    total_marks += 2
                elif i.predicament == 'Wrong':
                    wrongAnswer.append(i.id)
                    allAnswer.append(i.id)
                    total_marks -= 0.25
                break
            elif k == 'c' and n == 2:
                chid.append(i.id)
                if i.predicament == 'Correct':
                    rightAnswer.append(i.id)
                    allAnswer.append(i.id)
                    total_marks += 2
                elif i.predicament == 'Wrong':
                    wrongAnswer.append(i.id)
                    allAnswer.append(i.id)
                    total_marks -= 0.25
                break
            elif k == 'd' and n == 3:
                chid.append(i.id)
                if i.predicament == 'Correct':
                    rightAnswer.append(i.id)
                    allAnswer.append(i.id)
                    total_marks += 2
                elif i.predicament == 'Wrong':
                    wrongAnswer.append(i.id)
                    allAnswer.append(i.id)
                    total_marks -= 0.25
                break
            elif k == 'e' and n == 4:
                chid.append(i.id)
                if i.predicament == 'Correct':
                    rightAnswer.append(i.id)
                    allAnswer.append(i.id)
                    total_marks += 2
                elif i.predicament == 'Wrong':
                    wrongAnswer.append(i.id)
                    allAnswer.append(i.id)
                    total_marks -= 0.25
                break
    offline_marks = SSCOfflineMarks()
    offline_marks.allAnswers = allAnswer
    offline_marks.rightAnswers = rightAnswer
    offline_marks.wrongAnswers = wrongAnswer
    offline_marks.skippedAnswers = skippedAnswer
    offline_marks.test = test
    student = Student.objects.get(studentuser__username = studentid)
    offline_marks.student = student
    offline_marks.marks = total_marks
    offline_marks.testTaken = timezone.now()
    offline_marks.save()
             

def trial_ai(request):
    school = School.objects.get(name= 'Swami Reasoning World')
    students = Student.objects.filter(school=school)
    marks = []
    stud = []
    time = []
    ave_oftest = []
    for st in students:
        try:
            online_marks = SSCOnlineMarks.objects.filter(student =
                                                         st).order_by('testTaken')
            if len(online_marks) != 0:
                marks.extend(online_marks)
                for times in range(len(online_marks)):
                    stud.append(st)
                for num,om in enumerate(online_marks):
                    try:
                        test_loader =\
                        SscTeacherTestResultLoader.objects.get(test=om.test)
                        ave_oftest.append(test_loader.average)
                    except Exception as e:
                        print(str(e))
                        ave_oftest.append(float('nan'))
                    time.append(int(num+1))
        except Exception as e:
            print(str(e))
    st_marks = list(zip(stud,marks,ave_oftest,time))
    st_marks = np.array(st_marks)
    print(st_marks)
    print(st_marks.shape)
    qid2 = []
    catid2 = []
    accid2 = []
    st2 = []
    quest_acc = []
    questidfinal = []
    for st in students:
        online_marks =\
        SSCOnlineMarks.objects.filter(student=st).order_by('testTaken')
        if len(online_marks) != 0:
            for nu,marks in enumerate(online_marks):
                qid = []
                catid = []
                r_w = []
                for nu,quest in enumerate(marks.test.sscquestions_set.all()):
                    q_test = SSCOnlineMarks.objects.filter(test__sscquestions=quest)
                    right = 0
                    wrong = 0
                    skipped = 0
                    for q in q_test:
                        for c in quest.choices_set.all():
                            if c.id in q.rightAnswers:
                                right += 1
                            if c.id in q.wrongAnswers:
                                wrong += 1
                            else:
                                skipped += 1
                    try:
                        quest_acc.append((right-wrong)/(right+wrong)*100)
                        questidfinal.append(quest.id)
                    except Exception as e:
                        print(str(e))
                        quest_acc.append(float('nan'))
                        questidfinal.append(quest.id)

                    
                        
                    for ch in quest.choices_set.all():
                        if ch.id in marks.rightAnswers:
                            r_w.append('R')
                        if ch.id in marks.wrongAnswers:
                            r_w.append('W')
                        else:
                            r_w.append('S')
                        qid.append(quest.id)
                        catid.append(quest.topic_category)
                        st2.append(st.id)
                qid2.extend(qid)
                catid2.extend(catid)
                accid2.extend(r_w)

    #unique,count = np.unique(catid2,return_counts = True)
    #cat_unique = np.asarray((unique,count)).T
    cat_unique = list(unique_everseen(catid2))
    cat_tot = []
    acc_cat_stu = []
    stu_cat = []
    for st in students:
        for un_cat in cat_unique:
            right = 0
            wrong = 0
            om_marks = SSCOnlineMarks.objects.filter(test__testTakers
                                                     =st)
            for om in om_marks:
                for quest in\
                om.test.sscquestions_set.filter(topic_category=un_cat):
                    for ch in quest.choices_set.all():
                        if ch.id in om.rightAnswers:
                            right += 1
                        if ch.id in om.wrongAnswers:
                            wrong += 1
            try:
                acc = ((right-wrong)/(right+wrong)*100)

            except Exception as e:
                acc_cat_stu.append(float('nan'))
            cat_tot.append(un_cat)
            acc_cat_stu.append(acc)
            stu_cat.append(st.id)

           

    personal_cat = list(zip(stu_cat,cat_tot,acc_cat_stu))
    personal_cat = np.array(personal_cat)
    print(personal_cat)
    print(personal_cat.shape)
    qu_acc = list(zip(questidfinal,quest_acc))
    qu_acc = np.array(qu_acc)
    final = list(zip(st2,qid2,catid2,accid2))
    final = np.array(final)
    quest_accuracy = []
    for st,qid,catid,accid in final:
        for q,a in qu_acc:
            if int(qid) == int(q):
                quest_accuracy.append(a)
    final2 = list(zip(st2,qid2,catid2,accid2,quest_accuracy))
    final2 = np.array(final2)
    stu_category = []
    last_st = []
    last_cat = []
    last_qid = []
    last_accid = []
    last_questacc = []
    last_stqacc = []
    for st,qid,catid,accid,quest_accuracy in final2:
        for stid,cat,qacc in personal_cat:
            if st == stid and catid == cat:
                last_st.append(st)
                last_cat.append(catid)
                last_qid.append(qid)
                last_accid.append(accid)
                last_questacc.append(quest_accuracy)
                last_stqacc.append(qacc)
    last =\
    list(zip(last_st,last_cat,last_qid,last_accid,last_questacc,last_stqacc))
    last = np.array(last)
    with open('bodhidata.pkl','wb') as fi:
        pickle.dump(last,fi)
    print(last)
    print(last.shape)
    print(last.shape)
    print(len(stu_category))
    print(len(personal_cat))
    print(final.shape)
    print(qu_acc.shape)



def replace_quest_image(sheet_link,production=False):
    for sh in sheet_link:
        if production:
            df=\
            pd.read_csv('/app/question_data/jito_IITJEE/'+sh,error_bad_lines=False )
        else:
            df=\
            pd.read_csv('/home/prashant/Desktop/programming/projects/bod/BodhiAI/question_data/jito_IITJEE/'+sh,error_bad_lines=False )
    old_links = df['oldLink']
    new_links = df['newLink']
    link_list = list(zip(old_links,new_links))


    for old,new in link_list:
        print('%s old link, %s new link' %(old,new))
        image_question = SSCquestions.objects.filter(picture = old)
        print(len(image_question))
        for i in image_question:
            i.picture = new
            i.save()
    #image_questions = SSCquestions.objects.all()
    #all_quests = []
    #for i in image_questions:
    #    if i.picture != None:
    #        all_quests.append(i)
    #for num,i in enumerate(all_quests):
    #    if num == 5:
    #        break
    #    img = Image.open(requests.get(i.picture,stream=True).raw)
    #    img = img.convert("RGBA")
    #    datas = img.getdata()
    #    newData = []
    #    for item in datas:
    #        if item[0] == 255 and item[1] == 255 and item[2]:
    #            newData.append((255,255,255,0))
    #        else:
    #            newData.append(item)
    #            img.putdata(newData)
    #    img.show()

def real_create_teacher(name,teach,ph = False):
    school = School.objects.get(name=name)
    for name,batch,email in teach:
        print([name,batch,email])
        if ph:
            pas = str(email)
            pas = pas[::-1]
        else:
            pass
        try:
            us = User.objects.create_user(username=str(email),
                                          email='',
                                          password=pas)
            us.save()
            gr = Group.objects.get(name='Teachers')
            gr.user_set.add(us)

            teache = Teacher(teacheruser=us,
                             experience=0, name=name,
                             school=school)
            teache.save() 
            print('%s --- name saved' %name)
        except Exception as e:
            print(str(e))

def add_teachers(path_file,schoolName,production=False,jecrc=False,dummy=False):
    if dummy != True:
        if production:
            df = \
            pd.read_csv('/app/client_info/dummy/'+path_file,error_bad_lines =False)
        else:
            df =\
            pd.read_csv('/home/prashant/Desktop/programming/projects/bod/BodhiAI/client_info/dummy/'+path_file,error_bad_lines=False )
        if jecrc:
            name = df['Name']
            batch = df['Group associated']
            email = df['email ID']
            teach = list(zip(name,batch,email))
            real_create_teacher('JECRC',teach)
        if schoolName == 'Colonel Defence Academy':
            print('here in colonel')
            name = df['Name']
            phone = df['Phone']
            batch = ['DefenceBatch','DefenceBatch']
            teach = list(zip(name,batch,phone))
            real_create_teacher('Colonel Defence Academy',teach,ph=True)
        if schoolName == 'Govindam Defence Academy':
            name = df['Name']
            many = len(name)
            phone = df['Phone']
            batch = many*['DefenceBatch']
            teach = list(zip(name,batch,phone))
            real_create_teacher('Govindam Defence Academy',teach,ph=True)
        if schoolName == 'Kartavya Defence Academy':
            name = df['Name']
            many = len(name)
            phone = df['Phone']
            batch = many*['DefBatchKartavya']
            teach = list(zip(name,batch,phone))
            real_create_teacher('Kartavya Defence Academy',teach,ph=True)

        if schoolName == 'KR Defence Coaching':
            name = df['Name']
            many = len(name)
            phone = df['Phone']
            batch = many*['DefBatchKr']
            teach = list(zip(name,batch,phone))

            real_create_teacher('KR Defence Coaching',teach,ph=True)
        if schoolName == 'Aravali Defence Academy':
            name = df['Name']
            many = len(name)
            phone = df['Phone']
            batch = many*['None']
            teach = list(zip(name,batch,phone))

            real_create_teacher('Aravali Defence Academy',teach,ph=True)





    else:
        if schoolName == 'Govindam Defence Academy':
            name = ['Name']
            many = len(name)
            phone = ['Phone']
            batch = many*['DefenceBatch']
            teach = list(zip(name,batch,phone))
            real_create_teacher('Govindam Defence Academy',teach,ph=True)



def add_students(path_file,schoolName,production = False,swami=False,dummy=False):
    if dummy == False:
        if production:
            df = \
            pd.read_csv('/app/client_info/dummy/'+path_file,error_bad_lines =False)
        else:
            df =\
            pd.read_csv('/home/prashant/Desktop/programming/projects/bod/BodhiAI/client_info/dummy/'+path_file,error_bad_lines=False )
        if swami:
            name = df['Name']
            dob = df['DOB']
            batch = df['Batch no']
            username = df['Phone']
            password = df['password']
            stu = list(zip(name,dob,batch,username,password))
            real_create_student(stu,'Swami Reasoning World',swami = True)
            return HttpResponse(stu)
        if schoolName == 'Colonel Defence Academy':
            name = df['Name']
            many = len(name)
            email = many*['']
            phone = df['Phone']
            batch = many*['']
            teach = many*['']
            stu = list(zip(name,batch,phone,teach,email))
            real_create_student(stu,'Colonel Defence Academy',multiTeacher=True)
            return HttpResponse(stu)

        if schoolName == 'Govindam Defence Academy':
            name = df['Name']
            many = len(name)
            email = many*['']
            phone = df['Phone']
            batch = many*['']
            teach = many*['']
            stu = list(zip(name,batch,phone,teach,email))
            real_create_student(stu,'Govindam Defence Academy',multiTeacher=True)
            return HttpResponse(stu)

        if schoolName == 'JECRC':
            name = df['Name']
            email = df['email']
            phone = df['Phone']
            teach = df['TG']
            batch = df['batch']
            stu = list(zip(name,batch,phone,teach,email))
            real_create_student(stu,'JECRC',delUsers= True)
            return HttpResponse(stu)
        if schoolName == 'Kartavya Defence Academy':
            name = df['Name']
            many = len(name)
            email = many*['']
            phone = df['Phone']
            batch = many*['']
            teach = many*['']
            stu = list(zip(name,batch,phone,teach,email))
            real_create_student(stu,'Kartavya Defence Academy',multiTeacher=True,delUsers = True)
            return HttpResponse(stu)
        if schoolName == 'KR Defence Coaching':
            name = df['Name']
            many = len(name)
            email = many*['']
            phone = df['Phone']
            batch = many*['']
            teach = many*['']
            stu = list(zip(name,batch,phone,teach,email))
            real_create_student(stu,'KR Defence Coaching',multiTeacher=True,delUsers=True)
            return HttpResponse(stu)
        if schoolName == 'Aravali Defence Academy':
            name = df['Name']
            many = len(name)
            email = many*['']
            phone = df['Phone']
            batch = df['batch']
            teach = many*['']
            stu = list(zip(name,batch,phone,teach,email))
            real_create_student(stu,'Aravali Defence Academy',multiTeacher=True,delUsers=False)
            return HttpResponse(stu)





    else:
        #name = df['Student Name']
        #email = df['Email ID(Active)']
        #phone = df['Contact Number(Whatsapp)']
        #teach = df['TG']
        #batch = df['batch']
        name = ['Dummy Student1','Dummy Student2','Dummy\
                Student3','Dummy Student4','Dummy Student5','Dummy\
                Student6','Dummy Student7','Dummy Student8','Dummy\
                Student9','Dummy Student10','Dummy Student11','Dummy Student12']
        email =\
        ['dummystudent@govindam.com','dummystudent@govindam.com','dummystudent@govindam.com','dummystudent@govindam.com','dummystudent@govindam.com','dummystudent@govindam.com','dummystudent@govindam.com','dummystudent@govindam.com','dummystudent@govindam.com','dummystudent@govindam.com','dummystudent@govindam.com','dummystudent@govindam.com']
        phone =\
        ['g1','g2','g3','g4','g5','g6','g7','g8','g9','g10','g11','g12']
        teach =\
        ['govindgarwa@gmail.com','govindgarwa@gmail.com','govindgarwa@gmail.com','govindgarwa@gmail.com','govindgarwa@gmail.com','govindgarwa@gmail.com','govindgarwa@gmail.com','govindgarwa@gmail.com','govindgarwa@gmail.com','govindgarwa@gmail.com','govindgarwa@gmail.com','govindgarwa@gmail.com']
        batch =\
        ['Airforce-GroupX','Airforce-GroupX','Airforce-GroupX','Airforce-GroupX','Airforce-GroupX','Airforce-GroupX','Airforce-GroupX','Airforce-GroupX','Airforce-GroupX','Airforce-GroupX','Airforce-GroupX','Airforce-GroupX']
        print(len(name))
        print(len(email))
        print(len(phone))
        print(len(teach))
        print(len(batch))
        stu_details = list(zip(name,batch,phone,teach,email))
        real_create_student(stu_details,'Govindam Defence Academy')


                    
def change_password(institute,acc):
    if institute == 'JECRC':
        for us,pa in acc:
            user = User.objects.get(username = us)
            print(user.password)
            user.set_password(pa)
            user.save()
            print('%s-- username , %s -- password'
                  %(user.username,user.password))



def add_student_subject(institute,subject,teach,allTeacers=False):
    students = Student.objects.filter(school__name = institute)
    if allTeacers:
        teachers = Teacher.objects.filter(school__name = institute)
        for st in students:
            for teach in teachers:
                sub = Subject(name=subject, student=st,
                                    teacher=teach)
                sub.save()

    else:
        teach = Teacher.objects.get(name=teach,school=institute)
        for st in students:
            sub = Subject(name=subject, student=st,
                                    teacher=teach)
            sub.save()


def add_new_subject_student(subject):
    students = Student.objects.filter(school__name = 'JEN')
    teacher = Teacher.objects.get(name = 'Anshul Goyal')
    for st in students:
        sub = Subject(name=subject, student=st,
                                    teacher=teacher)
        sub.save()




def check_add_entities():
        all_students = Student.objects.filter(school__name = 'JECRC')
        all_teachers = Teacher.objects.filter(school__name = 'JECRC')
        
        print(len(all_teachers))
        df =\
        pd.read_csv('/app/client_info/jecrc/jecrc_6thsem_itdepartment.csv',error_bad_lines=False )
        cf =\
        pd.read_csv('/app/client_info/jecrc/jecrc_4thsem.csv',error_bad_lines=False )
        tf =\
        pd.read_csv('/app/client_info/jecrc/jecrc_teacher.csv',error_bad_lines=False )
        name = tf['Name']
        email = tf['email ID']
        em_id = []
        for i in email:
            em_id.append(i)
        password = []
        for i in name:
            j = i.replace(" ","")
            pa = j.lower()
            password.append(str(pa))
        acc = list(zip(em_id,password))
        change_password('JECRC',acc)
        phoneNum = []
        phone = df['Contact Number(Whatsapp)']
        phone2 = cf['Contact Number(Whatsapp)']

        for i in phone:
            phoneNum.append(str(i))
        for i in phone2:
            phoneNum.append(str(i))
        print(len(phoneNum))
        print(phoneNum)
        student_num = []
        for num,st in enumerate(all_students):
            student_num.append(str(st.rollNumber))
        print('%s len students' %len(student_num))
        pho = list(unique_everseen(phoneNum))
        print('%s len pho' %len(pho))
        for n,ph in enumerate(phoneNum):
            if str(ph) in student_num:
                pass
            else:
                print('%s ---%s' %(n,ph))


def old_student_marks():
             #Get all the student marks
            try:
                mathst1,mathst2,mathst3,mathshy,mathst4,mathspredhy =\
                me.readmarks('Maths')
            except:
                mathst1 = mathst2 = mathst3 = mathshy = mathst4 = mathspredhy=None
            try:
                hindit1,hindit2,hindit3,hindihy,hindit4,hindipredhy =\
                me.readmarks('Hindi')
            except:
                hindit1 = hindit2 = hindit3 = hindihy = hindit4 = hindipredhy=None
            try:
                englisht1,englisht2,englisht3,englishhy,englisht4,englishpredhy =\
                me.readmarks('English')
            except:
                englisht1 = englisht2 = englisht3 = englishhy = englisht4 =\
                englishpredhy=None
            try:
                sciencet1,sciencet2,sciencet3,sciencehy,sciencet4,sciencepredhy =\
                me.readmarks('Science')
            except:
                sciencet1 = sciencet2 = sciencet3 = sciencehy = sciencet4 =\
                sciencepredhy=None

            # check for announcements in past 24 hours
            startdate = date.today()
            enddate = startdate - timedelta(days=1)
            try:
                my_announcements = Announcement.objects.filter(listener =
                                                           profile,date__range=[enddate,startdate])
            except:
                my_announcements = None

            # find the predicted marks
            try:
                hindipredhy_raw = \
                me.hindi_3testhyprediction(hindit1,hindit2,hindit3,me.get_dob(),me.get_section())
                hindipredhy = me.predictionConvertion(hindipredhy_raw)
            except:
                pass

            try:
                mathspredhy_raw = \
                me.hindi_3testhyprediction(mathst1,mathst2,mathst3,me.get_dob(),me.get_section())
                mathspredhy = me.predictionConvertion(mathspredhy_raw)
            except:
                pass
            try:
                englishpredhy_raw = \
                me.english_3testhyprediction(englisht1,englisht2,englisht3,me.get_dob(),me.get_section())
                englishpredhy = me.predictionConvertion(englishpredhy_raw)
            except:
                pass
            try:
                sciencepredhy_raw = \
                me.science_3testhyprediction(sciencet1,sciencet2,sciencet3,me.get_dob(),me.get_section())
                sciencepredhy = me.predictionConvertion(sciencepredhy_raw)
            except:
                pass
            context = {'profile': profile, 'subjects': subjects,
                       'hindihy_prediction': hindipredhy, 'mathshy_prediction': mathspredhy,
                       'englishhy_prediction': englishpredhy,
                       'sciencehy_prediction': sciencepredhy,
                       'maths1': mathst1, 'maths2': mathst2, 'maths3': mathst3,
                       'maths4': mathst4, 'hindi1': hindit1, 'hindi2': hindit2,
                       'hindi3': hindit3, 'hindi4': hindit4, 'english1': englisht1,
                       'english2': englisht2, 'english3': englisht3, 'english4': englisht4,
                       'science1': sciencet1, 'science2': sciencet2,
                       'science3': sciencet3, 'science4':
                       sciencet4,'announcements':my_announcements,'message':storage}
def some_AI_function():
            # testing for AI
            #trial_ai(request)
            #school = School.objects.get(name='Swami Reasoning World')
            #student = Student.objects.filter(school = school)
            #all_categories = []
            #student_accuracy = []
            #acc_list_all = []
            #acc_cat_all = []
            #stu_id_all = []
            
            #for i in student:
            #    total_right = []
            #    total_wrong = []
            #    subTest = SSCKlassTest.objects.filter(testTakers = i,sub =
            #                                          'General-Intelligence')
            #    right = 0
            #    wrong = 0
            #    category_right = []
            #    category_wrong = []
            #    for j in subTest:
            #        onlineMarks = SSCOnlineMarks.objects.filter(test =
            #                                                j,student =
            #                                                i)
            #        
            #        for k in onlineMarks:
            #            right = right + len(k.rightAnswers)
            #            wrong = wrong + len(k.wrongAnswers)
            #            for quest in k.test.sscquestions_set.all():
            #                for ch in quest.choices_set.all():
            #                    if ch.id in k.rightAnswers:
            #                        category_right.append(quest.topic_category)

            #                    if ch.id in k.wrongAnswers:
            #                        category_wrong.append(quest.topic_category)

            #            
            #    category_right = np.array(category_right)
            #    category_wrong = np.array(category_wrong)
            #    unique,counts = np.unique(category_right,return_counts = True)
            #    right_category = np.asarray((unique,counts)).T
            #    unique,counts = np.unique(category_wrong,return_counts = True)
            #    wrong_category = np.asarray((unique,counts)).T
            #    print(right_category,wrong_category)
            #    acc_list = []
            #    acc_cat = []
            #    stu_id = []
            #    for ca,freq in right_category:
            #        for cw,freqwr in wrong_category:
            #            if ca == cw:
            #                acc =\
            #                ((int(freq)-int(freqwr))/(int(freq)+int(freqwr)))*100
            #                acc_list.append(acc)
            #                acc_cat.append(ca)
            #                stu_id.append(i.id)
            #    acc_list_all.extend(acc_list)
            #    acc_cat_all.extend(acc_cat)
            #    stu_id_all.extend(stu_id)
            #    for cat_r in category_right:
            #        all_categories.append(cat_r)
            #    for cat_wr in category_wrong:
            #        all_categories.append(cat_wr)
            #acc_student = np.array([stu_id_all,acc_cat_all,acc_list_all])
            #all_categories = list(unique_everseen(all_categories))
            #print(all_categories)
            #teach = Teacher.objects.get(school = school)
            #all_questions = []
            #all_std = []
            #for stu in student:
            #    questions = []
            #    std =[]
            #    online_marks =SSCOnlineMarks.objects.filter(student=stu)
            #    for om in online_marks:
            #        for q in om.test.sscquestions_set.all():
            #            questions.append(q)
            #    count = len(questions)
            #    for i in range(count):
            #        std.append(stu)
            #    all_std.extend(std)
            #    
            #    

            #    if len(questions) != 0:
            #        all_questions.extend(questions)
            #        overall = list(zip(all_std,all_questions))
            #overall = np.array(overall)
            #print(overall.shape)
            #quest_accuracy = []
            #quest_skipped = []
            #for i,k in overall:
            #     
            #    topic = k.topic_category
            #    r_ans = 0
            #    w_ans = 0
            #    s_ans = 0

            #    online_marks =\
            #        SSCOnlineMarks.objects.filter(test__sscquestions=k,test__creator=
            #                                     teach.teacheruser)

            #    for qid in online_marks:
            #        if k.id in qid.skippedAnswers:
            #            s_ans = s_ans + 1
            #        else:
            #            for ch in k.choices_set.all():
            #                if ch.id in qid.rightAnswers:
            #                    r_ans = r_ans + 1
            #                if ch.id in qid.wrongAnswers:
            #                    w_ans = w_ans + 1
            #    try:
            #        accuracy = ((r_ans-w_ans)/(r_ans+w_ans))*100
            #        print('%s--%s---%s---%s----%s'
            #              %(k.id,accuracy,s_ans,r_ans,w_ans))
            #    except:
            #        accuracy = None
            #    quest_accuracy.append(accuracy)
            #    quest_skipped.append(s_ans)
            #quest_accuracy = np.array(quest_accuracy)
            #quest_skipped = np.array(quest_skipped)
            #overall_2 =\
            #np.array([overall[:,0],overall[:,1],quest_accuracy,quest_skipped])
            #overall_2 = np.transpose(overall_2)
            #student_accuracy = np.array(acc_student)
            #student_accuracy = np.transpose(student_accuracy)
            #num = 0
            #for stu,quest,acc,ski in overall_2:
            #    num = num +1
            #    for s,c,a in student_accuracy:
            #        
            #        if int(stu.id) == int(s) and quest.topic_category == c:
            #            print('%s--%s-- %s---%s---%s---%s'
            #                  %(num,stu.id,quest.topic_category,acc,a,ski))
            #predicament = []
            #stu_id = []
            #q_id = []
            #for stu,quest in overall_2[:,[0,1]]:
            #    stu_id.append(stu.id)
            #    q_id.append(quest.id)
            #    online_marks = SSCOnlineMarks.objects.filter(student =
            #                                                 stu,test__sscquestions
            #                                                 = quest)
            #    for om in online_marks:
            #        if quest.id in om.skippedAnswers:
            #            predicament.append('S')
            #        for ch in quest.choices_set.all():
            #            if ch.id in om.rightAnswers:
            #                predicament.append('R')
            #            if ch.id in om.wrongAnswers:
            #                predicament.append('W')
            #predicament = np.array(predicament)
            #stu_id = np.array(stu_id)
            #q_id = np.array(q_id)
            #pred = list(zip(stu_id,predicament,q_id))

            #pred = np.array(pred)
            #print(pred[:10])
            #print(pred.shape)
            #st_final = []
            #qu_final = []
            #qu_cat_fianl = []
            #for st in overall_2[:,0]:
            #    st_final.append(st.id)
            #for qu in overall_2[:,1]:
            #    qu_final.append(qu.id)
            #    qu_cat_fianl.append(qu.topic_category)
            #acc_student = np.transpose(acc_student)

            #print('%s-- ac student' %acc_student)
            #final =\
            #list(zip(st_final,qu_final,qu_cat_fianl,overall_2[:,2],overall_2[:,3],predicament))
            #final = np.array(final)
            #st_accu = []
            #n=0
            #nu = 0
            #for st,qu,cat,tacc,sk,pr in final:
            #    n = n +1
            #    for s,c,a in acc_student:
            #        if int(st) == int(s) and cat == c:
            #            nu = nu + 1
            #            print('%s-- %s-----%s---%s' %(n,nu,a,c))
            #            st_accu.append(a)
            #temp =[]
            #no_ids = []
            #unique,counts = np.unique(st_final,return_counts = True)
            #unique_stu = np.asarray((unique,counts)).T
            #for s in unique_stu[:,0]:
            #    if s in stu_id_all:
            #        temp.append('yes')
            #    else:
            #        temp.append('no')
            #        no_ids.append(s)
            #        print(s)
            #right_quid = []
            #quid = []
            #ls_id = []
            #acc_list = []
            ##for s,q,c,qa,qsk,pre in final:
            ##    marks =\
            ##    SSCOnlineMarks.objects.filter(student=stud)
            ##    if len(marks) == 0:
            ##        acc_list.append(0)
            ##    for ma in marks:
            ##        right = 0
            ##        wrong = 0
            ##        for quest in ma.test.sscquestions_set.all():
            ##            if quest.topic_category == c:
            ##                for ch in quest.choices_set.all():
            ##                    if ch.id in ma.rightAnswers:
            ##                        right = right + 1
            ##                    if ch.id in ma.wrongAnswers:
            ##                        wrong += 1
            ##                try:
            ##                    acc = ((right-wrong)/(right + wrong)*100)
            ##                except:
            ##                    acc = 0
            ##            else:
            ##                continue
            ##        quid.append(quest.id)
            ##        acc_list.append(acc)
            ##        ls_id.append(st)

            #lost_students = list(zip(ls_id,quid,acc_list))
            #lost_students = np.array(lost_students)
            #print(lost_students)
            #print(lost_students.shape)
            #





            #                   


            #unique,counts = np.unique(temp,return_counts = True)
            #unique_stu2 = np.asarray((unique,counts)).T
            #print(unique_stu2)
       
            #print(len(new_list))
            #new_list = np.array(new_list)
            #final_2 =\
            #list(zip([st_final,qu_final,qu_cat_fianl,overall_2[:,2],overall_2[:,3],new_list,predicament]))
            #final_2 = np.array(final_2)
            #final_2 = np.transpose(final_2)

            #print(final)
            #print(final_2.shape)
            #print(len(st_accu))



            #with open('bodhidata.pkl','wb') as fi:
            #    pickle.dump(final,fi)

            

                                
                                





 
                
            #for i in all_categories:
            #    quests = SSCquestions.objects.filter(section_category =
            #                                         'General-Intelligence',topic_category =
            #                                         i)
            #    print('%s quests len---%s topic' %(len(quests),i))
            #    for j in quests:
            #        r_ans = 0
            #        w_ans = 0
            #        s_ans = 0

            #        online_marks =\
            #            SSCOnlineMarks.objects.filter(test__sscquestions=j,test__creator=
            #                                         teach.teacheruser)

            #        if len(online_marks) != 0:
            #            for qid in online_marks:
            #                if j.id in qid.skippedAnswers:
            #                    s_ans = s_ans + 1
            #                else:
            #                    for ch in j.choices_set.all():
            #                        if ch.id in qid.rightAnswers:
            #                            r_ans = r_ans + 1
            #                        if ch.id in qid.wrongAnswers:
            #                            w_ans = w_ans + 1
            #        try:
            #            accuracy = ((r_ans-w_ans)/(r_ans+w_ans))*100
            #            print('%s--%s---%s' %(j.id,accuracy,s_ans))
            #        except:
            #            accuracy = None
            #            print('%s--%s---%s' %(j.id,accuracy,s_ans))


                




            #print('%s - tests taken' %len(online_marks))
            #tests = []
            #for i in online_marks:
            #    tests.append(i.test)
            #quests = []
            #for n,i in enumerate(tests):
            #    for q in i.sscquestions_set.all():
            #        quests.append(q)
            #for i in quests:
            #    print(i.text)
    pass
                
                
def change_question_marks(subject):
    questions = SSCquestions.objects.filter(section_category = subject)
    for i in questions:
        i.max_marks = int(1)
        i.negative_marks = 0
        i.save()

def delete_concepts():
    concepts = Concept.objects.all()
    for i in concepts:
        i.delete()

def add_concepts():
    df =\
    pd.read_csv('/app/question_data/helper/si_categories.csv')
    quest_ids = df['question_id']
    cons = df['concept_id']
    overall = list(zip(quest_ids,cons))
    for i,j in overall:
        quest = SSCquestions.objects.get(id = i)
        if ',' in j:
            kk = j.split(',')
            for n in kk:
                c = Concepts.objects.get(concept_number = int(n))
                quest.concepts.add(c)
        else:
            c = Concepts.objects.get(concept_number = int(j))
            quest.concepts.add(c)

            print('{} normal'.format(j))

def howitworks(request):
    return render(request,'basicinformation/index3.html')

def showCourses(request):
    return render(request,'basicinformation/courses.html')

def redirectPlayStore(request):
    return render(request,'basicinformation/play_store_redirect.html')
    

