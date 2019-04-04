from rest_framework import generics
from django.utils import timezone
from celery.result import AsyncResult 
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from basicinformation.models import *
from django.http import Http404, HttpResponse
from .serializers import *
from QuestionsAndPapers.api.views import *
from learning.models import *
from basicinformation.marksprediction import *
from QuestionsAndPapers.models import * 
from basicinformation.models import * 
from basicinformation.marksprediction import * 
from membership.api.views import add_subjects
import json
import random
from basicinformation.nameconversions import *
from membership.api.serializers import *
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated
)
from basicinformation.tasks import *
import datetime
import time
from decimal import Decimal
from exponent_server_sdk import DeviceNotRegisteredError
from exponent_server_sdk import PushClient
from exponent_server_sdk import PushMessage
from exponent_server_sdk import PushResponseError
from exponent_server_sdk import PushServerError
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError



class StudentListAPIView(generics.ListAPIView):
    serializer_class = StudentModelSerializer
    def get_queryset(self):
        return Student.objects.all()

class StudentDetailAPIView(APIView):

    def get(self,request,format=None):
        user = self.request.user
        username = user.username
        email = user.email
        first_name = user.first_name
        me = Studs(user)
        school_name = me.profile.school.name
        subjects = me.my_subjects_names()

        my_details =\
        {'username':username,'email':email,'firstName':first_name,'school':school_name,'subjects':subjects}
        return Response(my_details)


class StudentShowDetialsAPIView(APIView):
    def get(self,request,format=None):
        aws_keys = AWSKey.objects.all()
        aws_key = aws_keys[0]

        try:
            my_profile = StudentDetails.objects.get(student = self.request.user)
            
            context =\
                    {'id':self.request.user.id,'fullName':my_profile.fullName,'phone':my_profile.phone,'address':my_profile.address,'email':my_profile.address,'fatherName':my_profile.fatherName,'parentPhone':my_profile.parentPhone,'photo_url':my_profile.photo,'language':my_profile.language,'course':my_profile.course,'accessKey':aws_key.accessKey,'secretKey':aws_key.secretKey}
            #serializer_student_profile =\
            #StudentProfileDetailsSerializer(my_profile)
            return Response(context)
        except Exception as e:
            print(str(e))
            context =\
                    {"id":None,"fullName":None,"phone":None,"address":None,"email":None,"fatherName":None,"parentPhone":None,"photo_url":None,'accessKey':aws_key.accessKey,'secretKey':aws_key.secretKey}
            return Response(context)


class StudentFillDetailsAPIView(APIView):
    def post(self,request,*args,**kwargs):
        name = request.POST['fullName']
        phone = request.POST['phone']
        address = request.POST['address']
        fatherName = request.POST['fathersName']
        parentPhone = request.POST['parentPhone']
        email = request.POST['email']
        photo_url = request.POST['photo_url']
        try:
            my_profile = StudentDetails.objects.get(student =
                                                    self.request.user)
        except:

            my_profile = StudentDetails()
        if parentPhone == "":
            parentPhone = None
        if email == "":
            email = 'none@none.com'

        my_profile.student = self.request.user
        my_profile.photo = photo_url
        my_profile.address = address
        my_profile.email = email
        my_profile.phone = phone
        my_profile.parentPhone = parentPhone
        my_profile.fatherName = fatherName
        my_profile.fullName = name
        my_profile.save()
        serialzer = StudentProfileDetailsSerializer(my_profile)
        return Response(serialzer.data)
        

#----------------------------------------------------------------------------------------
# Find out if student of teacher
class TeacherorStudentAPIView(APIView):
    def get(self,request,format = None):
        user = self.request.user
        user_type =user.groups.all()[0]
        user_type = user_type.name
        context = {'userType':user_type}
        return Response(context)
# ALL TEACHER APIs

#----------------------------------------------------------------------------------------
# returns the details about the last test created by teacher.

class LastClassTestPerformanceTeacherAPI(APIView):
    def get(self,request,format = None):
        #me = Teach(self.request.user)
        new_test =\
        SSCKlassTest.objects.filter(creator=self.request.user).order_by('published')[0]
        counter = 0
        quest_marks = 0
        test_id = new_test.id
        for quest in new_test.sscquestions_set.all():
            counter = counter + 1
            quest_marks = quest_marks + quest.max_marks

        publised_date = new_test.published
        subject = new_test.sub
        my_tests = SSCOnlineMarks.objects.filter(test__creator =
                                                 self.request.user,test
                                                 =new_test )
        marks = []
        for test in my_tests:
            marks.append((test.marks/test.test.max_marks)*100)
        info =\
                {'subject':subject,'date':publised_date,'test_takers':len(my_tests),'marks':marks,'num_questions':counter,'test_id':test_id}
        return Response(info)

#---------------------------------------------------------------------------------------

# returns the names of  weak areas by subject and batch taught by the teacher.
class TeacherWeakAreasBrief(APIView):
    def get(self,request,format=None):
        me = Teach(self.request.user)
        subjects = me.my_subjects_names()
        weak_subs_areas_dict = []
        teach_klass = TeacherClasses.objects.filter(teacher=me.profile)
        klasses = []
        if len(teach_klass) != 0:
            for kl in teach_klass:
                klasses.append(kl.klass)
        else:
            klasses = me.my_classes_names()
            for kl in klasses:
                new_teach_klass = TeacherClasses()
                new_teach_klass.teacher = me.profile
                new_teach_klass.klass = kl
                new_teach_klass.numStudents = 0
                new_teach_klass.save()


        #weak_ar = teacher_home_weak_areas.delay(self.request.user.id)
        weak_ar = teacher_home_weak_areas(self.request.user.id)
        #print(weak_ar)
        #te_id = weak_ar.task_id
        #res = AsyncResult(te_id)

        #klasses,subjects = res.get()

        weak_links = {}
        weak_klass = []
        weak_subs = []
        subs = []
        try:
            for sub in subjects:
                for i in klasses:
                    try:
                        weak_links[i]= \
                        me.online_problematicAreasNames(self.request.user,sub,i)
                        kk = me.online_problematicAreasNames(self.request.user,sub,i)
                        kk = kk.tolist()
                        weak_subs.append(weak_links[i])

                        weak_klass.append(i)
                        subs.append(sub)


                        #print(weak_links)
                        #print(weak_subs)
                    except Exception as e:
                        print(str(e))
            weak_subs_areas = list(zip(subs,weak_klass,weak_subs))
            #weak_subs_areas = None
        except:
            weak_subs_areas = None


        return Response(weak_subs_areas)

#---------------------------------------------------------------------------------------


# returns the names of  weak areas by subject and batch taught by the teacher.
class TeacherWeakAreasBriefAndroid(APIView):
    def get(self,request,format=None):
        res = TeacherWeakAreasBriefAsync.delay(self.request.user.id)
        te_id = res.task_id
        res_final = AsyncResult(te_id)
        ars = res_final.get()
        ars_encode = bytes(ars,'utf-8')
        ars_dict = pickle.loads(ars_encode)
        return Response(ars_dict)








#---------------------------------------------------------------------------------------


# returns details about last few tests given out by the teacher(eg. date
# published,total marks,subject,class,number of students who have taken the
# test etc...)


class TeacherTestsOverview(APIView):
    def get(self,request,format=None):
        new_test = SSCKlassTest.objects.filter(creator =
                                               self.request.user).order_by('published')[:3]
        test_details = {}
        max_marks = 0
        for test in new_test:
            max_marks = test.max_marks
            counter = len(test.sscquestions_set.all())
            student_marks = SSCOnlineMarks.objects.filter(test = test)
            taken_students = len(student_marks)
            all_marks = []
            for stu in student_marks:
                all_marks.append((stu.marks/max_marks)*100)
            try:
                average_marks = sum(all_marks)/len(all_marks)
            except:
                average_marks = 0


            test_details[test.id] =\
                    {'published':test.published,'num_questions':counter,'total_marks':max_marks,'class':test.klas.name,'subject':test.sub,'average':round(average_marks,2),'students_taken':taken_students}
        return Response(test_details)




#-------------------------------------------------------------------
class TeacherTestsOverviewAndroid(APIView):
    def get(self,request,format=None):
        new_test = SSCKlassTest.objects.filter(creator =
                                               self.request.user).order_by('published')[:3]
        test_details = {}
        max_marks = 0
        all_details = []
        for test in new_test:
            max_marks = test.max_marks
            counter = len(test.sscquestions_set.all())
            student_marks = SSCOnlineMarks.objects.filter(test = test)
            taken_students = len(student_marks)
            all_marks = []
            for stu in student_marks:
                all_marks.append((stu.marks/max_marks)*100)
            try:
                average_marks = sum(all_marks)/len(all_marks)
            except:
                average_marks = 0


            test_details =\
                    {'testid':test.id,'published':test.published,'num_questions':counter,'total_marks':max_marks,'class':test.klas.name,'subject':test.sub,'average':round(average_marks,2),'students_taken':taken_students}
            all_details.append(test_details)
        return Response(all_details)


#-------------------------------------------------------------------

# Show hard questions in a test of all tests


#This has been put into celery#
class TeachersHardQuestionsAPIView(APIView):
    def get(self,request,format=None):
        res = TeacherHardQuestionsAsync.delay(self.request.user.id)
        res_id = res.task_id
        quest = AsyncResult(res_id)
        questions = quest.get()
        return Response(questions)

class TeachersHardQuestions3TestsAPIView(APIView):
    def get(self,request,format=None):
        res = TeacherHardQuestionsLast3TestsAsync.delay(self.request.user.id)
        res_id = res.task_id
        quest = AsyncResult(res_id)
        questions = quest.get()
        return Response(questions)




#-------------------------------------------------------------------

class TeacherSubjectsAPIView(APIView):
    def get(self,request,format=None):
        me = Teach(self.request.user)
        subjects = me.my_subjects_names()
        sub_dict = {'subjects':subjects}
        return Response(sub_dict)

class TeacherBatchesAPIView(APIView):
    def get(self,request,format=None):
        me = Teach(self.request.user)
        klasses = me.my_classes_names()
        class_dict = {'Batches':klasses}
        return Response(class_dict)
#-------------------------------------------------------------------
# APIs for teacher performance

class TeacherSelectionAPIView(APIView):
    def post(self,request,*args,**kwargs):
        if 'onlineTestAnalysis' in request.POST:
            which_klass = request.POST['onlineTestAnalysis']
            sub = bring_teacher_subjects_analysis.delay(user.id)
            te_id = sub.task_id
            res = AsyncResult(te_id)
            subs = res.get()
            context = {'subs': subs, 'which_class': which_klass}
            return Response(context)
class TeacherSubjectAPIView(APIView):
    def post(self,request,*args,**kwargs):
        if 'onlineschoolSubject' in request.POST:
            onlineSubject = request.POST['onlineschoolSubject']
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
            return Response(context)
class TeacherTestAnalysisAPIView(APIView):
    def post(self,request,*args,**kwargs):
        if 'onlinetestid' in request.POST:
            test_id = request.POST['onlinetestid']
            me = Teach(self.request.user)
            # get the number of students who took test
            test_object = SSCKlassTest.objects.get(id = test_id)
            online_marks =\
            SSCOnlineMarks.objects.filter(test = test_object,student__school =
                                          me.profile.school)


            all_marks = []
            all_students = []
            test_max_marks = test_object.max_marks
            for om in online_marks:
                all_marks.append(om.marks)
                all_students.append(om.student)
            marks_student = list(zip(all_students,all_marks))
            grade_s = 0 
            grade_a = 0
            grade_b = 0
            grade_c = 0
            grade_d = 0
            grade_e = 0
            for am in all_marks:
                percentage = am / test_max_marks
                if percentage >= 90:
                    grade_s += 1
                elif 80 <= percentage < 90:
                    grade_a += 1
                elif 70 <= percentage < 80:
                    grade_b += 1
                elif 60 <= percentage < 70:
                    grade_c += 1
                elif 50 <= percentage < 60:
                    grade_d += 1
                elif percentage < 50:
                    grade_e += 1
            marks_student = np.array(marks_student)
            sorted_ranked_marks = sorted(marks_student, key=lambda x:\
                                 x[1],reverse=True)
            rank_list = []
            count_rank = 1
            for i,j in sorted_ranked_marks:
                count_rank += 1
                ranked_dict = {'rank':count_rank,'student':i,'marks':j}
                rank_list.append(ranked_dict)
            hardest_question_id = []
            for om in online_marks:
                rightAnswers = om.rightAnswers
                wrongAnswers = om.wrongAnswers
                skippedAnwers = om.skippedAnswers
                for wa in wrongAnswers:
                    question = SSCquestions.objects.get(choices__id =wa)
                    hardest_question_id.append(question.id)
                for sa in skippedAnswers:
                    hardest_question_id.append(sa)
            unique, counts = np.unique(hardest_question_id, return_counts=True)
            hard_freq = np.asarray((unique, counts)).T
            sorted_hard_questions = sorted(hard_freq, key=lambda x:\
                                 x[1],reverse=True)
            hard_quest_final = []
            for i,j in sorted_hard_questions:
                quest = SSCquestions.objects.get(id = i)
                choices_list = []
                choices = quest.choices_set.all()
                for ch in choices:
                    ch_dict =\
                    {'predicament':ch.predicament,'text':ch.text,'picture':ch.picture,'explanation':ch.explanation,'explanationPicture':ch.explanationPicture}
                    choices_list.append(ch_dict)
                question = {'picture':quest.picture,'choices':choices_list}
                hard_quest_final.append(question)
            context = {'grade_s':grade_s,'grade_a':grade_a,'grade_b':grade_b,'grade_c':grade_c,
                       'grade_d':grade_d,'grade_e':grade_e,
                       'hardQuestions':hard_quest_final,'rank':rank_list,'len_test':len(online_marks)}
            return Response(context)


class TeacherTestSelectionAPIView(APIView):
    def post(self,request,*args,**kwargs):
        if 'onlinetestid' in request.POST:
            test_id = request.POST['onlinetestid']
            me = Teach(self.request.user)
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
                    asyn_rt = generate_testRankTable.delay(self.request.user.id,test_id)
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
                return Response(context)

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
                return response(context)
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
                return Response(context)

class GenerateRankTableAPIView(APIView):
    def post(self,request,*args,**kwargs):
        test_id = request.POST['onlinetestid']
        me = Teach(self.request.user)
        online_marks =\
        SSCOnlineMarks.objects.filter(test__id=test_id,student__school =
                                      me.profile.school)

    # try to get result table associated with particular test
        try:
            result = TestRankTable.objects.get(test__id = test_id)
    # if no new student has taken the test then simply sort the old rank table
            if len(result.names) == len(online_marks):
                result = me.combine_rankTable(result)
                return Response(result)

    # else generate new rank table, sort it and display it
            else:
                asyn_rt = generate_testRankTable.delay(user.id,test_id)
                result = 'None'
                while result is 'None':
                    try:
                        result = TestRankTable.objects.filter(test__id =\
                                                      test_id).order_by('-time')[0]
                        result = combine_rankTableDict(result)
                        return Response(result)

                    except Exception as e:
                        print(str(e))
    # if no result table is found associated to particular test then generate
    # new rank table, sort it and display it

        except:
            asyn_rt = generate_testRankTable.delay(self.request.user.id,test_id)
            result = 'None'
            while result is 'None':
                try:
                    result = TestRankTable.objects.filter(test__id =\
                                                  test_id).order_by('-time')[0]
                    result = me.combine_rankTableDict(result)
                    return Response(result)
                except Exception as e:
                    print(str(e))

class TeacherTestBasicDetailsAPIView(APIView):
    def post(self,request,*args,**kwargs):
        test_id = request.POST['onlinetestid']
        me = Teach(self.request.user)
        online_marks =\
        SSCOnlineMarks.objects.filter(test__id=test_id,student__school =
                                      me.profile.school)

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
            context =\
            {'maxMarks':max_marks,'average':average,'percent_average':percent_average,'grade_s':grade_s,'grade_a':grade_a,'grade_b':grade_b,'grade_c':grade_c,'grade_d':grade_d,'grade_e':grade_e,'grade_f':grade_f}
            return Response(context)
        saved_marks = result_loader.onlineMarks.all()
        if len(online_marks) == len(saved_marks):
            max_marks = result_loader.test.max_marks
            average = result_loader.average
            percent_average = result_loader.percentAverage
            grade_s = result_loader.grade_s
            grade_a = result_loader.grade_a
            grade_b = result_loader.grade_b
            grade_c = result_loader.grade_c
            grade_d = result_loader.grade_d
            grade_e = result_loader.grade_e
            grade_f = result_loader.grade_f
            context =\
            {'maxMarks':max_marks,'average':average,'percent_average':percent_average,'grade_s':grade_s,'grade_a':grade_a,'grade_b':grade_b,'grade_c':grade_c,'grade_d':grade_d,'grade_e':grade_e,'grade_f':grade_f}
            return Response(context)
        else:
            new_rl = teacher_test_analysis_already.delay(test_id,user.id)
            rl_id = new_rl.task_id
            max_marks = result_loader.test.max_marks
            average = result_loader.average
            percent_average = result_loader.percentAverage
            grade_s = result_loader.grade_s
            grade_a = result_loader.grade_a
            grade_b = result_loader.grade_b
            grade_c = result_loader.grade_c
            grade_d = result_loader.grade_d
            grade_e = result_loader.grade_e
            grade_f = result_loader.grade_f
            context =\
            {'maxMarks':max_marks,'average':average,'percent_average':percent_average,'grade_s':grade_s,'grade_a':grade_a,'grade_b':grade_b,'grade_c':grade_c,'grade_d':grade_d,'grade_e':grade_e,'grade_f':grade_f}
            return Response(context)

class TeacherTestQuestionsAPIView(APIView):
    def post(self,request,*args,**kwargs):
        test_id = request.POST['onlinetestid']
        me = Teach(self.request.user)
        # get the number of students who took test
        online_marks =\
        SSCOnlineMarks.objects.filter(test__id=test_id,student__school =
                                      me.profile.school)

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
            skipped_quests = new_rl.skipped
            skipped_freq = new_rl.skippedFreq
            sq = list(zip(skipped_quests,skipped_freq))
            freqQuests = new_rl.freqAnswersQuestions
            freqQuestsfreq = new_rl.freqAnswersFreq
            freq = list(zip(freqQuests,freqQuestsfreq))
            pro_quests = new_rl.problemQuestions
            pro_freq  = new_rl.problemQuestionsFreq
            problem_quests = list(zip(pro_quests,pro_freq))


        saved_marks = result_loader.onlineMarks.all()
        if len(online_marks) == len(saved_marks):
# case 2 : if no new student has taken the test then just load and display
# result_loder
            pro_quests = result_loader.problemQuestions
            pro_freq  = result_loader.problemQuestionsFreq
            problem_quests = list(zip(pro_quests,pro_freq))
            skipped_quests = result_loader.skipped
            skipped_freq = result_loader.skippedFreq
            sq = list(zip(skipped_quests,skipped_freq))
            freqQuests = result_loader.freqAnswersQuestions
            freqQuestsfreq = result_loader.freqAnswersFreq
            freq = list(zip(freqQuests,freqQuestsfreq))
        else:
            new_rl = teacher_test_analysis_already.delay(test_id,user.id)
            rl_id = new_rl.task_id
            pro_quests = result_loader.problemQuestions
            pro_freq  = result_loader.problemQuestionsFreq
            problem_quests = list(zip(pro_quests,pro_freq))
            skipped_quests = result_loader.skipped
            skipped_freq = result_loader.skippedFreq
            sq = list(zip(skipped_quests,skipped_freq))
            freqQuests = result_loader.freqAnswersQuestions
            freqQuestsfreq = result_loader.freqAnswersFreq
            freq = list(zip(freqQuests,freqQuestsfreq))


class TeacherWeakAreasDetailAPIView(APIView):
    def post(self,request,*args,**kwargs):
        req = request.POST['weakAreas']
        which_class = req.split(',')[0]
        which_sub = req.split(',')[1]
        user = request.user
        me = Teach(user)
        res = \
        me.online_problematicAreaswithIntensityAverage(user,which_sub,which_class)
        res = me.change_topicNumbersNamesWeakAreas(res,which_sub)
        timing,freq_timing = me.weakAreas_timing(user,which_sub,which_class)
        timing = me.change_topicNumbersNamesWeakAreas(timing,which_sub)
        context =\
        {'which_class':which_class,'probAreas':res,'timing':timing}
        return Response(context)




#-------------------------------------------------------------------
# ALL STUDENT APIs



# Helper functions for Students APIs
#-------------------------------------------------------------------
def get_subject(user):
    me = Studs(user)
    taken_tests =\
    SSCOnlineMarks.objects.filter(student=me.profile).order_by('testTaken')
    prev_performance = {}
    subjects = []
    for test in taken_tests:
        subjects.append(test.test.sub)
    subjects = list(unique_everseen(subjects))
    return subjects

#--------------------------------------------------------------------
# returns the marks of all the tests taken by student.

class StudentPreviousPerformanceBriefAPIView(APIView):
    def get(self,request,format=None):
        me = Studs(self.request.user)
        taken_tests =\
        SSCOnlineMarks.objects.filter(student=me.profile).order_by('-testTaken')
        prev_performance = {}
        subjects = []
        for test in taken_tests:
            subjects.append(test.test.sub)
        subjects = list(unique_everseen(subjects))
        for sub in subjects:
            marks = []
            date = []
            for test in taken_tests:
                if test.test.sub == sub:
                    percentage = (test.marks/test.test.max_marks)*100
                    marks.append(percentage)
                    date.append(test.testTaken)
                prev_performance[sub]  = {'marks':marks,'date':date}
        return Response(prev_performance)


#---------------------------------------------------------------------
#Same as above but for android

class StudentPreviousPerformanceBriefAndroidAPIView(APIView):
    def get(self,request,format=None):
        me = Studs(self.request.user)
        taken_tests =\
        SSCOnlineMarks.objects.filter(student=me.profile).order_by('testTaken')
        past_performance = []
        prev_performance = {}
        overall = {}
        subjects = []
        for test in taken_tests:
            subjects.append(test.test.sub)
        subjects = list(unique_everseen(subjects))
        for sub in subjects:
            marks = []
            date = []
            for test in taken_tests:
                if test.test.sub == sub :
                    percentage = (test.marks/test.test.max_marks)*100
                    marks.append(percentage)
                    date.append(test.testTaken)
                prev_performance= {'subject':sub,'marks':marks, 'date':date}
            past_performance.append(prev_performance)
        return Response(past_performance)

#---------------------------------------------------------------------

# Gets all the area proficiecy in all the subjects a student studies

class StudentTopicWiseProficiency(APIView):
    def get(self,request,format=None):
        me = Studs(self.request.user)
        subjects = get_subject(self.request.user)
        strong_areas = {}
        for subject in subjects:

            freq = me.weakAreas_IntensityAverage(subject)
            strongAreas = []
            strongFreq = []
            try:
               for i,j in freq:
                    strongAreas.append(str(i))
                    strongFreq.append(round(j,1))
            except Exception as e:
                print(str(e))
            #if freq == 0:
            #   context = {'noMistake':'noMistake'}
            #   return render(request,'basicinformation/student_weakAreas.html',context)
            # changing topic categories numbers to names
            freq_Names = me.changeTopicNumbersNames(freq,subject)

            skills = list(zip(strongAreas,strongFreq))
            skills_names = me.changeTopicNumbersNames(skills,subject)
            if skills_names == None:
                continue
            strong_areas[subject] = {'strongTopics':skills_names}
        return Response(strong_areas)

class StudentAccuracyBriefAPIView(APIView):
    def get(self,request,format=None):
        me = Studs(self.request.user)
        weak_areas_cache = StudentWeakAreasChapterCache.objects.filter(student = me.profile)
        context = []
        for wa in weak_areas_cache:
            subject = wa.subject
            chapter = wa.chapter
            subject_chapter = SubjectChapters.objects.get(subject =
                                                         subject,code
                                                         =float(chapter)) 
            chapter_name = subject_chapter.name
            accuracy = wa.accuracy
            weak_areas =\
                    {'subject':subject,'chapter':chapter_name,'accuracy':accuracy,'chapterName':chapter_name}
            context.append(weak_areas)
        return Response(context)

class StudentAccuracyDetailAPIView(APIView):
    def post(self,request,*args,**kwargs):
        me = Studs(self.request.user)
        data = request.data
        subject = data['subject']
        chapter = data['chapter']
        weak_areas_cache =\
        StudentWeakAreasChapterCache.objects.get(student=me.profile,subject
                                                    = subject, chapter =
                                                    chapter)
        accuracy = weak_areas_cache.accuracy
        totalRight = weak_areas_cache.totalRight
        totalWrong = weak_areas_cache.totalWrong
        totalSkipped = weak_areas_cache.totalSkipped
        skippedPercent = weak_areas_cache.skippedPercent
        totalAttempted = weak_areas_cache.totalAttempted
        context =\
        {'accuracy':accuracy,'totalRight':totalRight,'totalWrong':totalWrong,'totalSkipped':totalSkipped,'skippedPercent':skippedPercent,'totalAttempted':totalAttempted}
        return Response(context)

class StudentTopicWiseProficiencyAndroid(APIView):
    def get(self,request,format=None):
        me = Studs(self.request.user)
        subjects = get_subject(self.request.user)
        strong_areas = {}
        overall = []
        for subject in subjects:
            freq = me.weakAreas_IntensityAverage(subject)
            strongAreas = []
            strongFreq = []
            try:
               for i,j in freq:
                    strongAreas.append(str(i))
                    strongFreq.append(round(j,1))
            except Exception as e:
                print(str(e))
            if freq == 0:
               context = {'noMistake':'noMistake'}
               return render(request,'basicinformation/student_weakAreas.html',context)
            # changing topic categories numbers to names
            freq_Names = me.changeTopicNumbersNames(freq,subject)
            skills = list(zip(strongAreas,strongFreq))
            skills_names = me.changeTopicNumbersNames(skills,subject)
            if skills_names == None:
                continue
            strong_areas = {'subject':subject,'strongTopics':skills_names}
            overall.append(strong_areas)
        return Response(overall)


#---------------------------------------------------------------------

# Shows basic details of taken test by students

class StudentTakenTestsDetailsAPIView(APIView):
    def get(self,request,format=None):
        me = Studs(self.request.user)
        marks = SSCOnlineMarks.objects.filter(student=
                                              me.profile).order_by('-testTaken')[:5]
        marks_dic = {}
        all_marks = []
        #percent = []
        #attempted = []
        #right = []
        #wrong = []
        for m in marks:
            percent_calc = ((m.marks/m.test.max_marks)*100)
            percent = percent_calc
            attempted = (len(m.rightAnswers)+len(m.wrongAnswers))
            right = (len(m.rightAnswers))
            wrong = (len(m.wrongAnswers))
            published = m.testTaken
            time = m.timeTaken
            try:
                sub_logo = SubjectLogo.objects.get(name = m.test.sub)
                logo = sub_logo.logo2
            except:
                logo = None
            total_questions = len(m.test.sscquestions_set.all())
            marks_dic =\
                    {'subject':m.test.sub,'logo':logo,'percent':round(percent,1),'attempted':attempted,'rightAnswers':right,'wrongAnswers':wrong,'total_questions':total_questions,'published':published,'time':time,'testid':m.test.id,'answer_id':m.id}
            all_marks.append(marks_dic)

        return Response(all_marks)


#---------------------------------------------------------------------

# Show average time taken to solve a questions in each topic

class StudentAverageTimeTopicAPIView(APIView):
    def get(self,request,format=None):
        me = Studs(self.request.user)
        subjects = get_subject(self.request.user)
        #average_timing_dict = {}
        timing = []
        for subject in subjects:
            timing_areawise,freq_timer = me.areawise_timing(subject)
            freq_timer = me.changeTopicNumbersNames(freq_timer,subject)
            timing_names = me.changeTopicNumbersNames(timing_areawise,subject)
            timing.append(timing_names)
        return Response(timing)


#---------------------------------------------------------------------
class StudentAverageTimeTopicAndroidAPIView(APIView):
    def get(self,request,format=None):
        me = Studs(self.request.user)
        subjects = get_subject(self.request.user)
        average_timing_dict = {}
        timing = []
        for subject in subjects:
            timing_areawise,freq_timer = me.areawise_timing(subject)
            freq_timer = me.changeTopicNumbersNames(freq_timer,subject)
            timing_names = me.changeTopicNumbersNames(timing_areawise,subject)
            if timing_names == None:
                continue
            average_timing_dict =\
            {'subject':subject,'topics_timing':timing_names}
            timing.append(average_timing_dict)
        return Response(timing)


# Student performance API
#---------------------------------------------------------------------
class StudentPerformanceBatchesAPIView(APIView):
    def get(self,request,format=None):
        me = Teach(self.request.user)
        all_klasses = me.my_classes_names_cache()
        my_batches = {'myBatches':all_klasses}
        return Response(my_batches)

#---------------------------------------------------------------------
# TimeTable APIs
#---------------------------------------------------------------------
class TeacherTimeTableAPIView(APIView):
    def get(self,request,format=None):
        me = Teach(self.request.user)
        time_table = TimeTable.objects.filter(teacher = me.profile,active=True)
        serialzer =TimeTableModelSerializer(time_table,many=True)
        return Response(serialzer.data)


class TeacherTimeTableFirst(APIView):
    def get(self,request,format=None):
        me = Teach(self.request.user)
        batches = me.my_classes_names_cache()
        context = {'batches':batches}
        return Response(context)


class TeacherCreateTimeTable(APIView):
    def post(self,request,*args,**kwargs):
        me = Teach(self.request.user)
        date = request.POST['timetable_date']
        note = request.POST['timetable_note']
        timeStart = request.POST['timetable_timeStart']
        timeEnd = request.POST['timetable_timeEnd']
        batch = request.POST['timetable_batch']
        subject = request.POST['timetable_sub']
        time_table = TimeTable()
        date = datetime.datetime.strptime(date,"%m-%d-%Y")
        final_date = date.date()
        batch = klass.objects.get(school = me.my_school(),name=batch)
        my_subjects = me.my_subjects_names()
        time_table.batch = batch
        time_table.date = final_date
        time_table.timeStart = timeStart
        time_table.timeEnd = timeEnd
        time_table.note = note
        time_table.teacher = me.profile
        time_table.created = timezone.now()
        if subject in my_subjects:
            time_table.sub = subject
            time_table.save()
            body = "Your class is on " + str(date)
            title = "Class of " + str(subject)
            notification_create_timetable.delay(title,body,self.request.user.id,batch.name)
            serialzer = TimeTableModelSerializer(time_table)
            return Response(serialzer.data)
        else:
            context = {'error':'There was some error'}
            return Response(context)

class StudentShowTimeTableAPIView(APIView):
    def get(self,request,format=None):
        me = Studs(self.request.user)
        batch = me.get_batch()
        all_time_tables = []
        all_time_tables_serializer = []
        time_table = TimeTable.objects.filter(batch = batch)
        for time_tab in time_table:
            all_time_tables.append(TimeTableModelSerializer(time_tab).data)
        return Response(all_time_tables)


class StudentTestPerformanceDetailedAPIView(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        test_id = data['test_id']
        sub = data['subject']
        me = Studs(self.request.user)
        #visible_tests(test_id)
        try:
            test = SSCOfflineMarks.objects.get(student=me.profile, test__id=test_id)
            mode = 'offline'
        except:
            test = SSCOnlineMarks.objects.filter(student=me.profile,
                                                 test__id=test_id)[0]
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
                analysis = StudentTestAnalysis.objects.get(student =\
                                                           me.profile,test =te)
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
                test_serializer = SSCOnlineMarksSerializer(test)
                context = \
                    {'test': test_serializer.data, 'average': classAverage,
                     'percentAverage': classAveragePercent,
                     'my_percent': myPercent, 'percentile': myPercentile,
                     'allMarks': allKlassMarks,
                     'freq':\
                     freq,'topicTiming':timing,
                     'numberRight':numRight,'numberWrong':numWrong,'numberSkipped':numSkipped,'accuracy':overallAccuracy,'subjectwise_accuracy':subjectwise_acc,'tt':tt}
                return \
                    Response(context)




            except Exception as e:
                print(str(e))
                old_analysis = StudentTestAnalysis.objects.filter(student =\
                                                           me.profile,test =te)
                if len(old_analysis) > 1:
                    for i in old_analysis:
                        i.delete()

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
                test_serializer = SSCOnlineMarksSerializer(test)

                context = \
                    {'thistest': test_serializer.data, 'average': average, 'percentAverage': percent_average,
                     'my_percent': my_marks_percent, 'percentile': percentile, 'allMarks': all_marks,
                     'freq':\
                     freq,'student_type':student_type,'topicWeakness':weak_names,'topicTiming':timing,
                     'numberRight':ra,'numberWrong':wa,'numberSkipped':sp,'accuracy':accuracy,'subjectwise_accuracy':subjectwise_accuracy,'tt':tt}
                return \
                    Response(context)

class StudentFindMyRankAPIView(APIView):
    def get(self,request,format=None):
        me = Studs(self.request.user)
        my_tests = SSCOnlineMarks.objects.filter(student = me.profile)
        all_ids = []
        all_context = []
        for i in my_tests:
            all_ids.append(i.test.id)
        for teid in all_ids:
            context = me.find_my_rank(teid)
           
            all_context.append(context)
        if len(all_context) == 0:
            all_context = {'NoTest':"Please take at-least one test so that we can calculate your rank.\
            कृपया एक टेस्ट लीजिये ताकि हम आपकी रैंक पता लगा पायें "}
            return Response(all_context)
        else:
            return Response(all_context)


class TeacherShowAllStudentsAPIView(APIView):
    def get(self,request,format=None):
        me = Teach(self.request.user)

        my_students = Student.objects.filter(school = me.my_school())
        number_students = len(my_students)
        student_serializer = StudentModelSerializer(my_students,many=True)
        context =\
        {'students':student_serializer.data,'number_students':number_students}
        return Response(context)


class StudentAverageTimingDetailAPIView(APIView):
    def post(self,request,*args,**kwargs):
        me = Studs(self.request.user)

        subject = request.POST['subject']
        chapter = request.POST['chapter']
        average_timing = request.POST['average_timing']
        chapter = changeIndividualNumberNames(chapter,subject)
        result = me.student_weak_timing_details(me.profile.id,subject,chapter)
        context = {'result':result,'overall_average_timing':average_timing}
        return Response(context)

class StudentAverageTimingChapterWiseAPIView(APIView):
    def get(self,request,format=None):
        me = Studs(self.request.user)
        timing_cache = StudentAverageTimingDetailCache.objects.filter(student =
                                                                      me.profile)
        final_timing = []
        for tc in timing_cache:
            try:
                chapter_name = \
                    SubjectChapters.objects.get(subject=tc.subject,code=float(tc.chapter))
                c_name = chapter_name.name
                cache =\
                {'id':tc.id,'student':tc.student.id,'subject':tc.subject,'chapter':c_name,'rightAverage':tc.rightAverage,'wrongAverage':tc.wrongAverage,'totalAverage':tc.totalAverage,'rightTotalTime':tc.rightTotalTime,'wrongTotalTime':tc.wrongTotalTime,'rightTotal':tc.rightTotal,'wrongTotal':tc.wrongTotal,'totalAttemted':tc.totalAttempted}
            except Exception as e:
                continue
            final_timing.append(cache)
        return Response(final_timing)
        #timing_serializer =\
        #StudentTimingChapterwiseSerializer(timing_cache,many=True)
        #return Response(timing_serializer.data)



class TeacherAnalysisShowTestsAPIView(APIView):
    def post(self,request,*args,**kwargs):
        subject = request.POST['subject']
        batch = request.POST['batch']
        me = Teach(self.request.user)
        school = me.my_school()
        kl = klass.objects.get(name = batch,school = school)
        all_tests = SSCKlassTest.objects.filter(creator =
                                                self.request.user,sub =
                                                subject,klas = kl)
        all_ids = []
        all_dates = []
        all_test_dict = {}
        for i in all_tests:
            all_ids.append(i.id)
            all_dates.append(i.published)
        overall_list = list(zip(all_ids,all_dates))
        all_test_dict = {'ids':overall_list}
        return Response(all_test_dict)

class TeacherAnalysisIndividualSendStudentAPIView(APIView):
    def post(self,request,*args,**kwargs):
        test_id = request.POST['test_id']
        mark = SSCOnlineMarks.objects.filter(test__id = test_id)
        students = []
        for i in mark:
            serializer = StudentModelSerializer(i.student)
            students.append(serializer.data)
        context = {'students':students}

        return Response(context)


class TeacherAnalysisIndividualStudentAPIView(APIView):
    def post(self,request,*args,**kwargs):
        me = Teach(self.request.user)
        test_id = request.POST['test_id']
        student_id = request.POST['student_id']
        student = Student.objects.get(id = int(student_id))
        mark = SSCOnlineMarks.objects.get(test__id = test_id,student = student)
        serializer = SSCOnlineMarksSerializer(mark)
        return Response(serializer.data)

class StudentShowPerformanceSubjectsAPIView(APIView):
    def get(self,request,format=None):
        me = Studs(self.request.user)
        #subjects = me.my_taken_subjects()
        subjects = Subject.objects.filter(student = me.profile)
        subs = []
        for sub in subjects:
            subs.append(sub.name)
        context = {'subjects':subs}
        return Response(context)

class StudentShowPerformanceTestsAPIView(APIView):
    def post(self,request,*args,**kwargs):
        me = Studs(self.request.user)
        data = request.data

        subject = data['subject']
        tests = SSCOnlineMarks.objects.filter(student =
                                              me.profile,test__sub = subject)
        test_date = []
        test_id = []
        for i in tests:
            test_date.append(i.testTaken)
            test_id.append(i.test.id)

        test_details = list(zip(test_id,test_date))
        context = {'test_details':test_details}
        return Response(context)


class TeacherEditBatches(APIView):
    def get(self,request):
        me = Teach(self.request.user)
        batch_confirmations = StudentConfirmation.objects.filter(teacher =
                                                                 me.profile)
        serializer =\
        StudentConfirmationSerializer(batch_confirmations,many=True)
        return Response(serializer.data)



class TeacherEditBatchesSendBatch(APIView):
    def get(self,request):
        me = Teach(self.request.user)
        klass = me.my_classes_names_cache()
        context = {'klasses':klass}
        return Response(context)

class TeacherEditBatchSearch(APIView):
    def post(self,request,*args,**kwargs):
        name =request.POST['name']
        batch_confirmations =\
        StudentConfirmation.objects.filter(student__username__icontains = name)
        serialzer =\
        StudentConfirmationSerializer(batch_confirmations,many=True)
        return Response(serialzer.data)

class TeacherEditBatchesFinal(APIView):
    def post(self,request,*args,**kwargs):
        me = Teach(self.request.user)
        confirmation_list = request.POST['confirmation_list']
        answers = confirmation_list.split(',')
        inner = []
        outer = []
        tot = 0
        for n,a in enumerate(answers):
            a = a.replace('[','')
            a = a.replace(']','')
            val = a
            inner.append(val)
            if (n+1)%2 == 0:
                outer.append(list(inner))
                inner = []




        outer = np.array(outer)
        for i,j in outer:
            kl = klass.objects.get(name = j.strip(),school = me.profile.school)
            confirmation = StudentConfirmation.objects.get(id = int(i))
            confirmation.batch = kl
            confirmation.confirm = True
            confirmation.save()
            student_user = confirmation.student
            student = Student.objects.get(studentuser = student_user)
            student.klass = kl
            student.save()
            my_subjects = student.subject_set.all()
            for i in my_subjects:
                i.delete()

            try:
                custom_batch = CustomBatch.objects.get(klass = kl, teacher=me.profile)
                subjects = custom_batch.subjects
                for sub in subjects:
                    custom_sub =\
                    Subject(name=sub.strip(),student=student,teacher=me.profile)
                    custom_sub.save()
            except Exception as e:
                print(str(e))

                if kl.name == 'SSC' or kl.name == 'RailwayGroupD':
                    course = 'SSC'
                if kl.name == 'LocoPilot' or kl.name == 'Outer':
                    course = 'Loco'
                add_subjects_change_batch.delay(course,student.id,me.profile.id,kl.id)
            addOldTests.delay(student.id,me.profile.id,kl.id)
            context = {'success':'success'}

        return Response(context)

class CreateBatchAPIView(APIView):
    def get(self,request,*args,**kwargs):
        me = Teach(self.request.user)
        teachers = Teacher.objects.filter(school = me.profile.school)
        teacher_serializer = TeacherSerializer(teachers,many=True)
        subjects = me.my_subjects_names()

        context  = {'teachers':teacher_serializer.data,'subjects':subjects}
        return Response(context)

class CreateBatchFinalAPIView(APIView):
    def post(self,request,*args,**kwargs):
        me = Teach(self.request.user)
        teacher = request.POST['teacher_id']
        name = request.POST['batch_name']
        subjects = request.POST['subjects']
        subjects = subjects.split(',')
        sub_list = []
        for i in subjects:
            su = i.replace('[','')
            su = su.replace(']','')
            sub_list.append(su.strip())
        kl = klass()
        kl.level = 'SSC'
        final_name = name.replace(' ','')
        final_name_2 = final_name.replace('-','_')
        kl.name = final_name_2
        kl.school = me.profile.school
        kl.save()
        teacher = Teacher.objects.get(id = teacher)
        custom_batch = CustomBatch()
        custom_batch.klass = kl
        custom_batch.school = me.profile.school
        custom_batch.subjects = sub_list
        custom_batch.save()
        custom_batch.teacher.add(teacher)
        klass_cache = TeacherClasses()
        klass_cache.teacher = teacher
        klass_cache.klass = kl
        klass_cache.numStudents = 0
        klass_cache.save()
        teacher_serializer = TeacherSerializer(teacher)
        context =\
        {'name':name,'teacher':teacher_serializer.data,'subjects':subjects}
        return Response(context)



class checkAndroidUpdateAPIView(APIView):
    def post(self,request,*args,**kwargs):
        package_name = request.POST['package_name']
        version_code = request.POST['version_code']
        return None
        entry = AndroidAppVersion.objects.filter(package_name =
                                                 package_name).order_by('time')
        new_version = False
        if len(entry) != 0:
            for i in entry:
                if int(version_code) < i.version_code:
                    new_version = True
                    context = {'new_version':new_version}
                    return Response(context)
                elif int(version_code) == i.version_code:
                    return Response({'new_version':False})
            new_entry = AndroidAppVersion()
            new_entry.package_name = package_name
            new_entry.time = timezone.now()
            new_entry.version_code = version_code
            new_entry.save()
            for i in entry:
                i.delete()
            return Response({'new_version':False})


        else:
            new_entry = AndroidAppVersion()
            new_entry.package_name = package_name
            new_entry.time = timezone.now()
            new_entry.version_code = version_code
            new_entry.save()
            return Response({'new_version':False})

class DeleteBadTestsAPIView(APIView):
    def get(self,request,format=None):
        deleteBadTests.delay()
        return Response({'deleted':'success'})


class StudentFilledProfileAPIView(APIView):
    def get(self,request,fromat=None):
        try:
            profile = StudentDetails.objects.get(student = self.request.user)
            phone = profile.phone
            if phone == '' or phone is None:
                return Response({'filled':False})
            else:
                return Response({'filled':True})
        except Exception as e:
            print(str(e))
            return Response({'filled':False})


class TeacherStudentProfileDetailAPIView(APIView):
    def post(self,request,*args,**kwargs):
        student_id = request.POST['student_id']
        me = Teach(self.request.user)
        student = Student.objects.get(id = student_id)
        student_user = student.studentuser
        try:
            profile = StudentDetails.objects.get(student = student_user)
            serializer = StudentProfileDetailsSerializer(profile)
            context ={'details':serializer.data}
            return Response(context)
        except:
            context = {'details':'No profile'}
            return Response(context)

class StudentAllWeakAreasAPIView(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        me = Studs(self.request.user)
        subject = data['subject']
        try:
            weak_areas_cache =\
            StudentWeakAreasChapterCache.objects.filter(student=me.profile,subject
                                                        = subject)
        except:
            context=\
            {'chapter':None,'accuracy':None,'totalRight':None,'totalWrong':None,'totalSkipped':None,'skippedPercent':None,'totalAttempted':None}
            return Response(context)
        weak_areas = []
        for i in weak_areas_cache:
            accuracy = i.accuracy
            totalRight = i.totalRight
            totalWrong = i.totalWrong
            totalSkipped = i.totalSkipped
            skippedPercent = i.skippedPercent
            totalAttempted = i.totalAttempted
            try:
                chapter_name_table = SubjectChapters.objects.get(subject =
                                                             subject,code =
                                                             float(i.chapter))
            except:
                continue
            chapter_name = chapter_name_table.name

            context =\
                    {'chapter':chapter_name,'accuracy':accuracy,'totalRight':totalRight,'totalWrong':totalWrong,'totalSkipped':totalSkipped,'skippedPercent':skippedPercent,'totalAttempted':totalAttempted}
            weak_areas.append(context)
        return Response(weak_areas)


class StudentProgressBriefAPIView(APIView):
    def get(self,request):
        me = Studs(self.request.user)
        progress_cache = StudentProgressChapterCache.objects.filter(student=
                                                                    me.profile)
        progress_list = []
        for pr in progress_cache:
            chapter = SubjectChapters.objects.get(subject = pr.subject,code =
                                                  pr.chapter)
            chapter_name = chapter.name
            pr_dict =\
                    {'subject':pr.subject,'chapter_code':pr.chapter,'chapter':chapter_name,'marks':pr.marks,'dates':pr.dates}
            progress_list.append(pr_dict)

        return Response(progress_list)

class StudentProgressChapterDetailAPIView(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        chapter = data['chapter']
        subject = data['subject']
        me = Studs(self.request.user)
        progress_cache = StudentProgressChapterCache.objects.get(subject =
                                                                    subject,chapter=chapter,student=me.profile)
        context =\
        {'marks':progress_cache.marks,'rightPercent':progress_cache.rightPercent,'wrongPercent':progress_cache.wrongPercent,
         'rightTime':progress_cache.rightTime,'wrongTime':progress_cache.wrongTime,'skippedPercent':progress_cache.skippedPercent,'totalRight':progress_cache.totalRight,
         'totalWrong':progress_cache.totalWrong,'totalSkipped':progress_cache.totalSkipped,'dates':progress_cache.dates}
        return Response(context)


class StudentProgressDetailAPIView(APIView):
    def post(self,request,*args,**kwargs):
        subject = request.POST['subject']
        me = Studs(self.request.user)
        progress_cache = StudentProgressChapterCache.objects.filter(student =
                                                                    me.profile,subject
                                                                    = subject)
        progress_list = []
        for pr in progress_cache:
            chapter = SubjectChapters.objects.get(subject = pr.subject,code =
                                                  pr.chapter)
            chapter_name = chapter.name

            context =\
                    {'chapter':chapter_name,'marks':pr.marks,'rightPercent':pr.rightPercent,'wrongPercent':pr.wrongPercent,
             'rightTime':pr.rightTime,'wrongTime':pr.wrongTime,'skippedPercent':pr.skippedPercent,'totalRight':pr.totalRight,
             'totalWrong':pr.totalWrong,'totalSkipped':pr.totalSkipped,'dates':pr.dates}
            progress_list.append(context)
        return Response(progress_list)

class TeacherAddQuestionImageAPIView(APIView):
    def post(self,request,*args,**kwargs):
        me = Teach(self.request.user)
        image_url = request.POST['image_url']
        subject = request.POST['subject']
        chapter = request.POST['chapter']
        correct_option = request.POST['correct']
        max_marks = request.POST['max_marks']
        negative_marks = request.POST['negative_marks']
        opt_num = request.POST['numberOptions']
        lang = request.POST['lang']
        direction = request.POST['direction']
        quest = SSCquestions()
        quest.picture = image_url
        if direction != "":
            quest.text = direction.strip()
        quest.section_category = subject
        quest.topic_category = chapter
        quest.max_marks = int(max_marks)
        quest.negative_marks = float(negative_marks)
        quest.language = lang
        quest.save()
        quest.school.add(me.profile.school)
        opt_num = int(opt_num)
        for i in range(opt_num):
            choice = Choices()
            choice.sscquest = quest
            if i == 0:
                choice.text = 'A'
            elif i == 1:
                choice.text = 'B'
            elif i == 2:
                choice.text = 'C'
            elif i == 3:
                choice.text = 'D'
            elif i == 4:
                choice.text = 'E'
            if i == 0 and correct_option == 'A':
                choice.predicament = 'Correct'
            elif i == 1 and correct_option == 'B':
                choice.predicament = 'Correct'
            elif i == 2 and correct_option == 'C':
                choice.predicament = 'Correct'
            elif i == 3 and correct_option == 'D':
                choice.predicament = 'Correct'
            elif i == 4 and correct_option == 'E':
                choice.predicament = 'Correct'
            else:
                choice.predicament = 'Wrong'

            choice.save()

        try:
            new = request.POST['new']
            serializer = SSCQuestionSerializerNew(qu,many=True)
        except Exception as e:

            serializer = SSCQuestionSerializer(quest)
        context = {'question':serializer.data}

        return Response(context)

class TeacherUploadTextQuestionAPIView(APIView):
    def post(self,request,*args,**kwargs):
        me = Teach(self.request.user)
        text = request.POST['text']
        optA = request.POST['optA']
        optB = request.POST['optB']
        optC = request.POST['optC']
        optD = request.POST['optD']
        optE = request.POST['optE']
        list_options = []
        list_options.append(optA)
        list_options.append(optB)
        list_options.append(optC)
        list_options.append(optD)
        list_options.append(optE)
        correct = request.POST['correct']
        max_marks = request.POST['max_marks']
        negative_marks = request.POST['negative_marks']
        subject = request.POST['subject']
        chapter = request.POST['chapter']
        num_options = request.POST['number_options']
        lang = request.POST['lang']
        quest = SSCquestions()
        quest.text = text.strip()
        quest.section_category = subject
        quest.topic_category = chapter
        quest.max_marks = int(max_marks)
        quest.negative_marks = Decimal(negative_marks)
        quest.language = lang
        quest.save()
        quest.school.add(me.profile.school)
        num_options = int(num_options)
        for opt in range(num_options):
            choice = Choices()
            choice.text = list_options[opt]
            if opt == 0 and correct == 'A':
                choice.predicament == 'Correct'
            elif opt == 1 and correct == 'B':
                choice.predicament == 'Correct'
            elif opt == 2 and correct == 'C':
                choice.predicament == 'Correct'
            elif opt == 3 and correct == 'D':
                choice.predicament == 'Correct'
            elif opt == 4 and correct == 'E':
                choice.predicament == 'Correct'
            else:
                choice.predicament = 'Wrong'
            choice.save()
        try:
            new = request.POST['new']
            serializer = SSCQuestionSerializerNew(qu,many=True)
        except Exception as e:

            serializer = SSCQuestionSerializer(quest)
        context = {'question':serializer.data}

        return Response(context)


class get_username(APIView):
    def get(self,request):
        user = self.request.user
        username = user.username
        context = {'username':username}
        return Response(context)



class SetPrefferedLanguage(APIView):
    def post(self,request,*args,**kwargs):
        language = request.POST['language']
        student = Student.objects.get(studentuser = self.request.user)
        try:
            preffered_lang = PrefferedLanguage.objects.get(student = student)
        except:
            preffered_lang = PrefferedLanguage()
            preffered_lang.student = student
            preffered_lang.language = language
            preffered_lang.save()
        context = {'saved':'saved'}
        return Response(context)

class StudentCurrentBatchAPIView(APIView):
    def get(self,request):
        me = Studs(self.request.user)
        batch = me.get_batch()
        context = {'batch':batch.name}
        return Response(context)

class StudentTrackActivityAPIView(APIView):
    def post(self,request,*args,**kwargs):
        me = Studs(self.request.user)
        data = request.data
        all_data = data.POST['all_data']
        json_data = json.loads(all_data)
        accuracy_Data = json_data(['accuracy_Data'])
        averageTime_data = json_data(['averageTime_Data'])
        progress_data = json_data(['progress_Data'])
        student_track_data = StudentTapTracker()
        student_track_data.student = me.profile
        student_track_data.accuracyData = accuracyData
        student_track_data.averageTimeData = averageTime_data
        student_track_data.progress_data = progress_data
        student_track.save()
        context = {'tracking':json_data}
        return Response(context)


class StudentBookmarkQuestionAPIView(APIView):
    def post(self,request,*args,**kwargs):
        me = Studs(self.request.user)
        question_list = request.POST['bookmark_id']
        question_arr = question_list.split(',')
        for i in question_arr:
            if '[' in i:
                j = i.replace('[','')
            elif ']' in i:
                j = i.replace(']','')
            else:
                j = i
            question = SSCquestions.objects.get(id = int(j))
            bookmark = StudentBookMarkQuestion()
            bookmark.student = me.profile
            bookmark.question = question
            bookmark.save()
        context = {'bookmark':'successful'}
        return Response(context)

class ShowBookMarksQuestionsAPIView(APIView):
    def get(self,request):
        me = Studs(self.request.user)
        my_bookmarks = StudentBookMarkQuestion.objects.filter(student =
                                                              me.profile)
        serializer = BookmarkSerializer(my_bookmarks,many=True)
        context = {'bookmarks':serializer.data}
        return Response(context)

class QuizGameAPIView(APIView):
    def post(self,request,*args,**kwargs):
        me = Studs(self.request.user)
        subject = request.POST['subject']
        chapter = request.POST['chapter']
        questions = SSCquestions.objects.filter(section_category =
                                                subject,topic_category =
                                                chapter)
        quest = random.choice(questions)
        right_choice = None
        choices = quest.choices_set.all()
        for i in choices:
            if i.predicament == 'Correct':
                right_choice = i
        quest_serializer = SSCQuestionSerializer(quest)

        hint =\
        {'text':right_choice.text,'picture':right_choice.picture,'time':20}
        context ={'question':quest_serializer.data,'hint':hint}
        return Response(context)

class StudentLanguage(APIView):
    def post(self,request,*args,**kwargs):
        me = Studs(self.request.user)
        data = request.data
        language = data['language']
        #try:
        #    student_lang = StudentLanguage.objects.get(student =
        #                                                   me.profile)
        #    student_lang.language = language
        #    student_lang.save()
        #except:
        #    student_lang = StudentLanguage()
        #    student_lang.student = me.profile
        #    student_lang.language = language
        #    student_lang.save()
        try:
            student_details = StudentDetails.objects.get(student = self.request.user)
            student_details.language = language
            student_details.save()
        except:
            student_details = StudentDetails()
            student_details.student = self.request.user
            student_details.language = language
            student_details.save()

        return Response({'language':language})

class HomePageSubjects(APIView):
    def get(self,request):
        user = self.request.user
        me = Studs(user)
        subjects = Subject.objects.filter(student=me.profile)
        subjects_list = []
        subjects_logo_list = []
        subjects_logo_list2 = []
        for sub in subjects:
            try:
                subject_logo = SubjectLogo.objects.get(name = sub.name)
                logo = subject_logo.logo
                logo2 = subject_logo.logo2
                subjects_logo_list.append(logo)
                subjects_logo_list2.append(logo2)
            except:
                subjects_logo_list.append('No logo')
                subjects_logo_list2.append('No logo')

            subjects_list.append(sub.name)
        final_subject_list =\
        list(zip(subjects_list,subjects_logo_list,subjects_logo_list2))
        context = {'subjects':final_subject_list}
        return Response(context)

class ChangeStudentDetails(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        photo_url = data['photo']
        course = data['course']
        language = data['language']
        phone = data['phone']
        full_name = data['full_name']
        student_details = StudentDetails.objects.get(student=self.request.user)
        student_details.photo = photo_url
        student_details.fullName = full_name
        student_details.language = language
        student_details.course = course
        student_details.phone = phone
        student_details.save()
        return\
                Response({'course':course,'phone':phone,'full_name':full_name,'language':language,'photo_url':photo_url})


class getTestRank(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        test_id = data['test_id']
        final_rank_list = []
        try:
            klass_test = SSCKlassTest.objects.get(id = test_id)
            test_rank = TestRank.objects.get(test=klass_test)
        except:
            context = {'ranking':[]}
            return Response(context)
        sortedMarks = test_rank.sortedMarks
        sortedStudents = test_rank.students
        for rank_index,stud in enumerate(sortedStudents):
            try:
                st = Student.objects.get(id = stud)
            except:
                continue
            try:
                student_detail = StudentDetails.objects.get(student =
                                                        st.studentuser)
                photo_url = student_detail.photo
                finalPhoto = photo_url

            except:
                finalPhoto = None
            student_marks = SSCOnlineMarks.objects.get(student=st,test
                                                       =klass_test)
            rightAnswers = len(student_marks.rightAnswers)
            allAnswers = len(student_marks.allAnswers)
            accuracy = rightAnswers/ allAnswers



            student_wise_rank_dict =\
                    {'name':st.name,'photo':finalPhoto,'username':st.studentuser.username,'rank':int(rank_index+1),'score':sortedMarks[rank_index],'accuracy':accuracy,'questionAttempted':allAnswers,'right':rightAnswers}
            final_rank_list.append(student_wise_rank_dict)
        #final_rank =\
        #list(zip(student_name_list,student_photo_list,student_rank_list,student_score_list,student_username_list))
        context = {'ranking':final_rank_list}
        return Response(context)



class getTestRankPaginated(APIView):
    def post(self,request,*args,**kwargs):
        me = Studs(self.request.user)
        data = request.data
        test_id = data['test_id']
        next_index = data['index']
        direction = data['direction']
 
        final_rank_list = []
        next_index = int(next_index)
        last_index = int(10)
        if direction == 'next':
            last_index = next_index + 14
        elif direction == 'prev':
            last_index = next_index  - 1
            next_index = last_index - 14
 
        try:
            klass_test = SSCKlassTest.objects.get(id = test_id)
            test_rank = TestRank.objects.get(test=klass_test)
        except:
            context = {'ranking':[]}
            return Response(context)

        sortedMarks = test_rank.sortedMarks
        sortedStudents = test_rank.students

        if next_index == 0:
            for rank_index,stud in enumerate(sortedStudents):
                if stud == me.profile.id:
                    my_rank = int(rank_index+1)
                    if my_rank > 5:
                        start_at = my_rank - 2
                    else:
                        start_at = 0
            try:
                if my_rank == None:
                    pass
            except:
                my_rank = 0
                start_at = 0

            for new_index,stud in\
                    enumerate(sortedStudents[start_at:my_rank+13]):
                try:
                    st = Student.objects.get(id = stud)
                except:
                    continue
                try:
                    student_detail = StudentDetails.objects.get(student =
                                                            st.studentuser)
                    photo_url = student_detail.photo
                    finalPhoto = photo_url

                except:
                    finalPhoto = None
                cal_rank = start_at + new_index + 1
                student_marks = SSCOnlineMarks.objects.get(student=st,test
                                                       =klass_test)

                rightAnswers = len(student_marks.rightAnswers)
                allAnswers = len(student_marks.allAnswers)
                accuracy = rightAnswers/ allAnswers
                student_wise_rank_dict =\
                    {'name':st.name,'photo':finalPhoto,'username':st.studentuser.username,'rank':cal_rank,'score':sortedMarks[new_index+start_at],'accuracy':accuracy,'questionAttempted':allAnswers,'right':rightAnswers}


                final_rank_list.append(student_wise_rank_dict)
            context = {'ranking':final_rank_list}
            return Response(context)



        for rank_index,stud in enumerate(sortedStudents[next_index:last_index]):
            try:
                st = Student.objects.get(id = stud)
            except:
                continue
            try:
                student_detail = StudentDetails.objects.get(student =
                                                        st.studentuser)
                photo_url = student_detail.photo
                finalPhoto = photo_url

            except:
                finalPhoto = None
            student_marks = SSCOnlineMarks.objects.get(student=st,test
                                                       =klass_test)

            rightAnswers = len(student_marks.rightAnswers)
            allAnswers = len(student_marks.allAnswers)
            accuracy = rightAnswers/ allAnswers

            cal_rank = next_index + rank_index + 1
            student_wise_rank_dict =\
                    {'name':st.name,'photo':finalPhoto,'username':st.studentuser.username,'rank':cal_rank,'score':sortedMarks[rank_index+start_at],'accuracy':accuracy,'questionAttempted':allAnswers,'right':rightAnswers}


            final_rank_list.append(student_wise_rank_dict)
        context = {'ranking':final_rank_list}
        return Response(context)







class getTakenTestsIds(APIView):
    def get(self,request):
        me = Studs(self.request.user)
        my_taken_marks = SSCOnlineMarks.objects.filter(student=me.profile)
        test_ids = []
        subjects = []
        subject_logo = []
        date = []
        test_details = []
        for t_marks in my_taken_marks:
            try:
                logo = SubjectLogo.objects.get(name = t_marks.test.sub)
                sub_logo = logo.logo2
            except:
                sub_logo = None
            subject_logo.append(sub_logo)
            test_detail =\
            {'test_id':t_marks.test.id,'subject':t_marks.test.sub,'logo':sub_logo,'date':t_marks.testTaken}
            test_details.append(test_detail)
        context =\
                    {'tests':test_details}
        return Response(context)


class printTestRank(APIView):
    def get(self,request):
        test_rank = TestRank.objects.all()
        test_ids = []
        for tr in test_rank:
            test_ids.append(tr.test.id)
        context = {'tests':test_ids}
        return Response(context)

#class setSubjectWiseRank(APIView):
#    def post(self,request,*args,**kwargs):
#        data = request.data
#        subject = data['subject']
#        all_subject_tests = SSCKlassTest.objects.filter(sub=subject)
#        student_accuracy = []
#        student_photo = []
#        student_name = []
#        student_username = []
#        for subjectTest in all_subject_tests:
#            all_subject_marks = SSCOnlineMarks.objects.filter(test =
#                                                              subjectTest)
#            for subjectMark in all_subject_marks:
#                #questions = SSCquestions.objects.filter(ktest = subjectTest)
#                rightAnswers = subjectMark.rightAnswers
#                wrongAnswers = subjectMark.wrongAnswers
#                countRightAnswers = 0
#                countWrongAnswers = 0
#                for ra in rightAnswers:
#                    question = SSCquestions.objects.get(choice__id = ra)
#                    if question.section_category == subject:
#                        countRightAnswers += 1
#                for wa in wrongAnswers:
#                    question = SSCquestions.objects.get(choice__id = wa)
#                    if question.section_category == subject:
#                        countWrongAnswers += 1
#                totalQuestionsAttempted = len(rightAnswers) + len(wrongAnswers)
#                accuracy = (countRightAnswers / totalQuestionsAttempted) * 100

class getSubjectRank(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        subject = data['subject']
        final_rank_list = []
        try:
            test_rank = SubjectRank.objects.get(subject=subject)
        except:
            context = {'subject':subject,'subject_ranking':{}}
            return Response(context)

        sortedMarks = test_rank.sortedAccuracies
        sortedStudents = test_rank.students
        sortedMinimumTests = test_rank.minimumTests

        for rank_index,stud in enumerate(sortedStudents):
            try:
                st = Student.objects.get(id = stud)
            except:
                continue
            try:
                student_detail = StudentDetails.objects.get(student =
                                                        st.studentuser)
                photo_url = student_detail.photo
                finalPhoto = photo_url

            except:
                finalPhoto = None
            student_cache =\
                SubjectAccuracyStudent.objects.get(student=st,subject=subject)
            totalQuestionAttempted = student_cache.totalAttempted
            totalQuestionsRight = student_cache.rightAnswers


            student_wise_rank_dict =\
                    {'name':st.name,'photo':finalPhoto,'username':st.studentuser.username,'rank':int(rank_index+1),'accuracy':sortedMarks[rank_index],'questionAttempted':totalQuestionAttempted,'right':totalQuestionsRight}
            final_rank_list.append(student_wise_rank_dict)
        #final_rank =\
        #list(zip(student_name_list,student_photo_list,student_rank_list,student_score_list,student_username_list))
        context = {'subject':subject,'subject_ranking':final_rank_list}
        return Response(context)


class getHomePageSubjectRank(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        subject = data['subject']
        final_rank_list = []
        try:
            test_rank = SubjectRank.objects.get(subject=subject)
        except:
            context = {'subject':subject,'subject_ranking':{}}
            return Response(context)
        sortedMarks = test_rank.sortedAccuracies
        sortedStudents =test_rank.students
        sortedMinimumTests = test_rank.minimumTests
        for rank_index,stud in enumerate(sortedStudents):
            if rank_index == 3:
                break
            try:
                st = Student.objects.get(id = stud)
            except:
                continue
            try:
                student_detail = StudentDetails.objects.get(student =
                                                        st.studentuser)
                photo_url = student_detail.photo
                finalPhoto = photo_url

            except:
                finalPhoto = None
            student_cache =\
                SubjectAccuracyStudent.objects.get(student=st,subject=subject)
            totalQuestionAttempted = student_cache.totalAttempted
            totalQuestionsRight = student_cache.rightAnswers


            student_wise_rank_dict =\
                    {'name':st.name,'photo':finalPhoto,'username':st.studentuser.username,'rank':int(rank_index+1),'accuracy':sortedMarks[rank_index],'questionAttempted':totalQuestionAttempted,'right':totalQuestionsRight}
            final_rank_list.append(student_wise_rank_dict)
        #final_rank =\
        #list(zip(student_name_list,student_photo_list,student_rank_list,student_score_list,student_username_list))
        context = {'subject':subject,'subject_ranking':final_rank_list}
        return Response(context)


class getSubjectRankPaginated(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        me = Studs(self.request.user)
        subject = data['subject']
        next_index = data['index']
        direction = data['direction']
        final_rank_list = []
        next_index = int(next_index)
        last_index = int(10)
        if direction == 'next':
            last_index = next_index + 14
        elif direction == 'prev':
            last_index = next_index  - 1
            next_index = last_index - 14
        try:
            test_rank = SubjectRank.objects.get(subject=subject)
        except:
            context = {'subject':subject,'subject_ranking':{}}
            return Response(context)

        sortedMarks = test_rank.sortedAccuracies
        sortedStudents = test_rank.students
        sortedMinimumTests = test_rank.minimumTests
        if next_index == 0:
            for rank_index,stud in enumerate(sortedStudents):
                if stud == me.profile.id:
                    my_rank = int(rank_index+1)
                    if my_rank > 5:
                        start_at = my_rank - 2
                    else:
                        start_at = 0
            try:
                if my_rank == None:
                    pass
            except:
                my_rank = 0
                start_at = 0

            for new_index,stud in\
                    enumerate(sortedStudents[start_at:my_rank+13]):
                try:
                    st = Student.objects.get(id = stud)
                except:
                    continue
                try:
                    student_detail = StudentDetails.objects.get(student =
                                                            st.studentuser)
                    photo_url = student_detail.photo
                    finalPhoto = photo_url

                except:
                    finalPhoto = None
                student_cache =\
                    SubjectAccuracyStudent.objects.get(student=st,subject=subject)
                totalQuestionAttempted = student_cache.totalAttempted
                totalQuestionsRight = student_cache.rightAnswers
                cal_rank = start_at + new_index + 1

                student_wise_rank_dict =\
                        {'name':st.name,'photo':finalPhoto,'username':st.studentuser.username,'rank':cal_rank,'accuracy':sortedMarks[start_at+new_index],'questionAttempted':totalQuestionAttempted,'right':totalQuestionsRight}
                final_rank_list.append(student_wise_rank_dict)
                #final_rank =\
                #list(zip(student_name_list,student_photo_list,student_rank_list,student_score_list,student_username_list))
            context = {'subject':subject,'subject_ranking':final_rank_list}
            return Response(context)



        for rank_index,stud in enumerate(sortedStudents[next_index:last_index]):
            try:
                st = Student.objects.get(id = stud)
            except:
                continue
            try:
                student_detail = StudentDetails.objects.get(student =
                                                        st.studentuser)
                photo_url = student_detail.photo
                finalPhoto = photo_url

            except:
                finalPhoto = None
            student_cache =\
                SubjectAccuracyStudent.objects.get(student=st,subject=subject)
            totalQuestionAttempted = student_cache.totalAttempted
            totalQuestionsRight = student_cache.rightAnswers
            cal_rank = next_index + rank_index + 1

            student_wise_rank_dict =\
                    {'name':st.name,'photo':finalPhoto,'username':st.studentuser.username,'rank':cal_rank,'accuracy':sortedMarks[rank_index+next_index],'questionAttempted':totalQuestionAttempted,'right':totalQuestionsRight}
            final_rank_list.append(student_wise_rank_dict)
        #final_rank =\
        #list(zip(student_name_list,student_photo_list,student_rank_list,student_score_list,student_username_list))
        context = {'subject':subject,'subject_ranking':final_rank_list}
        return Response(context)




class getSubjectLogo(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        subject = data['subject']
        subject_logo = SubjectLogo.objects.get(name=subject)
        logo_link = subject_logo.logo
        context = {'subject':subject,'logo':logo_link}
        return Response(context)



class getChapterRank(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        subject = data['subject']
        chapter_name = data['chapter_name']
        final_rank_list = []
        try:
            test_rank =\
            ChapterRank.objects.get(subject=subject,chapterCode=float(chapter_name))
        except:
            context = {'subject':subject,'subject_ranking':[]}
            return Response(context)


        sortedMarks = test_rank.sortedAccuracies
        sortedStudents = test_rank.students
        sortedMinimumTests = test_rank.minimumTests
        for rank_index,stud in enumerate(sortedStudents):
            st = Student.objects.get(id = stud)
            try:
                student_detail = StudentDetails.objects.get(student =
                                                        st.studentuser)
                photo_url = student_detail.photo
                finalPhoto = photo_url

            except:
                finalPhoto = None
            student_cache =\
                ChapterAccuracyStudent.objects.get(student=st,subject=subject,chapterCode=float(chapter_name))
            totalQuestionAttempted = student_cache.totalAttempted
            totalQuestionsRight = student_cache.rightAnswers


            student_wise_rank_dict =\
                    {'name':st.name,'photo':finalPhoto,'username':st.studentuser.username,'rank':int(rank_index+1),'accuracy':sortedMarks[rank_index],'questionAttempted':totalQuestionAttempted,'right':totalQuestionsRight,'chapter_name':test_rank.chapterName}
            final_rank_list.append(student_wise_rank_dict)
        context = {'subject':subject,'subject_ranking':final_rank_list}
        return Response(context)




class getChapterRankPaginated(APIView):
    def post(self,request,*args,**kwargs):
        me = Studs(self.request.user)
        data = request.data
        subject = data['subject']
        chapter_name = data['chapter_name']
        next_index = data['index']
        direction = data['direction']

        final_rank_list = []

        next_index = int(next_index)
        last_index = int(10)
        if direction == 'next':
            last_index = next_index + 14
        elif direction == 'prev':
            last_index = next_index  - 1
            next_index = last_index - 14

        try:
            test_rank =\
            ChapterRank.objects.get(subject=subject,chapterCode=float(chapter_name))
        except:
            context = {'subject':subject,'subject_ranking':[]}
            return Response(context)


        sortedMarks = test_rank.sortedAccuracies
        sortedStudents = test_rank.students
        sortedMinimumTests = test_rank.minimumTests


        if next_index == 0:
            for rank_index,stud in enumerate(sortedStudents):
                if stud == me.profile.id:
                    my_rank = int(rank_index+1)
                    if my_rank > 5:
                        start_at = my_rank - 2
                    else:
                        start_at = 0
            try:
                if my_rank == None:
                    pass
            except:
                my_rank = 0
                start_at = 0

            for new_index,stud in\
                    enumerate(sortedStudents[start_at:my_rank+13]):
                try:
                    st = Student.objects.get(id = stud)
                except:
                    continue
                try:
                    student_detail = StudentDetails.objects.get(student =
                                                            st.studentuser)
                    photo_url = student_detail.photo
                    finalPhoto = photo_url

                except:
                    finalPhoto = None
                cal_rank = start_at + new_index + 1

                student_cache =\
                    ChapterAccuracyStudent.objects.get(student=st,subject=subject,chapterCode=float(chapter_name))
                totalQuestionAttempted = student_cache.totalAttempted
                totalQuestionsRight = student_cache.rightAnswers

                student_wise_rank_dict =\
                    {'name':st.name,'photo':finalPhoto,'username':st.studentuser.username,'rank':cal_rank,'accuracy':sortedMarks[start_at+new_index],'questionAttempted':totalQuestionAttempted,'right':totalQuestionsRight,'chapter_name':test_rank.chapterName}
 
                final_rank_list.append(student_wise_rank_dict)

            context = {'subject':subject,'subject_ranking':final_rank_list}
            return Response(context)


        for rank_index,stud in enumerate(sortedStudents[next_index:last_index]):
            try:
                st = Student.objects.get(id = stud)
            except:
                continue
            try:
                student_detail = StudentDetails.objects.get(student =
                                                        st.studentuser)
                photo_url = student_detail.photo
                finalPhoto = photo_url

            except:
                finalPhoto = None

            student_cache =\
                ChapterAccuracyStudent.objects.get(student=st,subject=subject,chapterCode=float(chapter_name))
            totalQuestionAttempted = student_cache.totalAttempted
            totalQuestionsRight = student_cache.rightAnswers


            cal_rank = next_index + rank_index + 1
            student_wise_rank_dict =\
                    {'name':st.name,'photo':finalPhoto,'username':st.studentuser.username,'rank':cal_rank,'accuracy':sortedMarks[rank_index+next_index],'questionAttempted':totalQuestionAttempted,'right':totalQuestionsRight,'chapter_name':test_rank.chapterName}
 


            final_rank_list.append(student_wise_rank_dict)
        #final_rank =\
        #list(zip(student_name_list,student_photo_list,student_rank_list,student_score_list,student_username_list))
        context = {'subject':subject,'subject_ranking':final_rank_list}
        return Response(context)







class getStudentSubjectRankDetails(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        student_username = data['username']
        subject = data['subject']
        student_object = Student.objects.get(studentuser__username =
                                             student_username)
        try:
            student_details_object =\
            StudentDetails.objects.get(student=student_object.studentuser)
            student_photo = student_details_object.photo
            student_name = student_object.name
        except:
            student_photo = None
            student_name = student_object.name
        student_subjects = Subject.objects.filter(student = student_object)
        student_subject_cache =\
        SubjectAccuracyStudent.objects.get(subject=subject,student=student_object)
        questions_attempted = student_subject_cache.totalAttempted
        questions_right = student_subject_cache.rightAnswers
        questions_accuracy = student_subject_cache.accuracy
        context =\
        {'name':student_name,'photo':student_photo,'username':student_username,'subject':subject,'attempted':questions_attempted,'right':questions_right,'accuracy':questions_accuracy}
        return Response(context)



class getStudentSubjectAllRankDetails(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        student_username = data['username']
        student_object = Student.objects.get(studentuser__username =
                                             student_username)
        try:
            student_details_object =\
            StudentDetails.objects.get(student=student_object.studentuser)
            student_photo = student_details_object.photo
            student_name = student_object.name
        except:
            student_photo = None
            student_name = student_object.name
        student_subjects = Subject.objects.filter(student = student_object)
        all_subjects = []
        for sub in student_subjects:
            all_subjects.append(sub.name)
        details = []
        for sub in all_subjects:
            try:
                subject_logo =SubjectLogo.objects.get(name = sub)
                logo_url = subject_logo.logo
                student_subject_cache =\
                SubjectAccuracyStudent.objects.get(subject=sub,student=student_object)
                questions_attempted = student_subject_cache.totalAttempted
                questions_right = student_subject_cache.rightAnswers
                questions_accuracy = student_subject_cache.accuracy
                subject_details_dict =\
                        {'subject':sub,'logo':logo_url,'attempted':questions_attempted,'right':questions_right,'accuracy':questions_accuracy}
                details.append(subject_details_dict)
            except:
                continue
        context =\
                {'name':student_name,'photo':student_photo,'username':student_username,'details':details}
        return Response(context)


class deleteProfilePicture(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        old_url = data['old_url']
        context = {'old_url':old_url}
        return Response(context)

class getSubjectWiseGroupRank(APIView):
    def get(self,request):
        me = Studs(self.request.user)

        my_subjects = Subject.objects.filter(student=me.profile)
        details = []
        for sub in my_subjects:
            try:
                subject_rank = SubjectRank.objects.get(subject=sub.name)
                all_students = subject_rank.students
                rank = all_students.index(me.profile.id)
                rank = rank + 1
                group_size = 20
                which_group = (rank / group_size) 
                my_group = math.ceil(which_group)
                my_group_rank = (rank % group_size)
                try:
                    subject_logo = SubjectLogo.objects.get(name=sub.name)
                    logo_url = subject_logo.logo2
                except:
                    logo_url = None
                try:
                    group = GroupBadge.objects.get(group=my_group)
                    if my_group == 1:
                        group_name = 'Diamond'
                    elif my_group == 2:
                        group_name = 'Platinum'
                    elif my_group == 3:
                        group_name = 'Gold'
                    elif my_group == 4:
                        group_name = 'Silver'
                    elif my_group >=  5:
                        group_name = 'Bronze'
                    group_logo = group.logo
                except:
                    group_logo = None
                    group_name = None
                group_details =\
                        {'subject':sub.name,'group':group_name,'group_rank':my_group_rank,'totalRank':rank,'logo':logo_url,'group_logo':group_logo}
                details.append(group_details)
            except Exception as e:
                print('group rank {}'.format(str(e)))
        context = {'group_details':details}
        return Response(context)
class saveExpoToken(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        token = data['expoToken']
        me = Studs(self.request.user)
        try:
            expoToken = StudentExpoToken.objects.get(student = me.profile)
            expoToken.token = token
            expoToken.save()
            context = {'studentid':me.profile.id,'token':expoToken.token}
            return Response(context)


        except:
            expoToken = StudentExpoToken()
            expoToken.token = token
            expoToken.student = me.profile
            expoToken.save()
            context = {'studentid':me.profile.id,'token':token}
            return Response(context)

class expoNotification2(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        token = data['token']
        body = data['body']
        title = data['title']
        activity = data['activity']
        te_id = data['id']
        new_data = {"activity":activity,"id":te_id}
        data_send = json.dumps(new_data)
        r = requests.post('https://exp.host/--/api/v2/push/send',data={"to":  token,
                                                                       "title":title,
                                                                       "body":
                                                                       body,
                                                                       "sound":"default",
                                                                       "priority":"high",
                                                                       "data":data_send})
        
 
        return\
                Response({'token':token,'body':body,'title':title,'extra_data':data_send,'error':r.status_code})

class expoNotification(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        token = data['expoToken']
        message = data['message']
        #extra = {'to':token,'sound':'default','title':'title of the message','body':'this is the body'}
        extra = None
        try:
            response = PushClient().publish(
                PushMessage(to=token,
                            body=message,
                            data=extra,
                           title='Bodhi Notification',
                           priority='high',
                           sound='default',
                           ))
        except PushServerError as exc:
            # Encountered some likely formatting/validation error.
            rollbar.report_exc_info(
                extra_data={
                    'token': token,
                    'message': message,
                    'extra': extra,
                    'errors': exc.errors,
                    'response_data': exc.response_data,
                })
            raise
        except (ConnectionError, HTTPError) as exc:
            # Encountered some Connection or HTTP error - retry a few times in
            # case it is transient.
            rollbar.report_exc_info(
                extra_data={'token': token, 'message': message, 'extra': extra})
            raise self.retry(exc=exc)

        try:
            # We got a response back, but we don't know whether it's an error yet.
            # This call raises errors so we can handle them with normal exception
            # flows.
            response.validate_response()
        except DeviceNotRegisteredError:
            # Mark the push token as inactive
            from notifications.models import PushToken
            PushToken.objects.filter(token=token).update(active=False)
        except PushResponseError as exc:
            # Encountered some other per-notification error.
            rollbar.report_exc_info(
                extra_data={
                    'token': token,
                    'message': message,
                    'extra': extra,
                    'push_response': exc.push_response._asdict(),
                })
            raise self.retry(exc=exc)
        return Response({'notification':'sent'})

class RateTestAPIView(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        test_id = data['test_id']
        rating = data['rating']
        user = self.request.user
        me = Studs(user)
        test = SSCKlassTest.objects.get(id = test_id)
        try:
            test_rating = TestRating.objects.get(student = me.profile,test
                                                 =test)
            context =\
            {'rating':"False",'student':user.username,'test_id':test_id}
            return Response(context)
        except Exception as e:
            test_rating = TestRating()
            test_rating.test = test
            test_rating.student = me.profile
            test_rating.rating = int(rating)
            test_rating.save()
            context =\
                    {'rating':int(rating),'student':user.username,'test_id':test_id,'exception':str(e)}
            return Response(context)
 
 
class GetTestOverallRating(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        test_id = data['test_id']
        test = SSCKlassTest.objects.get(id = test_id)
        test_ratings = TestRating.objects.filter(test = test)
        total_ratings = len(test_ratings)
        ratings_list = []
        for tr in test_ratings:
            ratings_list.append(tr.rating)
            sum_ratings = sum(ratings_list)
            average_rating = sum_ratings / total_ratings
            context = {'testID':test_id,'averageRating':average_rating}
            return Response(context)

class GetNextExamDate(APIView):
    def get(self,request):
        data = request.data
        student_details = StudentDetails.objects.get(student =
                                                     self.request.user)
        course = student_details.course
        try:
            exam_date = NextExamDate.objects.get(course=course)
            date = exam_date.examDate
            date = str(date)
            date_date = date.split(' ')
            date_day = date_date[0]
            date_time = date_date[1]
            year = date_day.split('-')[0]
            month = date_day.split('-')[1]
            day = date_day.split('-')[2]
            hour = date_time.split(':')[0]
            minute = date_time.split(':')[1]
            final_day = {'year':year,'month':month,'day':day}
            final_time = {'hour':hour,'minute':minute}
            context =\
            {'course':course,'examDate':final_day,'examTime':final_time}
            return Response(context)
        except Exception as e:
            context = {'course':course,'examDate':'False','why':str(e),'examTime':final_time}
            return Response(context)


class TeacherGoLiveAPI(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        channel_id = data['channel_id']
        base_url =  'https://www.googleapis.com/'
        url =\
        'youtube/v3/search?order=date&part=snippet&channelId={}&maxResults=25&key=AIzaSyCJVAAmr4VLMyijGCE8l0mnswSH8GywJ-I'.format(channel_id)

        total_url = base_url + url
        r = requests.get(total_url)
        reply = r.text
        print('video url {}'.format(reply))
        rep = json.loads(reply)
        items = rep['items']
        title = items[0]
        video_url = title['id']['videoId']
        snippet = title['snippet']['liveBroadcastContent']
        TeacherGoLiveNotification.delay('New live\
                                        video',video_url,'Competition_Qualifiers','outer')
        context = {'content':video_url}
        return Response(context)
 
        #for i in range(4):
        #    r = requests.get(total_url)
        #    if r.status_code != 200:
        #        time.sleep(5)
        #        print('sleeping')
        #        continue
        #    else:
        #        try:
        #            print('video url, in reply')
        #            reply = r.text
        #            print('video url {}'.format(reply))
        #            rep = json.loads(reply)
        #            items = rep['items']
        #            title = items[0]
        #            video_url = title['id']['videoId']
        #            snippet = title['snippet']['liveBroadcastContent']
        #            if snippet == 'live':
        #                TeacherGoLiveNotification.delay('New live\
        #                                                video',video_url,'Competition_Qualifiers','outer')
        #                context = {'content':video_url}
        #                return Response(context)
        #            else:
        #                time.sleep(5)
        #                continue
        #        except Exception as e:
        #            print('video url error {}'.format(str(e)))
        #            context = {'content':str(e)}

        #context= {'context':None}
        #return Response(context)
            
class ChallengeStudent(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        challenged_username = data['username']
        me = Studs(self.request.user)
        student_two =\
        Student.objects.get(studentuser__username=challenged_username)
        try:
            newChallenge = StudentChallenge.objects.get(studentOne =
                                                    me.profile,studentTwo =
                                                    student_two)
            context = {'challenge':'True'}
        except:
            newChallenge = StudentChallenge()
            newChallenge.studentOne = me.profile
            newChallenge.studentTwo = student_two
            newChallenge.when = timezone.now()
            newChallenge.save()
            try:
                studentOneToken = StudentExpoToken.objects.get(student=me.profile)
                studentTwoToken = StudentExpoToken.objects.get(student=student_two)
                messageFrom =\
                'You have challenged {}. Good Luck !!'.format(student_two.name)
                messageTo = """You have been challenged by {} Don\'t worry we will help you win.We wish you good luck.""".format(me.profile.name)
                title = "Bodhi Challenge"
                stud_detail = StudentDetails.objects.get(student =
                                                         student_two.studentuser)
                stud_detail_one = StudentDetails.objects.get(student =
                                                         me.profile.studentuser)

                in_id =\
                {'username':student_two.studentuser.username,'photo':stud_detail.photo,'name':student_two.name}
                in_id2 =\
                {'username':me.profile.studentuser.username,'photo':stud_detail_one.photo,'name':me.profile.name}

                extra_data1 =\
                {'activity':'challenge','id':in_id}
                extra_data2 =\
                {'activity':'challenge','id':in_id2}

                sendExpoNotification2.delay(studentOneToken.token,messageFrom,title,custom_data=extra_data1)
                sendExpoNotification2.delay(studentTwoToken.token,messageTo,title,custom_data
                                           = extra_data2)
            except Exception as e:
                print(str(e))
            context = {'challenge':'Success'}

        return Response(context)

class GetChallengedStudents(APIView):
    def get(self,request):
        data = request.data
        me = Studs(self.request.user)
        challenged = StudentChallenge.objects.filter(studentOne = me.profile)
        my_challenges = StudentChallenge.objects.filter(studentTwo = me.profile)
        to_challenge_list = []
        from_challenge_list = []
        for i in challenged:
            to_challenged = i.studentTwo
            to_challenged_student = StudentDetails.objects.get(student =
                                                           to_challenged.studentuser)
            given_challenges =\
                    {'to':to_challenged_student.fullName,'photo':to_challenged_student.photo,'username':to_challenged.studentuser.username}
            to_challenge_list.append(given_challenges)
        for i in my_challenges:
            from_challenged = i.studentOne
            from_challenged_student = StudentDetails.objects.get(student =
                                                           from_challenged.studentuser)
 
            sent_challenges =\
            {'from':from_challenged_student.fullName,'photo':from_challenged_student.photo,'username':from_challenged.studentuser.username}
            from_challenge_list.append(sent_challenges)
        context = {'to_challenges':
                       to_challenge_list,'from_challenges':from_challenge_list}

        return Response(context)


#class SubjectRankingProgress(APIView):
#    def post(self,request,*args,**kwargs):
#        data = request.data
#        subject = data['subject']
#    ranking_key = str(my_student_id)+sub_acc.subject
#    aws_keys = AWSKey.objects.all()
#    aws_key = aws_keys[0]
#    ACCESS_KEY_ID = aws_key.accessKey
#    ACCESS_SECRET_KEY = aws_key.secretKey
#    try:
#        my_rank = np.where(sorted_ranked_marks[:,0] == my_student_id)[0]
#        print('before my_rank {}'.format(my_rank))
#        my_rank = my_rank[0]+1
#        print('key {}, my rank {}'.format(ranking_key,my_rank))
#    except:
#        my_rank = int(99)
#    try:
#        client = boto3.resource(
#        'dynamodb',
#        aws_access_key_id = ACCESS_KEY_ID,
#        aws_secret_access_key = ACCESS_SECRET_KEY,
#        region_name = 'ap-south-1'
#        )
#        table = client.Table('subjectranking1')
#        response = table.query(KeyConditionExpression=Key('student_id').eq(student_id))
#        for i in response['Items']:
#            dateTaken = i['dateTaken']
#            ranking = i['ranking']

class StudentTestPerformanceNew(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        test_id = data['test_id']
        sub = data['subject']
        me = Studs(self.request.user)
        test = SSCOnlineMarks.objects.get(student = me.profile,test__id = test_id)
        #old_analysis = StudentTestAnalysis.objects.filter(student =\
        #                                               me.profile,test =te)
        #if len(old_analysis) > 1:
        #    for i in old_analysis:
        #        i.delete()

        #analysis = StudentTestAnalysis()
        questions = []
        rightAnswers = test.rightAnswers
        wrongAnswers = test.wrongAnswers
        skippedAnswers = test.skippedAnswers
        
        for quest in test.test.sscquestions_set.all():
            text = quest.text
            picture = quest.picture
            section_category = quest.section_category
            chapter_category = quest.topic_category
            sub_chapter =\
            SubjectChapters.objects.get(subject=section_category,code =
                                        float(chapter_category))
            chapter_name = sub_chapter.name
            direction = quest.comprehension
            if direction != None:
                directionText = direction.text
                directionPicture = direction.picture
                direction_dict =\
                {'text':directionText,'picture':directionPicture}
            else:
                 direction_dict = \
                {'text':None,'picture':None}
            if quest.id in skippedAnswers:
                skipped = 'True'
            else:
                skipped = 'False'
            time_details = SSCansweredQuestion.objects.get(onlineMarks =
                                                           test,quest = quest)
            timeTaken = time_details.time
            choices = quest.choices_set.all()
            positive_marks = quest.max_marks
            negative_marks = quest.negative_marks
            choices_list = []
            selected_list = []
            correct_choice = []
            explanation = []
            for ch in choices:
                ch_text = ch.text
                ch_picture = ch.picture
                ch_id = ch.id
                if ch.id in rightAnswers or ch.id in wrongAnswers:
                    selected_list.append(ch.id)
                if ch.predicament == 'Correct':
                    correct_choice.append(ch.id)
                if ch.explanationPicture != None and ch.explanationPicture != '' or ch.explanation != None:
                    exp =\
                    {'text':ch.explanation,'picture':ch.explanationPicture}
                    explanation.append(exp)


                
                ch_dict =\
                        {'text':ch_text,'picture':ch_picture,'id':ch_id,'freq':0}
                choices_list.append(ch_dict)
            quest_dict =\
                    {'id':quest.id,'text':text,'picture':picture,'subject':section_category,'chapter':chapter_name,'direction':direction_dict,'choice':choices_list,'skipped':skipped,'selected':selected_list,'rightChoice':correct_choice,'timeTaken':timeTaken,'explanation':explanation,'positiveMarks':positive_marks,'negativeMarks':negative_marks}
            questions.append(quest_dict)



        my_marks_percent = (test.marks / test.test.max_marks) * 100
        average, percent_average = \
            me.online_findAverageofTest(test_id, percent='p')
        percentile, all_marks,same_marks,less_marks,more_marks = me.online_findPercentileDetail(test_id)
        percentile = percentile * 100

        all_marks = [((i / test.test.max_marks) * 100) for i in all_marks]

        freq_qu = me.online_QuestionPercentage(test_id)
        for qu in questions:
            ch = qu['choice']
            for c in ch:
                c_id = c['id']
                for i,j in freq_qu:
                    if c_id == i:
                        c['freq'] = j



        # converting test time seconds to hours and minutes
        test_totalTime = test.timeTaken
        hours = int(test_totalTime/3600)
        t = int(test_totalTime%3600)
        mins = int(t/60)
        seconds =int(t%60)
        if hours == 0:
            tt = '{}m {}s'.format(mins,seconds)
        if hours == 0 and mins == 0:
            tt = '{}s'.format(seconds)
        if hours > 0:
            tt = '{}h {}m {}s'.format(hours,mins,seconds)
        try:
            if tt:
                pass
        except:
            tt = None

        ra,wa,sp,accuracy = me.test_statistics(test_id)
        weak_areas = me.weakAreas_Intensity(sub,singleTest = test_id)
        weak_cat = []
        weak_acc = []
        weak_list = []
        for i,j in weak_areas:
            cat = \
            SubjectChapters.objects.get(subject=sub,code =
                                        float(chapter_category))
            weaknesses = {'subject':cat.name,'accuracy':j}
            weak_list.append(weaknesses)
 
        sk_weak = me.skipped_testwise(test_id,me.profile)
        area_timing,freq = me.areawise_timing(sub,test_id)
        weak_time_cat = []
        weak_time = []
        for k,v in area_timing:
            weak_time_cat.append(k)
            weak_time.append(v)
        subjectwise_accuracy = me.test_SubjectAccuracy(test_id)
        sub_weak = []
        sub_weak_acc = []
        for i,j in subjectwise_accuracy.items():
            sub_weak.append(i)
            sub_weak_acc.append(j)
        if sub == 'SSCMultipleSections':
            weak_names = weak_areas
            timing = area_timing
        else:
            weak_names = me.changeTopicNumbersNames(weak_areas,sub)
            timing = me.changeTopicNumbersNames(area_timing,sub)
        test_serializer = SSCOnlineMarksSerializer(test)
        attempted = len(rightAnswers) + len(wrongAnswers)
        numberRight = len(rightAnswers)
        numberWrong  = len(wrongAnswers)
        total_test_marks = test.test.max_marks
        my_marks = test.marks
        context = \
                { 'questions':questions,'average': average, 'percentAverage': percent_average,
             'my_percent': my_marks_percent, 'percentile': percentile,
                 'allMarks': all_marks,'topicWeakness':weak_list,
             'numberRight':ra,'numberWrong':wa,'numberSkipped':sp,'accuracy':accuracy,'tt':tt,
                 'sameMarks':same_marks+1,'lessMarks':less_marks,'moreMarks':more_marks,'attempted':attempted,'numberRight':numberRight,'numberWrong':numberWrong,'totalTestMarks':total_test_marks,'myMarks':my_marks,'totalTimeInt':test_totalTime}
        return \
            Response(context)


class GetPromoCode(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        me = Studs(self.request.user)
        code = data['code']
        phone = data['phone']
        try:
            promoCode = PromoCode.objects.get(student = me.profile)
            context = {"status":'False'}
        except:
            promoCode = PromoCode()
            promoCode.student = me.profile
            promoCode.code = str(code)
            promoCode.phone = str(phone)
            promoCode.date = timezone.now()
            promoCode.save()
            context = {'status':'True'}
        studentOneToken = StudentExpoToken.objects.get(student=me.profile)
        messageFrom =\
                'You have challenged {}. Good Luck !!'.format(student_two.name)
        messageTo = """Congratulations !! You have got 3 months free membership
        to BodhiAI""".format(me.profile.name)
        title = "Bodhi AI 3 month membership"
        custom_data = {'activity':'home','id':self.request.user.username}
        sendExpoNotification2.delay(studentOneToken.token,messageFrom,title,custom_data
                                   = custom_data)
 
        return Response(context)


class ChallengeSubjectRank(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        me = Studs(self.request.user)
        student_username = data['username']
        second_student = Student.objects.get(studentuser__username = student_username)
        try:
            challenge = StudentChallenge.objects.get(studentOne = me.profile,studentTwo = second_student)
        except:
            challenge = StudentChallenge.objects.get(studentOne =
                                                     second_student,studentTwo
                                                     = me.profile)
        my_subjects = Subject.objects.filter(student = me.profile)
        second_student_subjects = Subject.objects.filter(student=second_student)
        subjects = []
        for sub in my_subjects:
            for sub2 in second_student_subjects:
                if sub.name == sub2.name:
                    subjects.append(sub.name)
        final_rank = []
        for sub in subjects:
            try:
                test_rank = SubjectRank.objects.get(subject=sub)
            except:
                continue

            sortedMarks = test_rank.sortedAccuracies
            sortedStudents = test_rank.students
            sortedMinimumTests = test_rank.minimumTests
            student_wise_rank_dict = {}
            for rank_index,stud in enumerate(sortedStudents):
                student_wise_rank_dict['subject'] = sub
                if stud == me.profile.id:
                    try:
                        student_detail = StudentDetails.objects.get(student =
                                                                me.profile.studentuser)
                        photo_url = student_detail.photo
                        finalPhoto = photo_url

                    except:
                        finalPhoto = None
                    student_cache =\
                        SubjectAccuracyStudent.objects.get(student=me.profile,subject=sub)
                    totalQuestionAttempted = student_cache.totalAttempted
                    totalQuestionsRight = student_cache.rightAnswers

                    student_wise_rank_dict['student1'] =\
                            {'rank':int(rank_index+1),'accuracy':sortedMarks[rank_index],'questionAttempted':totalQuestionAttempted,'myRight':totalQuestionsRight}

                if stud == second_student.id:
                    try:
                        student_detail2 = StudentDetails.objects.get(student =
                                                                second_student.studentuser)
                        photo_url2 = student_detail2.photo
                        finalPhoto2 = photo_url

                    except:
                        finalPhoto2 = None
                    student_cache2 =\
                        SubjectAccuracyStudent.objects.get(student=second_student,subject=sub)
                    totalQuestionAttempted2 = student_cache2.totalAttempted
                    totalQuestionsRight2 = student_cache2.rightAnswers
                    student_wise_rank_dict['student2'] =\
                            {'rankank2':int(rank_index+1),'accuracy2':sortedMarks[rank_index],'questionAttempted2':totalQuestionAttempted2,'right2':totalQuestionsRight2,'subject2':sub}
                if student_wise_rank_dict != {}:
                    try:
                        if student_wise_rank_dict['student1'] == {}:
                            pass
                    except:
                            student_wise_rank_dict['student1'] =None
                    try:
                        if student_wise_rank_dict['student2'] == {}:
                            pass
                    except:
                            student_wise_rank_dict['student2'] =None

                    final_rank.append(student_wise_rank_dict)

        final_rank = list(unique_everseen(final_rank))
        context = {'subject_ranking':final_rank}
        return Response(context)


class changeCourse(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        new_course = data['course']
        student_details = StudentDetails.objects.get(student =
                                                     self.request.user)
        student_details.course = new_course
        student_details.save()
        teacher = Teacher.objects.get(name='BodhiAI')
        try:
            course_model = StudentCourse.objects.get(student=me.profile)
            course_model.course = course
            course_model.save()
        except:
            context = {'subjects':'error'}
            return context
       # delete existing subjects
        student_subjects = Subject.objects.filter(student = me.profile)
        for sub in student_subjects:
            sub.delete()
        student_klass = me.profile.klass
        my_school = me.profile.school
        new_klass = klass.objects.get(name=course,school= my_school)
        me.profile.klass = new_klass
        stud = Student.objects.get(id = me.profile.id)
        stud.klass = new_klass
        stud.save()

        bodhi_teacher = Teacher.objects.get(school = my_school)
        membership.api.views.add_subjects(course,me.profile,bodhi_teacher)
        addOldTests.delay(me.profile.id,bodhi_teacher.id,new_klass.id)
        try:
            student_details = StudentDetails.objects.get(student = user)
            student_details.course = course
            student_details.language = language
            student_details.save()
        except:
            student_details = StudentDetails()
            student_details.student = user
            student_details.language = language
            student_details.course = course
            student_details.save()
        context = {'subjects':'{} course registered'.format(course)}
        return Response(context)


class userBeforeDownloadingData(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        ip_data = data['user_data']
        user_data = json.dumps(data)
        json_user_data = json.loads(user_data)
        final_data = json_user_data['user_data']
        ip_address = final_data['ip']
        city = final_data['city']
        region = final_data['region']
        country = final_data['country']
        location = final_data['loc']
        postal = final_data['postal']
        org = final_data['org']
        new_user_data = PotentialUserData()
        new_user_data.ipAddress = ip_address
        new_user_data.city = city
        new_user_data.region = region
        new_user_data.country = country
        new_user_data.loc = location
        new_user_data.postal = postal
        new_user_data.org = org
        new_user_data.save()

        print('ip address {}'.format(ip_address))
        context = {'data':str(user_data)}
        return Response(context)


#class teacheruploadimage(APIView):
#    def post(self,request,*args,**kwargs):
#        me = Teach(self.request.user)
#        data = request.data
#        title = data['title']
#        description = data['description']
#        content = data['content']
#        upload_obj = TeacherUploadedImage()
#        upload_obj.teacher = me.profile
#        upload_obj.title = title
#        upload_obj.content = content
#        upload_obj.description = description
#        upload_obj.time = timezone.now()
#        upload_obj.save()
#        context = {'title':title,'description':description,'img':content}
#        return Response(context)

