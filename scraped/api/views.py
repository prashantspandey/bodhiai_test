from rest_framework import generics
from rest_framework.views import APIView
from scraped.models import *
from basicinformation.models import *
from .serializers import *
from QuestionsAndPapers.models import *
from basicinformation.marksprediction import *
from rest_framework.response import *


class CreateJobsListAPIView(APIView):
    pass
