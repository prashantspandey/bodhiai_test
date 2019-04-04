from django.db import models
from basicinformation.models import *
from Recommendations.models import Concepts
from QuestionsAndPapers.models import *
from django.contrib.auth.models import User 
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Course(models.Model):
    course_name = models.CharField(max_length=100)


    def __str__(self):
        return self.course_name


class SubjectChapters(models.Model):
    subject = models.CharField(max_length = 200)
    name = models.CharField(max_length =200)
    code = models.FloatField()
    course = models.ManyToManyField(Course,null=True,blank=True)
    logo = models.URLField(max_length=500,null=True,blank=True)

    def __str__(self):
        return str(self.subject) + ' ' + str(self.name)



