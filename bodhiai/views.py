from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone

from basicinformation.models import InterestedPeople
def index(request):
    context = {'hello':'hello'}
    return render(request,'basicinformation/index_b2c.html',context)

def interested_people(request):
    if 'tel' in request.GET:
        number = request.GET['tel']
        interested_user = InterestedPeople()
        interested_user.number = number
        interested_user.time = timezone.now()
        interested_user.save()
        return render(request,'basicinformation/404.html')
