from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from basicinformation.models import *
from QuestionsAndPapers.models import *
from learning.models import *

# Create your models here.
class PossibleContext(models.Model):
    context = models.CharField(max_length=200)
    requisite = models.CharField(max_length = 200,blank=True,null=True)
    next_context = models.CharField(max_length = 200,blank=True,null=True)
    family = models.CharField(max_length =200)
    family_importance = models.IntegerField(null=True,blank=True)


    def __str__(self):
        return self.context

class ChatHistory(models.Model):
    student = models.ForeignKey(Student,null=True,blank=True)
    dates = ArrayField(models.DateTimeField())
    messages = ArrayField(models.TextField())
    contexts = ArrayField(models.CharField(max_length=200))
    types = ArrayField(models.CharField(max_length=200))
    nextPosition = ArrayField(models.CharField(max_length=200),default=['None'])
    repeat = ArrayField(models.BooleanField(default=False),default=[False])


    def __str__(self):
        return str(self.student.name) + ' ' + str(self.contexts)

class ContextDetail(models.Model):
    context = models.ForeignKey(PossibleContext)
    message = models.TextField()
    messageHindi = models.TextField(null=True,blank=True)
    how = models.TextField(max_length=300)
    position = models.CharField(max_length =50,blank=True,null=True)


    def __str__(self):
        return str(self.context) + ' ' + self.message[:20]


class StudyPlan(models.Model):
    student = models.OneToOneField(Student,null=True,blank=True)
    course_length = models.IntegerField(blank=True,null=True)
    course = models.CharField(max_length=50,blank=True,null=True)
    chapters = models.ManyToManyField(SubjectChapters)
    start = models.DateTimeField(blank=True,null=True)
    subjects = ArrayField(models.CharField(max_length=200),blank=True,null=True)
    current_subject = models.CharField(max_length = 50,blank=True,null=True)
    current_chapter_name = models.CharField(max_length = 50,blank=True,null=True)
    current_chapter_code = models.FloatField(blank=True,null=True)


    def __str__(self):
        return str(self.student) + ' ' + self.course + ' ' +\
    str(self.course_length)

class ChapterPlan(models.Model):
    studyPlan = models.ForeignKey(StudyPlan,null=True,blank=True)
    chapter = models.ForeignKey(SubjectChapters)
    overall_sovle = models.IntegerField(blank=True,null=True)
    solved = models.IntegerField(blank=True,null=True)
    to_solve = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return str(self.chapter) + ' ' + str(self.to_solve)

class LatestChatData(models.Model):
    student = models.OneToOneField(Student,null=True,blank=True)
    data = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return str(self.student) + ' ' + self.data

