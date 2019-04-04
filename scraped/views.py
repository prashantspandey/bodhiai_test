from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
import os.path

import pickle
from django.http import Http404, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from datetime import timedelta
import math
from datetime import date
import numpy as np
import pandas as pd
from more_itertools import unique_everseen
from django.contrib.auth.models import User, Group
from .models import *
from django.utils import timezone
from django.contrib.staticfiles.templatetags.staticfiles import static
from Recommendations.models import *
from .marksprediction import *
from operator import itemgetter
from io import BytesIO as IO
from basicinformation.tasks import *
from celery.result import AsyncResult
from django.core import serializers
from time import sleep
from membership.forms import StudentInformationForm,StudentForm
from .tasks import *


# Create your views here.


