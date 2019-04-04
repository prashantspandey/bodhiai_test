from rest_framework import generics
from django.contrib.auth.models import Group
from celery.result import AsyncResult 
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from basicinformation.models import *
from django.http import Http404, HttpResponse 
from .serializers import * 
from basicinformation.marksprediction import *
from QuestionsAndPapers.models import *
from basicinformation.tasks import *
import json 
from more_itertools import unique_everseen
from rest_framework.response import Response
from rest_framework.permissions import (
   IsAuthenticated
)
from basicinformation.tasks import *
from django.utils import timezone
from django.utils.timezone import localdate
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import login as django_login, logout as django_logout
import requests
import random 


class CustomRegistration(APIView):
   def post(self,request,*args,**kwargs):
        username = request.POST['username']
        password = request.POST['password']
        name = request.POST['name'] 
        institute = request.POST['institute']
        context =\
           {'username':username,'password':password,'first_name':name}
        serializer = CustomRegistrationSerializer(data = context)
        if serializer.is_valid():
            user = serializer.save()
            print('user registered , institute {}'.format(institute))
            if user:
                if 'jen' in institute.lower():
                   institute = 'JEN'
                if 'ysm' in institute.lower():
                   institute = 'YSM'
                if 'cq' in institute.lower():
                    institute = "Competition_Qualifiers"
                if 'bodhiai' in institute.lower():
                   institute = "BodhiAI"
                if 'bc' in institute.lower():
                    institute = ""
                school = School.objects.get(name=institute)
                print('{} school'.format(school.name))
                batch = klass.objects.get(school=school,name='Outer')
                stud = Student(studentuser = user,klass = batch,school =school)
                stud.studentuser.first_name = name
                stud.name = name
                stud.save()
                my_group = Group.objects.get(name='Students')
                my_group.user_set.add(user)

            
                teacher = Teacher.objects.get(school=school)
                if institute == 'YSM' or institute == 'BodhiAi':
                   add_subjects('SSC',stud,teacher)
                elif 'jen' in institute.lower():
                   add_subjects('Loco',stud,teacher)
                elif 'cq' in institute.lower():
                   subEnglish = Subject(name="English",student=stud,teacher=teacher)
                   subEnglish.save()
                elif 'bc' in institute.lower():
                    add_subjects('SSC',stud,teacher)

                confirmation = StudentConfirmation()
                confirmation.student = user
                confirmation.school = school
                confirmation.name = stud.name
                confirmation.teacher = teacher
                confirmation.batch = batch
                confirmation.save()
                addOldTests.delay(stud.id,teacher.id,batch.id)
                add_announcements_newStudent.delay(stud.id,batch.id)

                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] =\
                {'token':token.key,'class':stud.klass.name,'school':stud.school.name}
                return Response(json,status = status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class TeacherStudentConfirmationDisplayAPIView(APIView):

    def get(self,request,format=None):
        me = Teach(self.request.user)
        confirmations = StudentConfirmation.objects.filter(teacher =
                                                           me.profile,confirm=None)
        if len(confirmations) == 0:
            context = {'response':'No new students waiting for Batch allocation.'}
            return Response(context)
        else:
            serializer = StudentConfirmationSerializer(confirmations,many=True)

            batches = me.my_classes_objects()
            batch_serializer =BatchSerializer(batches,many=True)

            context =\
            {'confirmations':serializer.data,'batches':batch_serializer.data}
            return Response(context)


class TeacherStudentConfirmedAPIView(APIView):
    def post(self,request,*args,**kwargs):
        batch_id = request.POST['batch_id']
        confirmation_id = request.POST['confirmation_id']
        batch = klass.objects.get(id = batch_id)
        me = Teach(self.request.user)
        confirmation = StudentConfirmation.objects.get(id = confirmation_id)
        school = confirmation.school
        student_user = confirmation.student
        student = Student.objects.get(studentuser = student_user)
        student.klass = batch
        student.save()
        subs = Subject.objects.filter(student = student)
        for i in subs:
            i.delete()
        custom_batches = CustomBatch.objects.filter(school = school)
        for cb in custom_batches:
            custom_bat = cb.klass
            if batch == custom_bat:
                subjects = cb.subjects
                for sub in subjects:
                    addSub = Subject(name =
                                     sub.strip(),student=student,teacher=me.profile)
                    addSub.save()
        if batch.name == 'LocoPilot':
            subGenInte = Subject(name="General-Intelligence",student=student,teacher=me.profile)
            subGenInte.save()
            subMaths = Subject(name="Quantitative-Analysis",student=student,teacher=me.profile)
            subEnglish = Subject(name="English",student=student,teacher=me.profile)
            subGenKnow = Subject(name="General-Knowledge",student=student,teacher=me.profile)
            subGenSci = Subject(name="General-Science",student=student,teacher=me.profile)
            subLocoPilot_Fitter =\
            Subject(name="FitterLocoPilot",student=student,teacher=me.profile)
            subLocoPilot_Fitter.save()
            subLocoPilot_diesel =\
            Subject(name="LocoPilot_Diesel",student=student,teacher=me.profile)
            subLocoPilot_diesel.save()
            subCivil =\
            Subject(name='Civil_Loco_Pilot_Tech',student=student,teacher=me.profile)


            subCivil.save() 
            subMaths.save()
            subEnglish.save()
            subGenSci.save()
            subGenKnow.save()

            subLocoPilot = Subject(name="ElectricalLocoPilot",student=student,teacher=me.profile)
            subLocoPilot.save()

        elif batch.name == 'SSC':
            subGenInte = Subject(name="General-Intelligence",student=student,teacher=me.profile)
            subGenInte.save()
            subMaths = Subject(name="Quantitative-Analysis",student=student,teacher=me.profile)
            subEnglish = Subject(name="English",student=student,teacher=me.profile)
            subGenKnow = Subject(name="General-Knowledge",student=student,teacher=me.profile)
            subGenSci = Subject(name="General-Science",student=student,teacher=me.profile)
            subCivil =\
            Subject(name='Civil_Loco_Pilot_Tech',student=student,teacher=me.profile)
            subCivil.save()
            subMaths.save()
            subGenSci.save()
            subEnglish.save()
            subGenKnow.save()
            subLocoPilot =\
            Subject(name="ElectricalLocoPilot",student=student,teacher=me.profile)
            subLocoPilot.save()
            subLocoPilot_Fitter =\
            Subject(name="FitterLocoPilot",student=student,teacher=me.profile)
            subLocoPilot_Fitter.save()
            subLocoPilot_diesel =\
            Subject(name="LocoPilot_Diesel",student=student,teacher=me.profile)
            subLocoPilot_diesel.save()





        elif batch.name == 'RailwayGroupD':
            subGenInte = Subject(name="General-Intelligence",student=student,teacher=me.profile)
            subGenInte.save()
            subMaths = Subject(name="Quantitative-Analysis",student=student,teacher=me.profile)
            subGenKnow = Subject(name="General-Knowledge",student=student,teacher=me.profile)
            subGenSci = Subject(name="General-Science",student=student,teacher=me.profile)
            subMaths.save()
            subGenSci.save()
            subLocoPilot =\
            Subject(name="ElectricalLocoPilot",student=student,teacher=me.profile)
            subLocoPilot.save()
            subLocoPilot_Fitter =\
            Subject(name="FitterLocoPilot",student=student,teacher=me.profile)
            subLocoPilot_Fitter.save()
            subLocoPilot_diesel =\
            Subject(name="LocoPilot_Diesel",student=student,teacher=me.profile)
            subLocoPilot_diesel.save()
            subCivil =\
            Subject(name='Civil_Loco_Pilot_Tech',student=student,teacher=me.profile)



            subCivil.save()
            subGenKnow.save()
        confirmation.confirm = True
        confirmation.batch = batch
        confirmation.save()
        addOldTests.delay(student.id,me.profile.id,batch.id)
        add_announcements_newStudent.delay(student.id,batch.id)
        context = {'success': '{} Successfully added to  {} batch.'.format(student.name,batch.name)}
        return Response(context)


class CustomLoginAPIView(APIView):
    def post(self,request):
        serializer = CustomLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data["user"]
        django_login(request,user)
        token, created = Token.objects.get_or_create(user=user)
        groups = user.groups.all()
        try:
            student = Student.objects.get(studentuser = user)
        except:
            token_context  = \
                    {'key':token.key,'user_type':groups[0].name,'name':user.username}
            return Response(token_context,status = 200)


        check_subjects = Subject.objects.filter(student = student)
        if len(check_subjects) != 0:
            hasCourse = True
        else:
            hasCourse = False


        #delete_bad_Online_Marks.delay(user.id)
        try:
            student_details = StudentDetails.objects.get(student = user)
            #student = Student.objects.get(studentuser = user)
            klass_name = student.klass.name

            token_context  = \
                    {'key':token.key,'user_type':groups[0].name,'name':user.username,'photo':student_details.photo,'batch':klass_name,'hasCourse':hasCourse,'display_name':student.name,'language':student_details.language}

        except:
            token_context  = \
                    {'key':token.key,'user_type':groups[0].name,'name':user.username,'photo':None,'hasCourse':hasCourse,'display_name':student.name,'language':student_details.language}

        return Response(token_context,status = 200)

class CustomLogoutAPIView(APIView):
    authentication_classes = (TokenAuthentication,)

    def post(self,request):
        django_logout(request)
        return Response(status=204)


def add_subjects(course,stud,teacher):
    if course == 'RRB':
        subGenInte =\
        Subject(name="General-Intelligence",student=stud,teacher=teacher)
        subGenInte.save()
        subMaths =\
        Subject(name="Quantitative-Analysis",student=stud,teacher=teacher)
        #subEnglish = Subject(name="English",student=stud,teacher=teacher)
        subGenKnow =\
        Subject(name="General-Knowledge",student=stud,teacher=teacher)
        subGenSci = Subject(name="General-Science",student=stud,teacher=teacher)
        #subCivil =\
        #Subject(name='Civil_Loco_Pilot_Tech',student=stud,teacher=teacher)
        subMaths.save()
        subGenSci.save()
        #subEnglish.save()
        subGenKnow.save()
        #subCivil.save()
 
    elif course == 'SSC':
        subGenInte =\
        Subject(name="General-Intelligence",student=stud,teacher=teacher)
        subGenInte.save()
        subMaths =\
        Subject(name="Quantitative-Analysis",student=stud,teacher=teacher)
        subEnglish = Subject(name="English",student=stud,teacher=teacher)
        subGenKnow =\
        Subject(name="General-Knowledge",student=stud,teacher=teacher)
        #subGenSci = Subject(name="General-Science",student=stud,teacher=teacher)
        #subCivil =\
        #Subject(name='Civil_Loco_Pilot_Tech',student=stud,teacher=teacher)
        subMaths.save()
        #subGenSci.save()
        subEnglish.save()
        subGenKnow.save()
        #subCivil.save()
    elif course == 'Loco':
       subGenInte =\
       Subject(name="General-Intelligence",student=stud,teacher=teacher)
       subGenInte.save()
       subMaths =\
       Subject(name="Quantitative-Analysis",student=stud,teacher=teacher)
       subEnglish =\
       Subject(name="English",student=stud,teacher=teacher)
       subGenKnow =\
       Subject(name="General-Knowledge",student=stud,teacher=teacher)
       subGenSci =\
       Subject(name="General-Science",student=stud,teacher=teacher)
       subLocoPilot =\
       Subject(name="ElectricalLocoPilot",student=stud,teacher=teacher)
       subLocoPilot.save()
       subLocoPilot_diesel =\
       Subject(name="LocoPilot_Diesel",student=stud,teacher=teacher)
       subLocoPilot_diesel.save()
       subCivil =\
       Subject(name='Civil_Loco_Pilot_Tech',student=stud,teacher=teacher)
    elif course == 'NEET':
       subPhysics =\
       Subject(name="Physics_NEET",student=stud,teacher=teacher)
       subChemistry =\
       Subject(name="Chemistry_NEET",student=stud,teacher=teacher)
       subBotony =\
       Subject(name="Biology_NEET",student=stud,teacher=teacher)




       subChemistry.save()
       subPhysics.save()
       subBotony.save()


    elif course == 'IITJEE':
       subPhysics =\
       Subject(name="Physics_IIT",student=stud,teacher=teacher)
       subMaths =\
       Subject(name="Maths_IIT",student=stud,teacher=teacher)
       subChemistry =\
       Subject(name="Chemistry_IIT",student=stud,teacher=teacher)

       subChemistry.save()
       subPhysics.save()
       subMaths.save()


class FireBaseToken(APIView):
    def post(self,request,*args,**kwargs):
        token = request.POST['token']
        user = self.request.user
        try:
            firebase_token = FirebaseToken.objects.get(user = user)
            firebase_token.token = token
            firebase_token.save()
        except Exception as e:
            print(str(e))
            firebase_token = FirebaseToken()
            firebase_token.user = user
            firebase_token.token = token
            firebase_token.save()
        context = {'token': 'token saved'}
        return Response(context)

class ResetPassword(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        username = data['username']
        phone = data['phone']
        password = data['password']
        try:
            user = User.objects.get(username=username)
            message = 'This is your new password '+str(password)
            send_url = 'http://sms.trickylab.com/http-api.php?username=bodhiai&password=123456&senderid=Bodhii&route=1&number='+phone+'&message='+message+''
            r = requests.get(send_url)
            print('status code {}'.format(r.status_code))
            print(r.text)
            user.set_password(str(password))
            user.save()
            return Response({'type':'success'})

        except:
            return Response({'type':'failed'})


class GoogleCustomLoginAndroid(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        user_id = data['user_id']
        email = data['email']
        display_name = data['display_name']
        photo = data['photo']
        try:
            user = User.objects.create_user(username=email, email=email,\
                                                password='newpassword')
            institute = "BodhiAI"
            school = School.objects.get(name=institute)
            batch = klass.objects.get(school=school,name='Outer')
            stud = Student(studentuser = user,klass = batch,school =school)
            stud.studentuser.first_name = display_name
            stud.name = display_name
            stud.save()
            student_details = StudentDetails()
            student_details.student = user
            student_details.photo = photo
            student_details.email = email
            student_details.username = email
            student_details.fullName = display_name
            student_details.save()
            my_group = Group.objects.get(name='Students')
            my_group.user_set.add(user)


            teacher = Teacher.objects.get(school=school)
            confirmation = StudentConfirmation()
            confirmation.student = user
            confirmation.school = school
            confirmation.name = stud.name
            confirmation.teacher = teacher
            confirmation.batch = batch
            confirmation.save()
            #addOldTests.delay(stud.id,teacher.id,batch.id)
            add_announcements_newStudent.delay(stud.id,batch.id)

            hasCourse = False
            token = Token.objects.create(user=user)
            json = serializer.data
            json['token'] =\
                    {'token':token.key,'class':stud.klass.name,'school':stud.school.name,'photo':photo,'name':email,'hasCourse':hasCourse,'display_name':display_name}
            return Response(json,status = status.HTTP_201_CREATED)

            print('new user created')
        except Exception as e:
            print(str(e))
            user = User.objects.get(username=email)
            django_login(request,user)
            token, created = Token.objects.get_or_create(user=user)
            groups = user.groups.all()
            student = Student.objects.get(studentuser = user)
            klass_name = student.klass.name
            check_subjects = Subject.objects.filter(student = student)
            if len(check_subjects) != 0:
                hasCourse = True
            else:
                hasCourse = False

            try:
                student_details = StudentDetails.objects.get(student = user)

                token_context  = \
                        {'key':token.key,'user_type':groups[0].name,'name':user.username,'photo':student_details.photo,'batch':klass_name,'hasCourse':hasCourse,'display_name':display_name}

            except:
                token_context  = \
                        {'key':token.key,'user_type':groups[0].name,'name':user.username,'photo':None,'batch':klass_name,'hasCourse':hasCourse,'display_name':display_name}
            return Response(token_context,status = 200)


class B2CNormalRegistration(APIView):
   def post(self,request,*args,**kwargs):
       data = request.data
       username = data['username']
       password = data['password']
       name = data['name'] 
       institute = data['institute']
       context =\
               {'username':username,'password':password,'first_name':name}
       serializer = CustomRegistrationSerializer(data = context)
       if serializer.is_valid():
           user = serializer.save()
           if user:
               print('{} institute'.format(institute))
               if 'bodhiai' in institute.lower():
                   institute = "BodhiAI"

               school = School.objects.get(name=institute)
               batch = klass.objects.get(school=school,name='Outer')
               stud = Student(studentuser = user,klass = batch,school =school)
               stud.studentuser.first_name = name
               stud.name = name
               stud.save()
               my_group = Group.objects.get(name='Students')
               my_group.user_set.add(user)
               student_details = StudentDetails()
               student_details.student = user
               #student_details.photo = photo
               #student_details.email = email
               student_details.username = username
               student_details.fullName = name
               student_details.save()
 
                # add subjects will happen when student chooses a course 
               #teacher = Teacher.objects.get(school=school)
               #if  institute == 'BodhiAi':
               #    add_subjects('SSC',stud,teacher)
               #elif 'jen' in institute.lower():
               #    add_subjects('Loco',stud,teacher)

               teacher = Teacher.objects.get(school=school)
               confirmation = StudentConfirmation()
               confirmation.student = user
               confirmation.school = school
               confirmation.name = stud.name
               confirmation.teacher = teacher
               confirmation.batch = batch
               confirmation.save()
               #addOldTests.delay(stud.id,teacher.id,batch.id)
               add_announcements_newStudent.delay(stud.id,batch.id)
               hasCourse = False
 
               token = Token.objects.create(user=user)
               json = serializer.data
               json['token'] =\
               {'token':token.key,'class':stud.klass.name,'school':stud.school.name,'hasCourse':hasCourse}
               return Response(json,status = status.HTTP_201_CREATED)
       return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class B2CRegisterCourse(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        user = self.request.user
        me = Studs(user)
        teacher = Teacher.objects.get(name='BodhiAI')
        course = data['course']
        try:
            course_model = StudentCourse.objects.get(student=me.profile)
        except:
            course_model = StudentCourse()
            course_model.student = me.profile
            course_model.course = course
            course_model.save()
        # delete existing subjects
        student_subjects = Subject.objects.filter(student = me.profile)
        for sub in student_subjects:
            sub.delete()
        student_klass = me.profile.klass
        my_school = me.profile.school
        new_klass = klass.objects.get(name=course,school= my_school)
        me.profile.klass = new_klass
        bodhi_teacher = Teacher.objects.get(school = my_school)
        add_subjects(course,me.profile,bodhi_teacher)
        addOldTests.delay(me.profile.id,bodhi_teacher.id,new_klass.id)
        student_details = StudentDetails.objects.get(student = user)
        student_details.course = course
        student_details.save()
        context = {'subjects':'{} course registered'.format(course)}
        return Response(context)

class B2CRegisterCourseAndLanguage(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        user = self.request.user
        me = Studs(user)
        teacher = Teacher.objects.get(name='BodhiAI')
        course = data['course']
        language = data['language']
        try:
            course_model = StudentCourse.objects.get(student=me.profile)
        except:
            course_model = StudentCourse()
            course_model.student = me.profile
            course_model.course = course
            course_model.save()
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
        add_subjects(course,me.profile,bodhi_teacher)
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


class CheckSubjects(APIView):
    def get(self,request):
        user = self.request.user
        me = Studs(user)
        student_id = me.profile.id
        
        subjects = Subject.objects.filter(student = me.profile)
        if len(subjects) != 0:
            context = {"subjects":'has course'}
            return Response(context)
        else:
            context = {"subjects":'no course'}
            return Response(context)

class SendOTPRegistration(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        phone = data['phone']
        try:
            user = User.objects.get(username = phone)
            context = {'number':phone,'otp':str(True)}
            return Response(context)
        except:
            pass
        otp = self.generate_four_digit_otp(4)
        send_otp.delay(phone,otp)
        context = {'number':phone,'otp':otp}
        return Response(context)

    def generate_four_digit_otp(self,digits):
        lower = 10**(digits-1)
        upper = 10**digits - 1
        return random.randint(lower, upper)


class IITJEE24jan(APIView):
   def post(self,request,*args,**kwargs):
       data = request.data
       username = data['email']
       password = data['phone']
       name = data['name'] 
       shift = data['shift']
       context =\
               {'username':email,'password':phone,'first_name':name}
       serializer = CustomRegistrationSerializer(data = context)
       if serializer.is_valid():
           user = serializer.save()
           if user:
               institute = "BodhiAI"
               school = School.objects.get(name=institute)
               print('{} institute'.format(institute))
               if shift == 'morning':
                   batch = klass.objects.get(school=school,name='24janmorning')
               elif shift == 'evening':
                   batch = klass.objects.get(school=school,name='24janevening')
               stud = Student(studentuser = user,klass = batch,school =school)
               stud.studentuser.first_name = name
               stud.name = name
               stud.save()
               my_group = Group.objects.get(name='Students')
               my_group.user_set.add(user)
               student_details = StudentDetails()
               student_details.student = user
               #student_details.photo = photo
               student_details.email = email
               student_details.username = username
               student_details.fullName = name
               student_details.save()
 
                # add subjects will happen when student chooses a course 
               #teacher = Teacher.objects.get(school=school)
               #if  institute == 'BodhiAi':
               #    add_subjects('SSC',stud,teacher)
               #elif 'jen' in institute.lower():
               #    add_subjects('Loco',stud,teacher)

               teacher = Teacher.objects.get(school=school)
               confirmation = StudentConfirmation()
               confirmation.student = user
               confirmation.school = school
               confirmation.name = stud.name
               confirmation.teacher = teacher
               confirmation.batch = batch
               confirmation.save()


               course = 'IITJEE'
               language = 'English'
               course_model = StudentCourse()
               course_model.student = stud
               course_model.course = course
               course_model.save()

               add_subjects(course,stud,teacher)
               #addOldTests.delay(me.profile.id,bodhi_teacher.id,new_klass.id)
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
 
               return Response({'response':'success'})


