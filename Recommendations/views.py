from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    context = {'hello':'hello'}
    return render(request,'basicinformation/index2.html',context)


