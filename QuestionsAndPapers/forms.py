from django.contrib.auth.models import User,Group
from django import forms
from basicinformation.models import *
from basicinformation.tasks import *
from .models import *

class CreateTimeTableForm(forms.ModelForm):
    class Meta:
        model = TimeTable
        fields = [
            'date',
            'timeStart',
            'timeEnd',
            'batch',
            'sub',
            'note',

        ]
        read_only_fields = ('created')
