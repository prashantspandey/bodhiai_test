from rest_framework import generics
from boto3.dynamodb.conditions import Key,Attr
from django.utils import timezone
from celery.result import AsyncResult 
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from basicinformation.models import *
import requests
from django.http import Http404, HttpResponse 
from .serializers import *
from QuestionsAndPapers.api.views import *
from chatbox.models import *
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
from decimal import Decimal



class ChatBoxAPIView(APIView):
    def post(self,request,*args,**kwargs):
        me = Studs(self.request.user)
        data = request.data
        user_reply = data['user_reply']
        if user_reply == 'custom_test_performance':
            nextContextObj =\
                PossibleContext.objects.get(context='analysis_specific_test')


            chatHistory = ChatHistory.objects.get(student= me.profile)
            response_context =\
                        self.fireNextContext(me,nextContextObj,user_reply,chatHistory,repeat=False,nextPosition='zero')
            return Response(response_context)

        try:
            chatHistory = ChatHistory.objects.get(student= me.profile)
            lastMessage = chatHistory.messages[-1]
            lastContext = chatHistory.contexts[-1]
            lastDate = chatHistory.dates[-1]
            nextPosition = chatHistory.nextPosition[-1]
            repeat = chatHistory.repeat[-1]



            if lastContext == 'error context':
                context =\
                    {'context':None,'message':'I will be back soon.','data':None}
                return Response(context)
            elif lastContext == 'end_message':
                context = \
                {'context':None,'message':'I will be back soon.','data':None}

                return Response(context)


            context_obj = PossibleContext.objects.get(context=lastContext)
            next_context = context_obj.next_context


            if next_context != None:
                if repeat == True:
                    print('I am in repeat of chat')
                    nextContextObj = context_obj
                    response_context =\
                            self.fireNextContext(me,nextContextObj,user_reply,chatHistory,repeat=True,nextPosition
                                                =nextPosition)
                    return Response(response_context)


                nextContextObj =\
                PossibleContext.objects.get(context=next_context)

                if next_context == 'None':
                    if requisite == 'ranking':
                        isRank = self.requisiteRanking(me.profile.id)
                        if isRank == True:
                            response_context =\
                            self.fireNextContext(me,nextContextObj,user_reply,chatHistory,repeat=repeat,nextPosition=nextPosition)
                        else:
                            nextContextObj =\
                                PossibleContext.objects.get(context='tests_first_test')
                    elif requisite == 'courselength':
                        iscourseLength =\
                        self.requisiteCourseLength(me.profile.id)
                        if iscourseLength == True:
                            response_context =\
                            self.fireNextContext(me,nextContextObj,user_reply,chatHistory,repeat=repeat,nextPosition=nextPosition)
                        else:
                            nextContextObj =\
                                PossibleContext.objects.get(context='welcome_choose_course_time')





                response_context =\
                self.fireNextContext(me,nextContextObj,user_reply,chatHistory,repeat=repeat,nextPosition=nextPosition)
                return Response(response_context)
            else:
                allPossibleContext = PossibleContext.objects.all()
                context_list = []
                for i in allPossibleContext:
                    if i.context not in chatHistory.context:
                        context_list.append(i.context)

                next_context = random.choice(context_list)
                nextContextObj =\
                PossibleContext.objects.get(context=next_context)
                print('family {}, nextContext\
                      {}'.format(nextContextObj.family,nextContextObj.context)
                      )
                response_context =\
                self.nextMessage(me.profile.id,nextContextObj.family,nextContextObj.context,user_reply)
                # saving to chat history
                allMessages = chatHistory.messages
                allContexts = chatHistory.contexts
                allDates = chatHistory.dates
                allTypes = chatHistory.types
                allMessages.append(response_context['message'])
                nextPosition.append(response_context['nextPosition'])
                repeat.append(response_context['repeat'])
                allContexts.append(response_context['context'])
                allDates.append(timezone.now())
                allTypes.append('sent')
                chatHistory.save()
 
                return Response(response_context)
 


           
            
        except ChatHistory.DoesNotExist:
            
            student_detail = StudentDetails.objects.get(student =
                                                       me.profile.studentuser)
            language = student_detail.language

            chatHistory = ChatHistory()
            first_context = PossibleContext.objects.get(context =
                                                        'welcome_first')
            detail_context = ContextDetail.objects.filter(context__context=
                                                          'welcome_first')

            dc_list = []
            for dc in detail_context:
                dc_list.append(dc)
            to_send_dc = random.choice(dc_list)
            if language == 'English':
                newMessage = to_send_dc.message.replace('{}',me.profile.name)
            else:
                newMessage = to_send_dc.messageHindi.replace('{}',me.profile.name)
            keywords = ['Next']
            context =\
                    {'context':first_context.context,'message':newMessage,'data':None,'next':False,'keywords':keywords}
            chatHistory.context = [first_context.context]
            chatHistory.dates = [timezone.now()]
            chatHistory.student = me.profile
            chatHistory.types =['sent']
            chatHistory.messages = [to_send_dc.message]
            chatHistory.contexts= [first_context.context]
            chatHistory.nextPosition = ['None']
            chatHistory.repeat = [False]
            chatHistory.save()
            return Response(context)


    def create_study_plan(self,me,course,course_length):
        study_plan = StudyPlan()
        study_plan.student = me.profile
        study_plan.course = course
        study_plan.course_length = course_length
        study_plan.start = timezone.now()
        subjects = me.my_subjects_names()
        study_plan.subjects = subjects
        study_plan.save()
        for sub in subjects:
            chapters = SubjectChapters.objects.filter(subject=sub)
            for chap in chapters:
                study_plan.chapters.add(chap)
                chapter_plan = ChapterPlan()
                chapter_plan.studyPlan = study_plan
                chapter_plan.chapter = chap
                chapter_plan.overall_sovle = int(50)
                chapter_plan.solved = int(0)
                chapter_plan.to_solve = int(50-0)
                chapter_plan.save()
        study_plan.save()
        return study_plan
        
        


    def translate_hindi(self,text):
        key = 'AIzaSyDOW6Nt-1jpzxcEbypSpJ-ObCsZHjYBjPA'
        url ='https://translation.googleapis.com/language/translate/v2?target=hi&key='+key+'&q='+text+''
        r = requests.get(url)
        if r.status_code == 200:
            trans = r.text
            trans = json.loads(trans)
            trans_dict = trans['data']['translations']
            final_text = trans_dict[0]['translatedText']
            return final_text
        else:
            return r.status_code


    def\
    fireNextContext(self,me,nextContextObj,user_reply,chatHistory,repeat=False,nextPosition=None):
        response_context =\
        self.nextMessage(me.profile.id,nextContextObj.family,nextContextObj.context,user_reply,repeat,nextPosition)
        # saving to chat history
        allMessages = chatHistory.messages
        allContexts = chatHistory.contexts
        allDates = chatHistory.dates
        allTypes = chatHistory.types
        allNextPosition = chatHistory.nextPosition
        allRepeat = chatHistory.repeat
        try:
            saveMessage = response_context['message']
        except:
            saveMessage = 'error message'
        try:
            saveContext = response_context['context']
        except:
            saveContext = 'error context'
        try:
            nextPosition = response_context['nextPosition']
        except:
            nextPosition = 'None'
        try:
            repeat = response_context['repeat']
        except:
            repeat = False
        try:
            allMessages.append(saveMessage)
            allContexts.append(saveContext)
            allDates.append(timezone.now())
            allTypes.append('sent')
            allNextPosition.append(nextPosition)
            allRepeat.append(repeat)
        except:
            allMessages.append('None')
            allContexts.append('None')
            allDates.append(timezone.now())
            allTypes.append('sent')
            allNextPosition.append('None')
            allRepeat.append(False)

        chatHistory.save()
        
        return response_context
 
    def requisiteRanking(self,student):
        student_obj = Student.objects.get(id = student)
        my_subjects = Subject.objects.filter(student = student_obj)
        rank = False
        for sub in my_subjects:
            try:
                subjectRanks = SubjectRank.objects.get(subject=sub)
                sub_ranks = subjectRanks.students
                if student in sub_ranks:
                    rank = True
                    return rank
            except:
                pass
        return False
    def requisiteCourseLength(self,student):
        student_obj = Student.objects.get(id = student)
        try:
            courseLength = CourseLength.objects.get(student = student_obj)
            return True
        except:
            return False

    def requisiteFirstTest(self,student):
        student_obj = Student.objects.get(id = student)
        tests = SSCOnlineMarks.objects.filter(student = student_obj)
        if len(tests) != 0:
            return True
        else:
            return False

    def analysis_specific_test_first(self,percent_attempted):
        if percent_attempted < 30:
            attempt_comment = """You did not attempt many questions.Next time try attempting much more. I will guide you how to do so."""
            attempt_comment_hindi = """आपने काफी कम  सवाल एटेम्पट किये . अगली बार ज्यादा सवाल एटेम्पट करने की कोशिश करें . चिंता मत करें मैं अप्पको गाइड कर्रूँगा कैसे करना है """
        elif 30 <= percent_attempted < 60:
            attempt_comment = """You attempted a few questions. But attempt percent can go higher."""
            attempt_comment_hindi = """आपने कुछ सवाल एटेम्पट किये . पर आपको और ज्यादा सवाल एटेम्पट करने चाहिए थे . मैं आपको गाइड कर्रूँगा कैसे करना है """
        else:
            attempt_comment = """You attempt rate was fine. Let's look at other things."""
            attempt_comment_hindi = """आपका  एटेम्पट परसेंट अच्छा था. ऐसे ही करते रहे """

        return attempt_comment,attempt_comment_hindi
    def analysis_specific_test_second(self,percent_score):
        if percent_score <30:
            score_comment = """You performed poorly.This way you can't reach your goal. Don't worry I will teach you how to score higher."""
            score_comment_hindi = """आपका स्कोर अच्छा नहीं है . इसको बढ़ाने के जरूरत है . मैं आपको गाइड कर्रूँगा कैसे """
        elif 30 <percent_score <60:
            score_comment = """You did not perform up to expectations.Don't worry I will teach you how to score higher."""
            score_comment_hindi = """आपने उम्मीद के अनुसार परफॉर्म नहीं किया. इसको और अच्छा करने की जरूरत है """
        elif 60 <percent_score <90:
            score_comment = """Good Score.You are doing going.But we will take this to even greater score.."""
            score_comment_hindi = """अच्छा स्कोर।    लेकिन हम इसे और भी अधिक स्कोर तक ले जाएंगे।"""
 
        else:
            score_comment = """You scored decent marks. Lets get this score even higher"""
            score_comment_hindi = """आपका स्कोर अच्छा था . मैं आपको इसे और अच्छा करने मैं गाइड कर्रूँगा  """
        return score_comment,score_comment_hindi
    def analysis_specific_test_third(self,time):
        if time < 120:
            time_comment = """It seems like you did not take this test seriously . Please be serious and try to solve questions so that your score can improve."""
            time_comment_hindi = """ऐसा लगता है जैसे आपने इस परीक्षा को गंभीरता से नहीं लिया। कृपया गंभीर रहें और प्रश्नों को हल करने का प्रयास करें ताकि आपका स्कोर बेहतर हो सके।"""
        else:
            time_comment = """We will work on improving your timing. Are you sure you are giving appropriate time to every question."""
            time_comment_hindi = """हम आपकी टाइमिंग सुधारने पर काम करेंगे। क्या आप सुनिश्चित हैं कि आप हर प्रश्न को उचित समय दे रहे हैं?"""

        return time_comment,time_comment_hindi

    def get_specific_testRank(self,test_id,student_id):
        my_rank = 0
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
            #student_marks = SSCOnlineMarks.objects.get(student=st,test
            #                                           =klass_test)
            #rightAnswers = len(student_marks.rightAnswers)
            #allAnswers = len(student_marks.allAnswers)
            #accuracy = rightAnswers/ allAnswers



            student_wise_rank_dict =\
                    {'name':st.name,'photo':finalPhoto,'username':st.studentuser.username,'rank':int(rank_index+1)}
            final_rank_list.append(student_wise_rank_dict)
            if stud == student_id:
                my_rank = int(rank_index+1)
        if my_rank > 5:
            final_ranking = final_rank_list[my_rank-4:my_rank-1]
        else:
            final_ranking = final_rank_list[0:5]

        return final_ranking,my_rank,len(sortedStudents)


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

    def divert_context(self,me,to_context,repeat=None,nextPosition=None):
        nextContextObj =\
            PossibleContext.objects.get(context=to_context)
        user_reply = None

        chatHistory = ChatHistory.objects.get(student= me.profile)
        if repeat == True and nextPosition:
            response_context =\
            self.fireNextContext(me,nextContextObj,user_reply,chatHistory,repeat=True,nextPosition=nextPosition)
        else:
            response_context =\
            self.fireNextContext(me,nextContextObj,user_reply,chatHistory)
        return response_context
 

    def nextMessage(self,student,family,specific_context,user_data =\
                    None,repeat=False,nextPosition=None):
        student = Student.objects.get(id = student)
        me = Studs(student.studentuser)
        student_detail = StudentDetails.objects.get(student =
                                                   student.studentuser)
        language = student_detail.language
        if family == 'free':
            if specific_context == 'free_change_chapter':
                print('in chanage chapter')
                if repeat == False:

                    study_plan = StudyPlan.objects.get(student=me.profile)
                    subjects = study_plan.subjects
                    sub_dict_list = []
                    for s in subjects:
                        subject_logo = SubjectLogo.objects.get(name=s)
                        sub_dict =\
                        {'button_text':s,'image':subject_logo.logo2,'hidden_variable':s}
                        sub_dict_list.append(sub_dict)
                    data ={'quick_reply':sub_dict_list}
                    fatherContext = PossibleContext.objects.get(context
                                                                    =
                                                                    specific_context)
                    context_detail = ContextDetail.objects.get(context
                                                                   =
                                                                   fatherContext,position='first')

                    final_message =\
                        context_detail.message
                    if language == 'English':
                        last_message = final_message
                    else:
                        last_message = self.translate_hindi(final_message)

                    response_context =\
                            {'context':specific_context,'message':last_message,'data':data,'repeat':True,'nextPosition':'second','next':False,'keywords':None,'view':specific_context}
                    return response_context
                if repeat:
                    if nextPosition == 'first':
                        study_plan = StudyPlan.objects.get(student=me.profile)
                        subjects = study_plan.subjects
                        sub_dict_list = []
                        for s in subjects:
                            subject_logo = SubjectLogo.objects.get(name=s)
                            sub_dict =\
                            {'button_text':s,'image':subject_logo.logo2,'hidden_variable':s}
                            sub_dict_list.append(sub_dict)
 
                        data ={'quick_reply':sub_dict_list}
                        fatherContext = PossibleContext.objects.get(context
                                                                        =
                                                                        specific_context)
                        context_detail = ContextDetail.objects.get(context
                                                                       =
                                                                       fatherContext,position='first')

                        final_message =\
                            context_detail.message
                        if language == 'English':
                            last_message = final_message
                        else:
                            last_message = self.translate_hindi(final_message)

                        #keywords = ["Next"]
                        response_context =\
                                {'context':specific_context,'message':last_message,'data':data,'repeat':True,'nextPosition':'second','next':False,'keywords':None,'view':specific_context,'view':specific_context}
                        return response_context
                    if nextPosition == 'second':
                        subject = str(user_data)
                        study_plan = StudyPlan.objects.get(student =
                                                           student)
                        study_plan.current_subject = subject
                        study_plan.save()
                        chapters = study_plan.chapters.all()
                        chapters_list = []
                        chapter_dict_list = []
                        for chap in chapters:
                            if chap.subject == subject:
                                chapters_list.append(chap.name)
                                chap_dict =\
                                        {'button_text':chap.name,'image':'https://s3.ap-south-1.amazonaws.com/subjecticon/chapter_icons/read.png','hidden_variable':chap.name}
                                chapter_dict_list.append(chap_dict)
                        
                        data ={'quick_reply':chapter_dict_list}
                        fatherContext = PossibleContext.objects.get(context
                                                                    =
                                                                    specific_context)
                        context_detail = ContextDetail.objects.get(context
                                                                   =
                                                                   fatherContext,position='third')

                        final_message =\
                            context_detail.message
                        if language == 'English':
                            last_message = final_message
                        else:
                            last_message = self.translate_hindi(final_message)

                        latest_data = LatestChatData()
                        try:
                            latest_data = LatestChatData.objects.get(student =
                                                                     me.profile)
                            latest_data.delete()
                        except:
                            pass
                        latest_data  = LatestChatData()
                        latest_data.student = me.profile
                        latest_data.data = str(user_data)
                        latest_data.save()
                        keywords = ['Next']
                        response_context =\
                            {'context':specific_context,'message':last_message,'data':data,'repeat':True,'nextPosition':'third','next':False,'keywords':keywords,'view':specific_context}
                        return response_context

                    if nextPosition == 'third':
                        if user_data != None and user_data !='none':
                            test_chapter = user_data
                            
                            latest_data =\
                            LatestChatData.objects.get(student=me.profile)
                            subject = latest_data.data
                            study_plan = StudyPlan.objects.get(student =
                                                               me.profile)
                            study_plan.current_chapter_name = test_chapter
                            study_plan.save()
                            chapters = study_plan.chapters.all()
                            chapter = 0
                            for chap in chapters:
                                if chap.name == test_chapter and chap.subject\
                                == subject:
                                    chapter = chap

                            chapter_plan = ChapterPlan.objects.get(studyPlan =
                                                                   study_plan,chapter
                                                                   =
                                                                   chapter)
                            data =\
                                    {'subject':subject,'chapter':test_chapter,'overall_solve':chapter_plan.overall_sovle,'solved':chapter_plan.solved,'to_solve':chapter_plan.to_solve}
                            fatherContext = PossibleContext.objects.get(context
                                                                        =
                                                                        specific_context)
                            context_detail = ContextDetail.objects.get(context
                                                                       =
                                                                       fatherContext,position='third')

                            final_message =\
                                context_detail.message
                            if language == 'English':
                                last_message = final_message
                            else:
                                last_message = self.translate_hindi(final_message)

                            latest_data.delete()
                            latest_data = LatestChatData()
                            latest_data.student = me.profile
                            latest_data.data = str(subject) + ',' +\
                            str(test_chapter)
                            latest_data.save()


                            keywords = ["Choose different chapter","Next"]
                            response_context =\
                                {'context':specific_context,'message':last_message,'data':data,'repeat':False,'nextPosition':'none','next':False,'keywords':keywords,'view':'welcome_choose_course_time'}
                            return response_context
                        else:
                            response_context = self.divert_context(me,'free_change_chapter')
                            return response_context
 



 




 
 
        if family == 'welcome':
            if specific_context == 'welcome_choose_aim':
                student_aims = StudentSubjectAim.objects.filter(student =
                                                                student)
                if len(student_aims) == 0:
                    father_context = PossibleContext.objects.get(context =
                                                                  specific_context)
                    context_detail = ContextDetail.objects.filter(context =
                                                               father_context)
                    dc_list = [] 
                    for i in context_detail:
                        dc_list.append(i)
                    to_be_sent = random.choice(dc_list)
                    subjects = Subject.objects.filter(student=student)
                    sub_final = []
                    for i in subjects:
                        logos = SubjectLogo.objects.get(name=i.name)
                        sub = {'name':i.name\
                               ,'logo':logos.logo2,'marks':str(40)}
                        sub_final.append(sub)
                    if language == 'English':
                        final_message_send = to_be_sent.message
                    else:
                        final_message_send = to_be_sent.messageHindi
                    keywords = ['Choose Goal']
                    response_context =\
                            {'context':specific_context,'message':final_message_send,'data':sub_final,'repeat':False,'nextPostion':'None','next':False,'keywords':keywords,'view':specific_context}
                return response_context
            elif specific_context == 'welcome_choose_course_time':
                if repeat == False:
                        fatherContext = PossibleContext.objects.get(context
                                                                            =
                                                                            specific_context)
                        context_detail = ContextDetail.objects.get(context
                                                                           =
                                                                           fatherContext,position='first')

                        final_message =\
                            context_detail.message
                        if language == 'English':
                            last_message = final_message
                        else:
                            last_message = self.translate_hindi(final_message)
                        length_list = []
                        one_month_dict = {'button_text':'1 Month','image':'https://s3.ap-south-1.amazonaws.com/subjecticon/course_length/one.png','hidden_variable':'1 Month'}
                        three_month_dict = {'button_text':'3 Months','image':'https://s3.ap-south-1.amazonaws.com/subjecticon/course_length/three.png','hidden_variable':'3 Months'}
                        six_month_dict = {'button_text':'6 Months','image':'https://s3.ap-south-1.amazonaws.com/subjecticon/course_length/six.png','hidden_variable':'6 Months'}
                        length_list.append(one_month_dict)
                        length_list.append(three_month_dict)
                        length_list.append(six_month_dict)
                        data ={'quick_reply':length_list}

                        #keywords = ["Choose later"]
                        response_context =\
                                {'context':specific_context,'message':last_message,'data':data,'repeat':True,'nextPosition':'second','next':False,'keywords':None,'view':specific_context}
                        return response_context

                if repeat:
                    if nextPosition == 'first':
                        fatherContext = PossibleContext.objects.get(context
                                                                            =
                                                                            specific_context)
                        context_detail = ContextDetail.objects.get(context
                                                                           =
                                                                           fatherContext,position='first')

                        final_message =\
                            context_detail.message.format(str(attempted),str(len(my_marks.allAnswers)),attempt_comment)
                        if language == 'English':
                            last_message = final_message
                        else:
                            last_message = self.translate_hindi(final_message)
                        one_month_dict = {'button_text':'1 Month','image':'https://s3.ap-south-1.amazonaws.com/subjecticon/course_length/one.png','hidden_variable':'1 Month'}
                        three_month_dict = {'button_text':'3 Months','image':'https://s3.ap-south-1.amazonaws.com/subjecticon/course_length/three.png','hidden_variable':'3 Months'}
                        six_month_dict = {'button_text':'6 Months','image':'https://s3.ap-south-1.amazonaws.com/subjecticon/course_length/six.png','hidden_variable':'6 Months'}
                        length_list.append(one_month_dict)
                        length_list.append(three_month_dict)
                        length_list.append(six_month_dict)
 
                        data ={'quick_reply':length_list}

                        response_context =\
                                {'context':specific_context,'message':final_message,'data':data,'repeat':True,'nextPosition':'second','next':False,'keywords':None,'view':specific_context}
                        return response_context
                    elif nextPosition == 'second':
                        if user_data != None and user_data!='none' and\
                        user_data!='None':
                            course_length = CourseLength()
                            course_length.student = student
                            course_length.length = str(user_data)
                            student_course = StudentCourse.objects.get(student =
                                                                       student)
                            course_length.course = student_course.course
                            course_length.save()

                            fatherContext = PossibleContext.objects.get(context
                                                                            =
                                                                            specific_context)
                            context_detail = ContextDetail.objects.get(context
                                                                           =
                                                                           fatherContext,position='second')

                            final_message =\
                                context_detail.message.format(str(user_data))
                            if language == 'English':
                                last_message = final_message
                            else:
                                last_message = self.translate_hindi(final_message)

                            #keywords = ["Next"]
                            response_context =\
                                    {'context':specific_context,'message':last_message,'data':None,'repeat':True,'nextPosition':'third','next':True,'keywords':None,'view':specific_context}
                            return response_context
                        else:
                            response_context = self.divert_context(me,'welcome_choose_course_time')
                            return response_context
 
                    elif nextPosition == 'third':
                        course_length =\
                        CourseLength.objects.get(student=student)
                        course = course_length.course

                        length = course_length.length
                        if length == '1 Month':
                            days = 30
                        elif length == '3 Months':
                            days = 90
                        elif length == '6 Months':
                            days = 180
                        else:
                            days = 100
                        try:
                            study_plan = self.create_study_plan(me,course,days)
                        except:
                            study_plan = StudyPlan.objects.get(student =
                                                               me.profile)
                        subjects = study_plan.subjects
                        sub_dict_list = []
                        for s in subjects:
                            subject_logo = SubjectLogo.objects.get(name=s)
                            sub_dict =\
                            {'button_text':s,'image':subject_logo.logo2,'hidden_variable':s}
                            sub_dict_list.append(sub_dict)
 
                        data ={'quick_reply':sub_dict_list}
                        fatherContext = PossibleContext.objects.get(context
                                                                        =
                                                                        specific_context)
                        context_detail = ContextDetail.objects.get(context
                                                                       =
                                                                       fatherContext,position='third')

                        final_message =\
                            context_detail.message
                        if language == 'English':
                            last_message = final_message
                        else:
                            last_message = self.translate_hindi(final_message)

                        #keywords = ["Next"]
                        response_context =\
                                {'context':specific_context,'message':last_message,'data':data,'repeat':True,'nextPosition':'fourth','next':False,'keywords':None,'view':specific_context}
                        return response_context
                    elif nextPosition == 'fourth':
                        if user_data != None and user_data!='none':
                            subject = str(user_data)
                            study_plan = StudyPlan.objects.get(student =
                                                               student)
                            chapters = study_plan.chapters.all()
                            chapters_list = []
                            for chap in chapters:
                                if chap.subject == subject:
                                    chapters_list.append(chap)
                            random_chapter = random.choice(chapters_list)
                            chapter_plan = ChapterPlan.objects.get(studyPlan =
                                                                   study_plan,chapter
                                                                   =
                                                                   random_chapter)
                            study_plan.current_subject = subject
                            study_plan.current_chapter_name =\
                            random_chapter.name
                            study_plan.save()
                            data =\
                                    {'subject':subject,'chapter':random_chapter.name,'overall_solve':chapter_plan.overall_sovle,'solved':chapter_plan.solved,'to_solve':chapter_plan.to_solve}
                            fatherContext = PossibleContext.objects.get(context
                                                                        =
                                                                        specific_context)
                            context_detail = ContextDetail.objects.get(context
                                                                       =
                                                                       fatherContext,position='fourth')

                            final_message =\
                                context_detail.message
                            if language == 'English':
                                last_message = final_message
                            else:
                                last_message = self.translate_hindi(final_message)


                            keywords = ["Choose different chapter","Next"]
                            response_context =\
                                {'context':specific_context,'message':last_message,'data':data,'repeat':False,'nextPosition':'none','next':False,'keywords':keywords,'view':'welcome_choose_course_time'}
                            return response_context
                        else:
                            response_context =\
                            self.divert_context(me,'welcome_choose_course_time',repeat=True,nextPosition='third')
                            return response_context
 

            elif specific_context == 'welcome_after_choose_aim':
                print('in choose after {}'.format(user_data))
                if user_data.strip() == 'Choose different chapter':
                    print('in difference chapter')
                    nextContextObj =\
                        PossibleContext.objects.get(context='free_change_chapter')
                    user_reply = None

                    chatHistory = ChatHistory.objects.get(student= me.profile)
                    response_context =\
                    self.fireNextContext(me,nextContextObj,user_reply,chatHistory)
                    return response_context


                islength = self.requisiteCourseLength(student.id)
                if islength == False:
                    nextContextObj =\
                        PossibleContext.objects.get(context='welcome_choose_course_time')
                    user_reply = None

                    chatHistory = ChatHistory.objects.get(student= me.profile)
                    response_context =\
                    self.fireNextContext(me,nextContextObj,user_reply,chatHistory)
                    return response_context
                else:
 
                    subs_data = []
                    aims_data = []
                    for i in user_data:
                        for j in i:
                            try:
                                marks = int(j)
                                aims_data.append(j)
                            except:
                                subs_data.append(j)

                    combined = list(zip(subs_data,aims_data))

                    for sub,aim in combined:
                        subjectAims = StudentSubjectAim()
                        subjectAims.student = student
                        subjectAims.subject = sub
                        subjectAims.aim = aim
                        subjectAims.save()

                    student_aims = StudentSubjectAim.objects.filter(student
                                                                    =student)
                    aims = []
                    for si in student_aims:
                        si_dict = {'subject':si.subject,'aim':si.aim}
                        aims.append(si_dict)


                    father_context = PossibleContext.objects.get(context =
                                                                    specific_context)

                    context_detail = ContextDetail.objects.filter(context =
                                                                father_context)
     
                    dc_list = []
                    for i in context_detail:
                        dc_list.append(i)
                    to_be_sent = random.choice(dc_list)
                    message = to_be_sent.message
                    if language == 'English':
                        final_message = to_be_sent.message.replace('{}',str(aims))
                    else:
                        final_message = to_be_sent.messageHindi.replace('{}',str(aims))
                    keywords = ["Choose different chapter",'Next']
                    response_context =\
                            {'context':specific_context,'message':final_message,'data':None,'repeat':False,'nextPostion':'None','next':False,'keywords':keywords,'view':specific_context}
                    return response_context


        elif family == 'analysis':
            if specific_context == 'analysis_chapterwise_weakareas':
                study_plan = StudyPlan.objects.get(student = student)
                subject = study_plan.current_subject
                chapter_name = chapter_name_table.name
                chapter_obj = SubjectChapters.objects.get(subject=subject,name=chapter_name)
                chapter_code = chapter_obj.code
                fatherContext = PossibleContext.objects.get(context=specific_context)
                context_detail = ContextDetail.objects.get(context=fatherContext,position='first')

                try:
                    weak_areas_cache =\
                    StudentWeakAreasChapterCache.objects.get(student=me.profile,subject
                                                        = subject,chapter=chapter_code)
                    
                    accuracy = weak_areas_cache.accuracy
                    totalRight = weak_areas_cache.totalRight
                    totalWrong = weak_areas_cache.totalWrong
                    totalSkipped = weak_areas_cache.totalSkipped
                    skippedPercent = weak_areas_cache.skippedPercent
                    totalAttempted = weak_areas_cache.totalAttempted
                    message = context_detail.message
                    if accuracy < 40:
                        message = """This is not a satisfactory result. You should work hard in {} . I will guide you on your weaknesses. """.format(chapter_name)
                    elif 40 < accuracy <= 60:
                        message = """Not good. We should work on {} . I will guide you on your weaknesses. """.format(chapter_name)
                    elif 60 < accuracy <= 80:
                        message = """Not bad. But we can do even better in {} . I will guide you on how to increase your score. """.format(chapter_name)                       
                    elif accuracy > 80:
                        message = """Good. I think you are doing good in {}. You should practice the chapter you haven't mastered yet. """.format(chapter_name)
                    if language == 'English':
                        final_message = message
                    else:
                        final_message = self.translate_hindi(message)
                    
                    data =\
                    {'chapter':chapter_name,'accuracy':accuracy,'totalRight':totalRight,'totalWrong':totalWrong,'totalSkipped':totalSkipped,'skippedPercent':skippedPercent,'totalAttempted':totalAttempted}
                    keywords = ['Choose different chapter','Next']
                    response_context =\
                                    {'context':specific_context,'message':final_message,'data':data,'repeat':True,'nextPosition':'second','next':False,'keywords':keywords,'view':weak_areas_chapter}
                except:
                    message = """You havent' studied this {} yet. Lets start now. """.format(chapter_name)
                    if language == 'English':
                        final_message = message
                    else:
                        final_message = self.translate_hindi(message)
                    response_context =\
                                    {'context':specific_context,'message':final_message,'data':None,'repeat':True,'nextPosition':'second','next':False,'keywords':keywords,'view':weak_areas_chapter}
                return Response(context)
            if specific_context == 'analysis_subjectwise_weakareas':
                study_plan = StudyPlan.objects.get(student = student)
                subject = study_plan.current_subject
                chapter_name = chapter_name_table.name
                chapter_obj = SubjectChapters.objects.get(subject=subject,name=chapter_name)
                chapter_code = chapter_obj.code
                fatherContext = PossibleContext.objects.get(context=specific_context)
                context_detail = ContextDetail.objects.get(context=fatherContext,position='first')

                try:
                    weak_areas_list = []
                    weak_areas_cache =\
                    StudentWeakAreasChapterCache.objects.get(student=me.profile,subject
                                                        = subject,chapter=chapter_code)
                    very_poor_areas = []
                    for i in weak_areas_cache:
                        accuracy = i.accuracy
                        totalRight = i.totalRight
                        totalWrong = i.totalWrong
                        totalSkipped = i.totalSkipped
                        skippedPercent = i.skippedPercent
                        totalAttempted = i.totalAttempted
                        chapter_weakness =\
                    {'chapter':chapter_name,'accuracy':accuracy,'totalRight':totalRight,'totalWrong':totalWrong,'totalSkipped':totalSkipped,'skippedPercent':skippedPercent,'totalAttempted':totalAttempted}
                        weak_areas_list.append(chapter_weakness)
                        if accuracy < 40:
                            very_poor_areas.append({'name':chapter_name,'accuracy':accuracy})
                    message = context_detail.message

                    data = {weak_areas_list}                    
                    if language == 'English':
                        last_message = """Upon some analysis ..."""
                    else:
                        last_message = self.translate_hindi(last_message)
                    if len(very_poor_areas) > 0:
                        for i in very_poor_areas:
                            message = """You are doing poorly in {} with accuracy of only {}""".format(i['name'],i['accuracy'])
                            if language == 'English':
                                final_message = message
                            else:
                                final_message = self.translate_hindi(message)
                            last_message += final_message + '\n'
                    else:
                        message = """Impressive !! You are doing good in every chapter you have studied till now in {}""".format(subject)
                        if language == 'English':
                            last_message = message
                        else:
                            last_message = self.translate_hindi(message)
                            
                    keywords = ['Choose different chapter','Next']
                    response_context =\
                                    {'context':specific_context,'message':last_message,'data':data,'repeat':False,'nextPosition':'none','next':False,'keywords':keywords,'view':weak_areas_chapter}
                except:
                    message = """You havent' studied this {} yet. Lets start now. """.format(chapter_name)
                    if language == 'English':
                        final_message = message
                    else:
                        final_message = self.translate_hindi(message)
                    response_context =\
                                    {'context':specific_context,'message':final_message,'data':None,'repeat':True,'nextPosition':'second','next':False,'keywords':keywords,'view':weak_areas_chapter}
                return Response(context)

            if specific_context == 'analysis_specific_test':
                fine =  self.requisiteFirstTest(student.id)
                if fine == False:
                    nextContextObj =\
                                PossibleContext.objects.get(context='tests_first_test')
                    user_reply = None

                    chatHistory = ChatHistory.objects.get(student= me.profile)
                    response_context =\
                    self.fireNextContext(me,nextContextObj,user_reply,chatHistory)
                    return response_context
                else:

                    my_marks = SSCOnlineMarks.objects.filter(student =
                                                      student).order_by('pk')
                    all_marks = []
                    for i in my_marks:
                        all_marks.append(i)
                    last_test = all_marks[-1]
                    my_marks = last_test
                    rightAnswers = len(my_marks.rightAnswers)
                    wrongAnswers = len(my_marks.wrongAnswers)
                    attempted = len(my_marks.rightAnswers) + len(my_marks.wrongAnswers)
                    total_questions = rightAnswers + wrongAnswers +\
                    len(my_marks.skippedAnswers)
                    if repeat == False:
                        if nextPosition == 'zero':
                            if language == 'English':
                                zero_message = """I am analyzing you performance ..."""
                            else:
                                zero_message = """मैं आपके प्रदर्शन का विश्लेषण कर रहा हूं"""
                            #keywords = ["Next"]
                            response_context =\
                                    {'context':specific_context,'message':zero_message,'data':None,'repeat':True,'nextPosition':'first','next':True,'keywords':None,'view':specific_context}
                            return response_context


                    if repeat:
                        if nextPosition == 'zero':
                            zero_message = """I am analyzing you performance ..."""
                            #keywords = ['Next']
                            response_context =\
                                    {'context':specific_context,'message':zero_message,'data':None,'repeat':True,'nextPosition':'first','next':True,'keywords':None,'view':specific_context}
                            return response_context


                        if nextPosition == 'first':
                            fatherContext = PossibleContext.objects.get(context
                                                                        =
                                                                        specific_context)
                            context_detail = ContextDetail.objects.get(context
                                                                       =
                                                                       fatherContext,position='first')

                            percent_attempted = (attempted / total_questions ) * 100
                            attempt_comment,attempt_comment_hindi = self.analysis_specific_test_first(percent_attempted)
                            if language == 'English':
                                final_message =\
                                context_detail.message.format(str(attempted),str(total_questions),attempt_comment)
                            else:
                                final_message = \
                                context_detail.messageHindi.format(str(attempted),str(total_questions),attempt_comment_hindi)

                            data ={'attempted':percent_attempted,'graph_type':'attempt'}

                            keywords = ['Next']
                            response_context =\
                                    {'context':specific_context,'message':final_message,'data':data,'repeat':True,'nextPosition':'second','next':False,'keywords':keywords,'view':specific_context}
                            return response_context
                        elif nextPosition == 'second':
                            fatherContext = PossibleContext.objects.get(context
                                                                        =
                                                                        specific_context)
                            context_detail = ContextDetail.objects.get(context
                                                                       =
                                                                       fatherContext,position='second')


                            score = my_marks.marks
                            percent_score = (score/ last_test.test.max_marks) * 100

                            score_comment,score_comment_hindi = self.analysis_specific_test_second(percent_score)
                            data={'score':percent_score,'graph_type':'score','rightAnswers':rightAnswers,'wrongAnswers':wrongAnswers}
                            if language == 'English':
                                final_message =\
                                context_detail.message.format(str(score),str(last_test.test.max_marks),score_comment)
                            else:
                                final_message =\
                                context_detail.messageHindi.format(str(score),str(last_test.test.max_marks),score_comment_hindi)

                            keywords = ['Next']
                            response_context =\
                                    {'context':specific_context,'message':final_message,'data':data,'repeat':True,'nextPosition':'third','next':False,'keywords':keywords,'view':specific_context}
                            return response_context
                        elif nextPosition == 'third':
                            fatherContext = PossibleContext.objects.get(context
                                                                        =
                                                                        specific_context)
                            context_detail = ContextDetail.objects.get(context
                                                                       =
                                                                       fatherContext,position='third')


                            timeTaken = my_marks.timeTaken
                            time_comment, time_comment_hindi =\
                            self.analysis_specific_test_third(timeTaken)

                            if timeTaken < 60:
                                timeTaken = '{} seconds'.format(timeTaken)
                                mins = ''
                                secs = timeTaken
                                timeTaken = '{} seconds'.format(secs)
                            else:
                                mins = int(timeTaken/60)
                                secs = timeTaken%60
                                timeTaken = '{} minutes and {} seconds'.format(str(mins),str(secs))
                            data ={'time':timeTaken,'graph_type':'timeTaken'}

                            if language == 'English':
                                final_message =\
                                context_detail.message.format(str(mins),str(secs),time_comment)
                            else:
                                final_message =\
                                context_detail.messageHindi.format(str(mins),str(secs),time_comment_hindi)

                            keywords = ['Next']
                            response_context =\
                                    {'context':specific_context,'message':final_message,'data':data,'repeat':True,'nextPosition':'fourth','next':False,'keywords':keywords,'view':specific_context}
                            return response_context
                        elif nextPosition == 'fourth':
                            fatherContext = PossibleContext.objects.get(context
                                                                        =
                                                                        specific_context)
                            context_detail = ContextDetail.objects.get(context
                                                                       =
                                                                       fatherContext,position='fourth')

                            final_ranking,my_rank,totalRank =\
                                    self.get_specific_testRank(my_marks.test.id,student.id)
                            context_detail
                            if language == 'English':
                                final_message =\
                                context_detail.message.format(str(my_rank),totalRank)
                            else:
                                final_message =\
                                context_detail.messageHindi.format(str(my_rank),str(totalRank))
                            keywords = ['Next','See test performance in detail',"Choose different chapter"] 
                            data =\
                                    {'test_id':my_marks.test.id,'subject':my_marks.test.sub,'graph_type':'detail_performance'}
                            response_context =\
                                    {'context':specific_context,'message':final_message,'data':data,'repeat':False,'nextPosition':'None','next':False,'keywords':keywords,'view':specific_context}
                            return response_context



        elif family == 'studyPlan':
            if specific_context == 'study_plan_last_test':
                study_plan = StudyPlan.objects.get(student =
                                                   me.profile)
                subject = study_plan.current_subject
                try:
                    test_chapter = study_plan.current_chapter_name
                except:
                    test_chapter = study_plan.current_chapter_code
                    sub_chapter = SubjectChapters.objects.get(subject =
                                                              subject,code=test_chapter)
                    test_chapter = sub_chapter.name

                chapters = study_plan.chapters.all()
                chapter = 0
                for chap in chapters:
                    if chap.name == test_chapter and chap.subject\
                    == subject:
                        chapter = chap

                chapter_plan = ChapterPlan.objects.get(studyPlan =
                                                       study_plan,chapter
                                                       =
                                                       chapter)
                data =\
                        {'subject':subject,'chapter':test_chapter,'overall_solve':chapter_plan.overall_sovle,'solved':chapter_plan.solved,'to_solve':chapter_plan.to_solve}
                fatherContext = PossibleContext.objects.get(context
                                                            =
                                                            specific_context)
                context_detail = ContextDetail.objects.get(context
                                                           =
                                                           fatherContext,position='first')

                final_message =\
                    context_detail.message.format(test_chapter)
                if language == 'English':
                    last_message = final_message
                else:
                    last_message = self.translate_hindi(final_message)


                keywords = ["Choose different chapter","Next"]
                response_context =\
                    {'context':specific_context,'message':last_message,'data':data,'repeat':False,'nextPosition':'none','next':False,'keywords':keywords,'view':'welcome_choose_course_time'}
                return response_context
            else:
                response_context = self.divert_context(me,'free_change_chapter')
                return response_context
 

           










        elif family == 'tests':
            if specific_context == 'tests_chapter_test':
                if user_data.strip() == 'Choose different chapter':
                    print('in difference chapter')
                    response_context =\
                    self.divert_context(me,'free_change_chapter')
                    return response_context
 


                #latest_data =\
                #    LatestChatData.objects.get(student=me.profile)
                #test_data = latest_data.data
                #test_chap = test_data.split(',')[1]
                #test_sub = test_data.split(',')[0]
                #test_chapter = str(user_data)
                study_plan = StudyPlan.objects.get(student = me.profile)
                test_sub = study_plan.current_subject
                try:
                    test_chap = study_plan.current_chapter_name
                except:
                    test_chapter = study_plan.current_chapter_code
                    sub_chapter =\
                    SubjectChapters.objects.get(subject=test_sub,code =
                                                test_chapter)
                    test_chap = sub_chapter.name

                    
                chapters = study_plan.chapters.all()
                chapter = 0
                for chap in chapters:
                    if chap.name == test_chap and chap.subject == test_sub:
                        chapter = chap

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
                    self.find_topics(te,test_chap)


                if isChapter == False:
                    data = None
                    last_message = 'Sorry no test available at this time, please choose any other chapter.'
                else:
                    last_message = 'I got this test for you . '
                data_dict =\
                    {'test_id':te.id,'subject':test_sub,'numberQuestions':num_questions}

                fatherContext = PossibleContext.objects.get(context = specific_context)
                context_detail = ContextDetail.objects.get(context
                                                       =fatherContext,position='first')
                message = context_detail.message
                if language == 'English':
                    last_message = message
                else:
                    last_message = self.translate_hindi(message)




                response_context =\
                        {'context':specific_context,'message':last_message,'data':data_dict,'repeat':False,'nextPosition':'None','view':'tests_first_test'}
                return response_context





            if specific_context == 'tests_first_test':
                prev_tests = SSCOnlineMarks.objects.filter(student =
                                                           student)
                if len(prev_tests) == 0:
                    study_plan = StudyPlan.objects.get(student=student)
                    test_sub = study_plan.current_subject
                    test_chap = study_plan.current_chapter_name
                    chapters = study_plan.chapters.all()
                    chapter = 0
                    for chap in chapters:
                        if chap.name == test_chap and chap.subject == test_sub:
                            chapter = chap

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
                        self.find_topics(te,test_chap)


                    if isChapter == False:
                        data = None
                        last_message = 'Sorry no test available at this time, please choose any other chapter.'
                    else:
                        last_message = 'I got this test for you . '
                    data_dict =\
                        {'test_id':te.id,'subject':test_sub,'numberQuestions':num_questions}

                    fatherContext = PossibleContext.objects.get(context = specific_context)
                    context_detail = ContextDetail.objects.get(context
                                                           =fatherContext,position='first')
                    message = context_detail.message
                    if language == 'English':
                        last_message = message
                    else:
                        last_message = self.translate_hindi(message)




                    response_context =\
                            {'context':specific_context,'message':last_message,'data':data_dict,'repeat':False,'nextPosition':'None','view':'tests_first_test'}
                    return response_context

####################################3
                    #test = SSCKlassTest.objects.filter(testTakers = student)
                    #take_test = test[0]
                    #subject = take_test.sub
                    #test_id = take_test.id
                    #quests = take_test.sscquestions_set.all()
                    #number_questions = len(quests)
                    #if language == 'English':
                    #    to_be_sent = """Step 1: Take this test. Based on your performance I will guide you further."""
                    #else:
                    #    to_be_sent = """चरण 1 : यह टेस्ट लें . इस टेस्ट के प्रदर्शन के अनुसार आपको मैं गाइड कर्रूँगा """
                    #print('in first test shold go with nextPostion zero')
                    #data_dict =\
                    #{'test_id':test_id,'subject':subject,'numberQuestions':number_questions}
                    #keywords = ['Start Test']
                    #response_context =\
                    #        {'context':specific_context,'message':to_be_sent,'data':data_dict,'repeat':False,'nextPosition':'zero','next':False,'keywords':keywords,'view':specific_context}
                #else#:
                    #test = SSCKlassTest.objects.filter(testTakers = student)

                    #prev_tests = SSCOnlineMarks.objects.filter(student =
                    #                                       student)
                    #taken_tests = []
                    #for i in prev_tests:
                    #    taken_tests.append(i.test.id)

                    #all_tests = []
                    #for i in test:
                    #    if i.id in taken_tests:
                    #        pass
                    #    else:
                    #        all_tests.append(i)
                    #try:
                    #    to_take = random.choice(all_tests)
                    #except:
                    #    to_be_sent = """Sorry I couldn't find any test for you.I will be back soon with a test."""

                    #    data_dict =\
                    #    {'test_id':None,'subject':None,'numberQuestions':None}
                    #    response_context =\
                    #            {'context':specific_context,'message':to_be_sent,'data':data_dict,'repeat':False,'nextPosition':'None','view':specific_context}
                    #    return response_context


                    #subject = to_take.sub
                    #test_id = to_take.id
                    #quests = to_take.sscquestions_set.all()
                    #number_questions = len(quests)
                    #if language == 'English':
                    #    to_be_sent = """Take this test."""
                    #else:
                    #    to_be_sent = """यह टेस्ट लें """

                    #data_dict =\
                    #{'test_id':test_id,'subject':subject,'numberQuestions':number_questions}
                    #keywords = ['Next','Start Test']
                    #response_context =\
                    #        {'context':specific_context,'message':to_be_sent,'data':data_dict,'repeat':False,'nextPosition':'zero','next':False,'keywords':keywords,'view':specific_context}


        if family == 'challenge':
            if repeat == False:
                if specific_context == 'challenge_specific_test':
                    if user_data.strip() == 'Choose different chapter':
                        print('in difference chapter')
                        nextContextObj =\
                            PossibleContext.objects.get(context='free_change_chapter')
                        user_reply = None

                        chatHistory = ChatHistory.objects.get(student= me.profile)
                        response_context =\
                        self.fireNextContext(me,nextContextObj,user_reply,chatHistory)
                        return response_context


                    print('specific context of challenge specific test')
                    fatherContext = PossibleContext.objects.get(context = specific_context)
                    context_detail = ContextDetail.objects.get(context
                                                               =fatherContext,position='first')


                    my_marks = SSCOnlineMarks.objects.filter(student =
                                                      student).order_by('pk')
                    all_marks = []
                    for i in my_marks:
                        all_marks.append(i)
                    last_test = all_marks[-1]
                    my_marks = last_test
                    final_ranking,my_rank,totalRank =\
                            self.get_specific_testRank(my_marks.test.id,student.id)
                
                    final_message =\
                        context_detail.message.format(str(my_rank),totalRank)
                    if language == 'English':
                        last_message = final_message
                    else:
                        last_message = self.translate_hindi(final_message)
                    data =final_ranking
                    response_context =\
                                {'context':specific_context,'message':last_message,'data':data,'repeat':True,'nextPosition':'second','next':False,'keywords':None,'view':specific_context}
                    return response_context
            if repeat:
                if nextPosition == 'second':
                    if user_data != None and user_data != 'none':
                        student_challenged =\
                        Student.objects.get(studentuser__username =
                                            str(user_data))
                        fatherContext = PossibleContext.objects.get(context = specific_context)
                        context_detail = ContextDetail.objects.get(context
                                                                   =fatherContext,position='second')


               
                        final_message =\
                            context_detail.message.format(str(student_challenged.name))
                        if language == 'English':
                            last_message = final_message
                        else:
                            last_message = self.translate_hindi(final_message)
                        keywords = ['Next']
                        response_context =\
                                {'context':specific_context,'message':last_message,'data':None,'repeat':True,'nextPosition':'third','next':False,'keywords':keywords,'view':specific_context}
                        return response_context
                    else:
                        nextContextObj =\
                            PossibleContext.objects.get(context='challenge_specific_test')
                        user_reply = None

                        chatHistory = ChatHistory.objects.get(student= me.profile)
                        response_context =\
                        self.fireNextContext(me,nextContextObj,user_reply,chatHistory)
                        return response_context
 

                elif nextPosition == 'third':
                        fatherContext = PossibleContext.objects.get(context = specific_context)
                        context_detail = ContextDetail.objects.get(context
                                                                   =fatherContext,position='third')


               
                        final_message =\
                            context_detail.message
                        if language == 'English':
                            last_message = final_message
                        else:
                            last_message = self.translate_hindi(final_message)

                        keywords = ['Next']
                        response_context =\
                                {'context':specific_context,'message':last_message,'data':None,'repeat':False,'nextPosition':'none','next':False,'keywords':keywords,'view':specific_context}
                        return response_context

 
 

            if specific_context == 'challenge_others_first':
                my_subjects = Subject.objects.filter(student = student)
                for sub in my_subjects:
                    try:
                        subjectRanks = SubjectRank.objects.get(subject=sub)
                        sub_ranks = subjectRanks.students
                        if student in sub_ranks:
                            my_rank = sub_ranks.index(student)
                            my_rank = my_rank + 1
                            other_students = []
                            for i in range(my_rank -6,my_rank+1):
                                stud =\
                                other_students.append(sub_ranks.index(i))
                            student_details = []
                            for i in other_students:
                                try:
                                    stud_other = Student.objects.get(id = i)
                                    stud_detail =\
                                    StudentDetails.objects.get(student = stud_other.studentuser)
                                except:
                                    pass

                            response_context =\
                            {'context':specific_context,'message':to_be_sent,'data':data_dict}



                    except:
                        pass
                return False




                return response_context
 
 
        elif family == 'recommendation':
            pass
        elif family == 'end':
            if specific_context == 'end_message':
                to_be_sent = """I will be back. If you liked me, please share. """
                response_context =\
                    {'context':specific_context,'message':to_be_sent,'data':None}
                return response_context
          
class saveBodhiChatAPIView(APIView):
    def post(self,request,*args,**kwargs):
        aws_keys = AWSKey.objects.all()
        me = Studs(self.request.user)
        data = request.data
        chat_data = data['chatData']
        if type(chat_data) == list:
            print(chat_data)
            for i in chat_data:
                obj_details = json.dumps(i)
                obj_load = json.loads(obj_details)
                for v in obj_load.values():
                    if type(v) == float:
                        v = Decimal(v)
              
        aws_key = aws_keys[0]
        print('this is the key {}'.format(aws_key.accessKey))
        ACCESS_KEY_ID = aws_key.accessKey
        ACCESS_SECRET_KEY = aws_key.secretKey
        client = boto3.resource(
        'dynamodb',
        aws_access_key_id = ACCESS_KEY_ID,
        aws_secret_access_key = ACCESS_SECRET_KEY,
        region_name = 'ap-south-1'
        )
        table = client.Table('bodhichattest')
        if type(chat_data) == list:
            for i in chat_data:
                print(i)
                try:
                    res = table.update_item(
                        Key = { 
                                'student_id':str(me.profile.id)
                            },  
                    UpdateExpression = """SET  chatData = list_append(chatData,:cd)""",
                    ExpressionAttributeValues={
                                ':cd': [i],

                            },  
                    ReturnValues="UPDATED_NEW"

                    )
                    print('db updated')
                except Exception as e:
                    print('amazon db error {}'.format(str(e)))
                    table.put_item(
                    Item={

                                'student_id':str(me.profile.id),
                                'chatData': [i],

                        }
                    )
                    print('db created')
        else:
            try:
                res = table.update_item(
                    Key = { 
                            'student_id':str(me.profile.id)
                        },  
                UpdateExpression = """SET  chatData = list_append(chatData,:cd)""",
                ExpressionAttributeValues={
                            ':cd': [chat_data],

                        },  
                ReturnValues="UPDATED_NEW"

                )
                print('db updated')
            except Exception as e:
                print('amazon db error {}'.format(str(e)))
                table.put_item(
                Item={

                            'student_id':str(me.profile.id),
                            'chatData': [chat_data],

                    }
                )
                print('db created')

        context = {'chat_data':chat_data}
        return Response(context)

    
        #try:
        #    res = table.update_item(
        #        Key = { 
        #                'student_id':str(me.profile.id)
        #            },  
        #    UpdateExpression = """SET  sentByMe = list_append(sentByMe,:sbm),text
        #        =list_append(text,:te),loading: list_append(loading,:lod),viewType:
        #        list_append(viewType,:vt),clickable:list_append(clickable,:ck),data:
        #        list_append(data,:da),when:list_append(when,:wh)""",
        #    ExpressionAttributeValues={
        #                ':sbm': [bool(sentByMe)],
        #                ':te': [str(messageText)],
        #                ':lod': [bool(loading)],
        #                ':vt': [str(viewType)],
        #                ':ck': [bool(clickable)],
        #                ':da': [str(data_front_end)],
        #                ':wh': [str(timezone.now())],

        #            },  
        #    ReturnValues="UPDATED_NEW"

        #    )
        #    print('db updated')
        #except Exception as e:
        #    print('amazon db error {}'.format(str(e)))
        #    table.put_item(
        #    Item={

        #                'student_id':str(me.profile.id),
        #                'sentByMe': [bool(sentByMe)],
        #                'text': [str(messageText)],
        #                'loading': [bool(loading)],
        #                'viewType': [str(viewType)],
        #                'clickable': [bool(clickable)],
        #                'data': [str(data)],
        #                'when': [str(timezone.now())],


        #        }
        #    )
        #    print('db created')


class getBodhiChatAPIView(APIView):
    def get(self,request):
        aws_keys = AWSKey.objects.all()
        me = Studs(self.request.user)
        aws_key = aws_keys[0]
        print('this is the key {}'.format(aws_key.accessKey))
        ACCESS_KEY_ID = aws_key.accessKey
        ACCESS_SECRET_KEY = aws_key.secretKey
        client = boto3.resource(
        'dynamodb',
        aws_access_key_id = ACCESS_KEY_ID,
        aws_secret_access_key = ACCESS_SECRET_KEY,
        region_name = 'ap-south-1'
        )
        table = client.Table('bodhichattest')
        student_id = str(me.profile.id)
        try:
            response = table.query(KeyConditionExpression=Key('student_id').eq(student_id))
            chatData2 = response['Items'][0]['chatData']
            context = {'chatHistory':chatData2}
        except:
            context = {'chatHistory':None}
        return Response(context)

