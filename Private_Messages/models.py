from django.db import models
from django.contrib.auth.models import User
from basicinformation.models import *

class PrivateMessage(models.Model):
    sender = models.ForeignKey(User,related_name = 'sender')
    receiver = models.ForeignKey(User,related_name = 'receiver')
    subject = models.CharField(max_length = 100, blank = True,null = True)
    body = models.TextField()
    sent_date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        if self.subject !=None:
            return self.subject
        else:
            return self.body[:50]

class Announcement(models.Model):
    announcer = models.ForeignKey(Teacher)
    listener = models.ManyToManyField(Student)
    text = models.CharField(max_length= 1000)
    date = models.DateField(auto_now_add = True)
    klass = models.ManyToManyField(klass,blank=True)

    def __str__(self):
        return self.text

