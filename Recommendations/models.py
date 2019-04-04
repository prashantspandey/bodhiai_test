from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from basicinformation.models import *
# Create your models here.

class RecommendedContent(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    lang = models.CharField(max_length=50)
    contentType = models.CharField(max_length=100)
    chapter = models.FloatField()
    subject = models.CharField(max_length = 50)
    date = models.DateField(auto_now_add=True)
    source = models.CharField(max_length =200,null=True,blank=True)

    def __str__(self):
        return str(self.subject) + str(self.chapter) + str(self.title)

#class Concept(models.Model):
#    question = models.ForeignKey(SSCquestions,null=True,blank=True)
#    name = models.CharField(max_length=200)
#    content = models.ForeignKey(RecommendedContent,null=True,blank=True)
#    subject = models.CharField(max_length =200)
#    chapter = models.FloatField(blank=True,null=True)
#    concept_number = models.IntegerField(blank=True,null=True)
#
#
#    def __str__(self):
#        return str(self.subject) +' '+ str(self.chapter) 

class Concepts(models.Model):
    name = models.CharField(max_length=200)
    content = models.ManyToManyField(RecommendedContent,null=True,blank=True)
    subject = models.CharField(max_length =200)
    chapter = models.FloatField(blank=True,null=True)
    concept_number = models.IntegerField(blank=True,null=True)


    def __str__(self):
        return str(self.subject) +' '+ str(self.chapter) 


class YoutubeExternalVideos(models.Model):
    title = models.CharField(max_length=200,blank=True,null=True)
    chapter = models.CharField(max_length=100,blank=True,null=True)
    subject = models.CharField(max_length=100,blank=True,null=True)
    link = models.URLField(max_length=500,blank=True,null=True)
    thumbnail = models.URLField(max_length=500,blank=True,null=True)
    
    def __str__(self):
        return str(self.title) + ' ' + str(self.subject)

