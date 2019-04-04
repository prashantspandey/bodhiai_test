from rest_framework import generics
from django.utils import timezone
from celery.result import AsyncResult 
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from more_itertools import unique_everseen
from basicinformation.models import *
from django.http import Http404, HttpResponse
from .serializers import *
from QuestionsAndPapers.api.views import *
from basicinformation.marksprediction import *
from QuestionsAndPapers.models import *
from basicinformation.models import * 
from basicinformation.marksprediction import * 
from membership.api.views import add_subjects
import json
from basicinformation.nameconversions import *
from membership.api.serializers import *
from rest_framework.response import Response
from basicinformation.tasks import *
from Recommendations.api.serializers import *
from Recommendations.models import *
import datetime

class StudentSubjectsAPIView(APIView):
    def get(self,request,format=None):
        me = Studs(self.request.user)
        #subjects = me.my_subjects_names()
        subjects = me.get_taken_subjects()
        print(subjects)
        context = {'subjects':subjects}
        return Response(context)


class StudentGetChaptersAPIView(APIView):
    def post(self,request,*args,**kwargs):
        me = Studs(self.request.user)
        data = request.data
        subject = data['subject']

        chapters = SubjectChapters.objects.filter(subject = subject)
        chapter_serializer = SubjectChapterSerializer(chapters,many=True)
        return Response(chapter_serializer.data)


class StudentGetCoceptsAPIView(APIView):
    def post(self,request,*args,**kwargs):
        code = request.POST['chapter']
        subject = request.POST['subject']
        con = Concepts.objects.filter(chapter = code,subject=subject)
        if len(con) == 0:
            return Response({'concepts':'no concepts'})
        else:

            concept_serializer = ConceptsBriefSerializer(con,many=True)
            context = {'concepts':concept_serializer.data}
            return Response(context)

class StudentGetContentAPIView(APIView):
    def post(self,request,*args,**kwargs):
        concept_id = request.POST['concept_id']
        lang = request.POST['lang']
        con_url = []
        con_title = []
        concept = Concepts.objects.get(id = concept_id)
        content = concept.content.all()
        print(type(content))
        for i in content:
            if lang.lower() in str(i.lang).lower():
                con_url.append(i.url)
                con_title.append(i.title)

        context = {'url':con_url,'title':con_title}
        return Response(context)

class TeacherSubjectsAPIView(APIView):
    def get(self,request):
        me = Teach(self.request.user)
        subjects = me.my_subjects_names()
        context = {'subjects':subjects}
        return Response(context)

class TeacherGetChaptersAPIView(APIView):
    def post(self,request,*args,**kwargs):
        subject = request.POST['subject']
        chapters = SubjectChapters.objects.filter(subject = subject)
        chapter_serializer = SubjectChapterSerializer(chapters,many=True)
        return Response(chapter_serializer.data)

class CourseSubjects(APIView):
    def post(self,request):
        data = request.data
        course = data['course']
        course = Course.objects.get(course_name=course)
        subject_chapters = SubjectChapters.objects.filter(course = course)
        subject_list=  []
        for i in subject_chapters:
            subject_list.append(i.subject)
        subjects = list(unique_everseen(subject_list))
        context = {'subjects':subjects}
        return Response(context)
