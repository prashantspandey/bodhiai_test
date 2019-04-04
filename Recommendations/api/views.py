from django.utils import timezone
from rest_framework import generics
from rest_framework import generics
from django.utils import timezone
from celery.result import AsyncResult 
from rest_framework.decorators import api_view
from rest_framework.views import APIView
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
from Recommendations.models import *
import datetime
from apiclient.discovery import build 
from apiclient.errors import HttpError 
from oauth2client.tools import argparser 
import pprint 
#import matplotlib.pyplot as pd 



class StudentChapterYoutubeRecommendationsAPIView(APIView):
    def get(self,request):
        me = Studs(self.request.user)
        weak_area = StudentWeakAreasChapterCache.objects.filter(student =
                                                                me.profile)
        recommendation_list = []
        for wa in weak_area:
            sub = wa.subject
            chap = wa.chapter
            try:
                subject_chapter = SubjectChapters.objects.get(subject = sub,code =
                                                              chap)
                chap_name = subject_chapter.name
                try:
                    youtube_video = YoutubeExternalVideos.objects.filter(subject =
                                                                  sub,chapter =
                                                                  chap_name)
                    for num,yv in enumerate(youtube_video):
                        if num == 1:
                            break
                        recommendation_dict =\
                            {'link':yv.link,'title':yv.title,'chapter':chap_name,'subject':sub,'thumbnail':yv.thumbnail}
                        recommendation_list.append(recommendation_dict)
                except Exception as e:
                    print(str(e))
            except Exception as e:
                print(str(e))
        context = {'recommendations':recommendation_list}
        return Response(context)

class StudentChapterWiseRecommendationAPIView(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        chapter = data['chapter']
        subject = data['subject']
        try:
            recommendation_list = []
            subject_chapter = SubjectChapters.objects.get(subject = subject,code =
                                                              chapter)
            chap_name = subject_chapter.name
            try:
                youtube_video = YoutubeExternalVideos.objects.filter(subject =
                                                                  subject,chapter =
                                                                  chap_name)
                for num,yv in enumerate(youtube_video):
                    if num == 3:
                        break
                    recommendation_dict =\
                            {'link':yv.link,'title':yv.title,'thumbnail':yv.thumbnail}
                    recommendation_list.append(recommendation_dict)
            except Exception as e:
                context = {'videos':str(e),'subject':subject,'chapter':chapter}
        except Exception as e:
            context = {'videos':str(e),'subject':subject,'chapter':chapter}
        context =\
            {'videos':recommendation_list,'subject':subject,'chapter':chapter}
        return Response(context)

        
 
