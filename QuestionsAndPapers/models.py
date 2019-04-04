from django.db import models
from basicinformation.models import *
from Recommendations.models import Concepts
from django.contrib.auth.models import User 
from django.contrib.postgres.fields import ArrayField



# Create your models here.  
class KlassTest(models.Model): 
    mode_choices =\
    (('BodhiOnline','BodhiOnline'),('BodhiSchool','BodhiSchool')) 
    name = models.CharField(max_length=100)
    subject_choices = (('Maths','Maths'),('Science','Science'),('English','English')) 
    max_marks = models.PositiveIntegerField() 
    testTakers = models.ManyToManyField(Student)
    published = models.DateField(auto_now_add= True)
    klas = models.ForeignKey(klass,null=True,blank=True) 
    creator = models.ForeignKey(User,null=True,blank=True)
    sub = models.CharField(max_length=70,choices = subject_choices)
    due_date = models.DateField(null=True,blank=True)
    mode = models.CharField(max_length=20,choices = mode_choices)
    totalTime = models.IntegerField(blank=True,null=True)
    def __str__(self):
        return self.name


class SSCKlassTest(models.Model):
    mode_choices =\
    (('BodhiOnline','BodhiOnline'),('BodhiSchool','BodhiSchool'))
    name = models.CharField(max_length=100)
    subject_choices = \
        (('General-Intelligence','General-Intelligence'),('General-Knowledge','General-Knowledge')
         ,('Quantitative-Analysis','Quantitative-Analysis'),('English','English')
         ,('Defence-English','Defence-English'),('Defence-Physics','Defence-Physics')
         ,('GroupX-Maths','GroupX-Maths'),('Defence-GK-CA','Defence-GK-CA'),
        ('SSCMultipleSections','SSCMultipleSections'),('Defence-MultipleSubjects','Defence-MultipleSubjects')
         ,('IITJEE10-MultipleSubjects','IITJEE10-MultipleSubjects'),('IITJEE11-MultipleSubjects','IITJEE11-MultipleSubjects')
         ,('IITJEE12-MultipleSubjects','IITJEE12-MultipleSubjects'),('MathsIITJEE10','MathsIITJEE10')
         ,('MathsIITJEE11','MathsIITJEE11'),('MathsIITJEE12','MathsIITJEE12')
         ,('ChemistryIITJEE10','ChemistryIITJEE10'),('ChemistryIITJEE11','ChemistryIITJEE11')
         ,('ChemistryIITJEE12','ChemistryIITJEE12'),('PhysicsIITJEE10','PhysicsIITJEE10')
         ,('PhysicsIITJEE11','PhysicsIITJEE11'),('PhysicsIITJEE12','PhysicsIITJEE12')
         ,('ElectricalLocoPilot','ElectricalLocoPilot'),('FitterLocoPilot','FitterLocoPilot')
         ,('General-Science','General-Science'),('LocoPilot_Diesel','LocoPilot_Diesel'),
        ('CAT_Quantitative_Aptitude','CAT_Quantitative_Aptitude'),('Civil_Loco_Pilot_Tech','Civil_Loco_Pilot_Tech'),
        ('SSC_Electronics1','SSC_Electronics1'),('Basic-Science','Basic-Science'),('Environment-Study','Environment-Study'),('Engineering-Drawing','Engineering-Drawing'),
        ('Physics_NEET','Physics_NEET'),('Chemistry_NEET','Chemistry_NEET'),('Botony_NEET','Botony_NEET'),('Physics_IIT','Physics_IIT'),('Maths_IIT','Maths_IIT'),
        ('Chemistry_IIT','Chemistry_IIT'),('Biology_NEET','Biology_NEET'))
    course_choices = (('SSC','SSC'),('Railways','Railways'))

    #max_marks = models.DecimalField(max_digits=4,decimal_places=2)
    max_marks = models.IntegerField()
    testTakers = models.ManyToManyField(Student)
    published = models.DateField(auto_now_add= True)
    klas = models.ForeignKey(klass,null=True,blank=True)
    patternTestBatches = models.ManyToManyField(klass,related_name =
                                                'patternBatches',null=True,blank=True)
    patternTestCreators = models.ManyToManyField(Teacher)
    creator = models.ForeignKey(User,null=True,blank=True)
    sub = models.CharField(max_length=70,choices = subject_choices)
    due_date = models.DateField(null=True,blank=True)
    mode = models.CharField(max_length=20,choices = mode_choices)
    totalTime = models.IntegerField(blank=True,null=True)
    course =\
    models.CharField(max_length=20,choices=course_choices,default='SSC')
    pattern_test = models.BooleanField(default=False)
    mock_test = models.NullBooleanField(default=False)
    typeTest = models.CharField(max_length=20,null=True,blank=True)
    def __str__(self):
        return self.name

class TestDetails(models.Model):
    test = models.ForeignKey(SSCKlassTest)
    num_questions = models.IntegerField()
    questions = ArrayField(models.IntegerField())

    def __str__(self):
        return str(self.test.id) + str(self.num_questions)

class Comprehension(models.Model):
    text = models.TextField()
    picture = models.URLField(max_length=500,null=True,blank=True)

    def __str__(self):
        return self.text[:100] + self.picture




class Questions(models.Model):
    ch = 1 
    tp = 1 
    topic_choice = []
    topic_choice2 = []
    for ch in range(1,20):
        for tp in range(1,20):
            topic_choice.append(str(ch)+'.'+str(tp))
            topic_choice2.append(str(ch)+'.'+str(tp))
    tp_choice = list(zip(topic_choice,topic_choice2))
    topic_choice = tuple(tp_choice)
    level_choices = (('9','Ninth'),('10','Tenth'),('11','Eleventh'),('12','Twelveth'))
    ktest = models.ManyToManyField(KlassTest,blank= True)
    chapter_choices = (('1','Chapter 1'),('2','Chapter 2'),('3','Chapter 3'))
    subject_choices = \
        (('Maths','Maths'),('Science','Science'),('English','English'))
    text = models.TextField()
    level = models.CharField(max_length=20,choices = level_choices)
    max_marks = models.IntegerField()
    sub  = models.CharField(max_length=70,choices = subject_choices)
    chapCategory = models.CharField(max_length=30,choices=chapter_choices)
    topic_category = models.CharField(max_length=10,choices = topic_choice)
    school = models.ManyToManyField(School)
    picture = models.URLField(null=True,blank=True)
    source = models.CharField(max_length= 50,null=True,blank=True)
    dateInserted = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return self.text[:50]



class SSCquestions(models.Model):
    ch = 1 
    tp = 1 
    topic_choice = []
    topic_choice2 = []
    for ch in range(1,70):
        for tp in range(1,10):
            topic_choice.append(str(ch)+'.'+str(tp))
            topic_choice2.append(str(ch)+'.'+str(tp))
    tp_choice = list(zip(topic_choice,topic_choice2))
    topic_choice = tuple(tp_choice)
    comprehension = models.ForeignKey(Comprehension,blank=True,null=True)
    ktest = models.ManyToManyField(SSCKlassTest,blank= True)
    max_marks = models.IntegerField(default= 2)
    negative_marks =\
    models.DecimalField(max_digits=2,decimal_places=2,default=0.25)
    tier_choices = (('1','Tier1'),('2','Tier2'),('3','Tier3'))
    usedFor_choices =\
    (('SSC','SSC'),('Aptitude','Aptitude'),('Groupx','Groupx'),('Groupy','Groupy'),('RPSC','RPSC'),('RAS','RAS'),('IITJEE','IITJEE'))
    language_choices = (('English','English'),('Hindi','Hindi'),('Bi','Bi'))
    section_choices = \
        (('General-Intelligence','General-Intelligence'),('General-Knowledge','General-Knowledge')
         ,('Quantitative-Analysis','Quantitative-Analysis'),('English','English')
         ,('Defence-English','Defence-English'),('Defence-Physics','Defence-Physics')
         ,('GroupX-Maths','GroupX-Maths'),('Defence-GK-CA','Defence-GK-CA')
         ,('MathsIITJEE10','MathsIITJEE10'),('MathsIITJEE11','MathsIITJEE11')
         ,('MathsIITJEE12','MathsIITJEE12'),('ChemistryIITJEE10','ChemistryIITJEE10')
         ,('ChemistryIITJEE11','ChemistryIITJEE11'),('ChemistryIITJEE12','ChemistryIITJEE12')
         ,('PhysicsIITJEE10','PhysicsIITJEE10'),('PhysicsIITJEE11','PhysicsIITJEE11')
         ,('PhysicsIITJEE12','PhysicsIITJEE12'),('Design and analysis of algorithm','Design and analysis of algorithm')
         ,('ElectricalLocoPilot','ElectricalLocoPilot'),('FitterLocoPilot','FitterLocoPilot')
         ,('General-Science','General-Science'),('LocoPilot_Diesel','LocoPilot_Diesel'),
        ('CAT_Quantitative_Aptitude','CAT_Quantitative_Aptitude'),('Civil_Loco_Pilot_Tech','Civil_Loco_Pilot_Tech'),
        ('SSC_Electronics1','SSC_Electronics1'),('Basic-Science','Basic-Science'),('Environment-Study','Environment-Study'),('Engineering-Drawing','Engineering-Drawing'),
        ('Physics_NEET','Physics_NEET'),('Chemistry_NEET','Chemistry_NEET'),('Botony_NEET','Botony_NEET'),('Physics_IIT','Physics_IIT'),('Maths_IIT','Maths_IIT'),
        ('Chemistry_IIT','Chemistry_IIT'),('Biology_NEET','Biology_NEET'))
    diffculty_choices = (('easy','easy'),('medium','medium'),('hard','hard'))
    text = models.TextField(blank=True,null=True)
    tier_category = models.CharField(max_length=20,choices = tier_choices)
    section_category  = models.CharField(max_length=70,choices = section_choices)
    diffculty_category = models.CharField(max_length = 10,choices =
                                          diffculty_choices,null=True,blank=True)
    topic_category = models.CharField(max_length=5,choices = topic_choice)
    school = models.ManyToManyField(School)
    picture = models.URLField(max_length=500,null=True,blank=True)
    usedFor = models.CharField(max_length=30,null=True,blank=True)
    source = models.CharField(max_length= 50,null=True,blank=True)
    dateInserted = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    language = models.CharField(max_length = 20,null=True,blank=True )
    concepts = models.ManyToManyField(Concepts)

    def __str__(self):
        return str(self.id)

class GeneralDifficulty(models.Model):
    average_difficulty = models.FloatField()
    skipped_ratio = models.FloatField()
    quest = models.ForeignKey(SSCquestions)

    def __str__(self):
        return str(self.average_difficulty)



class InstituteQuestionDifficulty(models.Model):
    average_difficulty = models.FloatField()
    skipped_ratio = models.FloatField()
    institute = models.ForeignKey(School)
    quest = models.ForeignKey(SSCquestions)

    def __str__(self):
        return str(self.institute)+','+str(self.average_difficulty)


class TimesUsed(models.Model):
    numUsed = models.IntegerField()
    teacher = models.ForeignKey(Teacher)
    quest = models.ForeignKey(SSCquestions)
    batch = models.ForeignKey(klass,null=True,blank=True)

    def __str__(self):
        name = str(self.batch) + str(self.teacher.name) + str(self.numUsed)
        return name

class TimesReported(models.Model):
    isReported = models.BooleanField()
    teacher = models.ForeignKey(Teacher)
    quest = models.ForeignKey(SSCquestions)

    def __str__(self):
        name = str(self.quest)+ str(self.teacher.name) + str(self.numReported)
        return name


class Choices(models.Model):
    class Meta:
        ordering = ['pk']
    res_choice = (('Correct','Correct'),('Wrong','Wrong'),('Not decided','Not decided'))
    predicament = models.CharField(max_length= 30, choices = res_choice)    
    quest = models.ForeignKey(Questions,blank=True,null=True)
    sscquest = models.ForeignKey(SSCquestions,blank=True,null=True)
    text = models.TextField(blank=True,null=True)
    picture = models.URLField(null=True,blank=True)
    explanation = models.TextField(null=True,blank=True)
    explanationPicture= models.URLField(null=True,blank=True)
    def __str__(self):
        if self.text != None:
            return self.text[:50]
        else:
            return self.picture

class OnlineMarks(models.Model):
    test = models.ForeignKey(KlassTest)
    student = models.ForeignKey(Student)
    rightAnswers = ArrayField(models.IntegerField(null=True,blank=True))
    wrongAnswers = ArrayField(models.IntegerField(null=True,blank=True))
    allAnswers = ArrayField(models.IntegerField(null=True,blank=True))
    skippedAnswers = ArrayField(models.IntegerField(null=True,blank=True))
    marks = models.IntegerField()
    testTaken = models.DateField()
    timeTaken = models.IntegerField()
    def __str__(self):
        return str(self.marks)
    
class SSCOnlineMarks(models.Model):
    test = models.ForeignKey(SSCKlassTest)
    student = models.ForeignKey(Student)
    rightAnswers = ArrayField(models.IntegerField(null=True,blank=True))
    wrongAnswers = ArrayField(models.IntegerField(null=True,blank=True))
    allAnswers = ArrayField(models.IntegerField(null=True,blank=True))
    skippedAnswers = ArrayField(models.IntegerField(null=True,blank=True))
    marks = models.DecimalField(max_digits=4,decimal_places=2)
    testTaken = models.DateField()
    testTakenTime = models.DateTimeField(blank=True,null=True)
    timeTaken = models.IntegerField()
    def __str__(self):
        return str(self.marks)

class SSCOfflineMarks(models.Model):
    test = models.ForeignKey(SSCKlassTest)
    student = models.ForeignKey(Student)
    rightAnswers = ArrayField(models.IntegerField(null=True,blank=True))
    wrongAnswers = ArrayField(models.IntegerField(null=True,blank=True))
    allAnswers = ArrayField(models.IntegerField(null=True,blank=True))
    skippedAnswers = ArrayField(models.IntegerField(null=True,blank=True))
    marks = models.DecimalField(max_digits=4,decimal_places=2)
    testTaken = models.DateField()
    def __str__(self):
        return str(self.marks)




class TemporaryAnswerHolder(models.Model):
    stud = models.ForeignKey(Student,null=True,blank=True)
    test = models.ForeignKey(SSCKlassTest)
    quests = models.CharField(max_length=10)
    answers = models.CharField(max_length=10)
    time = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return str(self.stud)

class SSCansweredQuestion(models.Model):
    onlineMarks = models.ForeignKey(SSCOnlineMarks)
    quest = models.ForeignKey(SSCquestions)
    time = models.IntegerField()


class AnsweredQuestion(models.Model):
    onlineMarks = models.ForeignKey(OnlineMarks)
    quest = models.ForeignKey(Questions)
    time = models.IntegerField()

class SSCTemporaryQuestionsHolder(models.Model):
    quests = ArrayField(models.IntegerField())
    teacher = models.ForeignKey(Teacher)
    time = models.DateTimeField()


class TemporaryQuestionsHolder(models.Model):
    quests = ArrayField(models.IntegerField())
    teacher = models.ForeignKey(Teacher)


class TemporaryOneClickTestHolder(models.Model):
    quests = ArrayField(models.IntegerField())
    teacher = models.ForeignKey(Teacher)

class SscTeacherTestResultLoader(models.Model):
    test = models.ForeignKey(SSCKlassTest)
    teacher = models.ForeignKey(Teacher)
    onlineMarks = models.ManyToManyField(SSCOnlineMarks)
    average = models.FloatField()
    percentAverage = models.FloatField()
    grade_a = models.IntegerField(default = 0)
    grade_b = models.IntegerField(default = 0)
    grade_c = models.IntegerField(default = 0)
    grade_d = models.IntegerField(default = 0)
    grade_e = models.IntegerField(default = 0)
    grade_f = models.IntegerField(default = 0)
    grade_s = models.IntegerField(default = 0)
    skipped  = ArrayField(models.IntegerField())
    skippedFreq = ArrayField(models.IntegerField())
    problemQuestions = ArrayField(models.IntegerField())
    problemQuestionsFreq = ArrayField(models.IntegerField())
    freqAnswersQuestions = ArrayField(models.IntegerField())
    freqAnswersFreq = ArrayField(models.IntegerField())


    def __str__(self):
        return str(self.test.id)

class SscStudentWeakAreaLoader(models.Model):
    subject_choices = \
        (('General-Intelligence','General-Intelligence'),('General-Knowledge','General-Knowledge')
         ,('Quantitative-Analysis','Quantitative-Analysis'),('English','English'),
        ('SSCMultipleSections','SSCMultipleSections'))

    student = models.ForeignKey(Student)
    subject = models.CharField(max_length = 70,choices = subject_choices)
    lenonlineSingleSub = models.IntegerField(null=True)
    lenonlineMultipleSub = models.IntegerField(null=True)
    lenofflineSingleSub = models.IntegerField(null=True)
    lenofflineMultipleSub = models.IntegerField(null=True)
    topics = ArrayField(models.FloatField())
    weakTopicsPercentage = ArrayField(models.FloatField())
    timingTopics = ArrayField(models.FloatField())
    weakTiming = ArrayField(models.FloatField())
    weakTimingFreq = ArrayField(models.IntegerField())


    def __str__(self):
        return str(self.student) + str(self.weakTopics)

class StudentCurrentTest(models.Model):
    student = models.ForeignKey(Student)
    test = models.ForeignKey(SSCKlassTest)
    time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.student) + str(self.test.id)

class TestRankTable(models.Model):
    teacher = models.ForeignKey(Teacher,null=True)
    test = models.ForeignKey(SSCKlassTest,null=True)
    names = ArrayField(models.CharField(max_length=100))
    totalMarks = ArrayField(models.IntegerField(null=True))
    scores = ArrayField(models.FloatField(null=True))
    percentage = ArrayField(models.FloatField(null=True))
    numCorrect = ArrayField(models.IntegerField(null=True))
    numIncorrect = ArrayField(models.IntegerField(null=True))
    numSkipped = ArrayField(models.IntegerField(null=True))
    rank = ArrayField(models.IntegerField(null=True,blank = True))
    time = models.DateTimeField(auto_now = True,null=True)

    def __str__(self):
        return str(self.teacher)+str(self.test.published)

class StudentSmartTestTopics(models.Model):
    student = models.ForeignKey(Student)
    topics = ArrayField(models.CharField(max_length=100))
    weakness = ArrayField(models.IntegerField(null=True))
    test = models.OneToOneField(SSCKlassTest)

    def __str__(self):
        return str(self.student) + " "+ str(self.topics) + " " +\
    str(self.weakness)

class TeacherBatchWeakAreas(models.Model):
    teacher = models.ForeignKey(Teacher,null=True)
    batch = models.CharField(max_length=20,null=True)
    subject = models.CharField(max_length = 100,null=True)
    weak_sections = ArrayField(models.CharField(max_length=100))
    date = models.DateField(auto_now_add= True,null=True)

    def __str__(self):
        return str(self.batch)+" " + str(self.subject)


class TeacherWeakAreasDetailCache(models.Model):
    date = models.DateField(auto_now_add= True,null=True)
    subject = models.CharField(max_length = 100,null=True)
    klass = models.CharField(max_length = 100,null=True)
    teacher = models.ForeignKey(Teacher,null=True)
    categories =  ArrayField(models.CharField(max_length=100))
    accuracies = ArrayField(models.FloatField())
    wrong_total = ArrayField(models.IntegerField())
    total_total = ArrayField(models.IntegerField())
    subjectTests = models.IntegerField(null=True)
    defenceTests = models.IntegerField(null=True)
    testids = ArrayField(models.IntegerField())

    def __str__(self):
        return str(self.date)+ " " + str(self.teacher)

class TeacherWeakAreasTimingCache(models.Model):
    date = models.DateField(auto_now_add= True,null=True)
    subject = models.CharField(max_length = 100,null=True)
    klass = models.CharField(max_length = 100,null=True)
    teacher = models.ForeignKey(Teacher,null=True)
    categories = ArrayField(models.CharField(max_length=100))
    averagetiming = ArrayField(models.FloatField(),null=True)
    totalTiming = ArrayField(models.FloatField(),null=True)
    totalFreq = ArrayField(models.FloatField(null=True),null=True)
    testids = ArrayField(models.IntegerField(),null=True)
    def __str__(self):
        return str(self.date)+ " " + str(self.teacher)

class StudentTestAnalysis(models.Model):
    date = models.DateField(auto_now_add= True,null=True)
    student = models.ForeignKey(Student)
    test = models.ForeignKey(SSCKlassTest)
    myPercent = models.FloatField()
    klassAverage = models.FloatField()
    klassAveragePercent = models.FloatField()
    myPercentile = models.FloatField()
    allKlassMarks = ArrayField(models.FloatField(),null=True)
    freqAnswerId = ArrayField(models.IntegerField(),null=True)
    freqAnswer = ArrayField(models.IntegerField(),null=True)
    weakCategories = ArrayField(models.CharField(max_length=100),null=True)
    weakAccuracies = ArrayField(models.FloatField(),null=True)
    numRight = models.IntegerField()
    numWrong =models.IntegerField()
    numSkipped = models.IntegerField()
    overallAccuracy = models.FloatField()
    subjectwiseAccuracySub =ArrayField(models.CharField(max_length = 50),null=True)
    subjectwiseAccuracy =ArrayField(models.FloatField(max_length = 50),null=True)
    areaTimeCategory = ArrayField(models.CharField(max_length=100),null=True)
    areaTime = ArrayField(models.FloatField(),null=True)
    hour = models.IntegerField()
    minute = models.IntegerField()
    second = models.IntegerField()
    


    def __str__(self):
        return str(self.student) + str(self.myPercent)


class StudentWeakAreasCache(models.Model):
    date = models.DateField(auto_now_add= True,null=True)
    student = models.ForeignKey(Student)
    accuracies =ArrayField(models.FloatField(max_length = 50),null=True)
    categories =ArrayField(models.FloatField(max_length = 50),null=True)
    subject = models.CharField(max_length = 100)
    allTests =ArrayField(models.IntegerField(),null=True)
    numTests = models.IntegerField()

    def __str__(self):
        return str(self.student) + str(self.subject)
    
class TimeTable(models.Model):
    created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    date = models.DateField(null=True,blank=True)
    timeStart = models.CharField(max_length=100,null=True,blank=True)
    timeEnd = models.CharField(max_length=100,null=True,blank=True)
    teacher = models.ForeignKey(Teacher,null=True,blank=True)
    batch = models.ForeignKey(klass)
    sub = models.CharField(max_length =100,null=True,blank=True)
    note = models.TextField(null=True,blank=True)
    management = models.ForeignKey(SchoolManagement,null=True,blank=True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return str(self.teacher) + str(self.batch) + str(self.date) +\
    str(self.time)

class StudentAverageTimingDetailCache(models.Model):
    student = models.ForeignKey(Student)
    subject = models.CharField(max_length=100)
    chapter = models.CharField(max_length=100)
    totalAttempted = models.IntegerField()
    rightAverage = models.FloatField()
    wrongAverage = models.FloatField()
    rightTotal = models.IntegerField()
    wrongTotal = models.IntegerField()
    rightTotalTime = models.FloatField()
    wrongTotalTime = models.FloatField()
    totalAverage = models.FloatField()
    allMarksIds = ArrayField(models.IntegerField(),null=True)

    def __str__(self):
        return str(self.student) + " " + str(self.subject) + " " +\
    str(self.chapter)

class StudentWeakAreasChapterCache(models.Model):
    student = models.ForeignKey(Student)
    subject = models.CharField(max_length=100)
    chapter = models.CharField(max_length=100)
    totalAttempted = models.IntegerField()
    accuracy = models.FloatField()
    totalRight = models.IntegerField()
    totalWrong = models.IntegerField()
    totalSkipped = models.IntegerField()
    skippedPercent = models.FloatField()
    def __str__(self):
        return str(self.student) + " " + str(self.subject) + " " +\
    str(self.chapter)


class StudentProgressChapterCache(models.Model):
    student = models.ForeignKey(Student)
    subject = models.CharField(max_length=100)
    chapter = models.CharField(max_length=100)
    marks = ArrayField(models.FloatField(),null=True)
    rightPercent = ArrayField(models.FloatField(),null=True)
    wrongPercent = ArrayField(models.FloatField(),null=True)
    rightTime = ArrayField(models.FloatField(),null=True)
    wrongTime = ArrayField(models.FloatField(),null=True)
    skippedPercent = ArrayField(models.FloatField(),null=True)
    dates = ArrayField(models.CharField(max_length = 25),null=True)
    totalRight = ArrayField(models.IntegerField(),null=True)
    totalWrong = ArrayField(models.IntegerField(),null=True)
    totalSkipped = ArrayField(models.IntegerField(),null=True)
    

    def __str__(self):
        return str(self.student) + ' ' + str(self.subject) + ' '+\
    str(self.marks)

class StudentChapterWiseActivity(models.Model):
    student = models.ForeignKey(Student)
    subject = models.CharField(max_length=100)
    chapter = models.CharField(max_length=100)
    numAttempted = ArrayField(models.IntegerField(),null=True)
    date = models.DateField()

    def __str__(self):
        return str(self.student) + ' ' + str(self.numAttempted) + ' ' +\
    str(self.date)
    
class JobList(models.Model):
    title = models.CharField(max_length = 500)
    body = models.TextField()
    date = models.CharField(max_length = 30)

    def __str__(self):
        return str(self.title) + ' '+ str(self.date)

class StudentBookMarkQuestion(models.Model):
    student = models.ForeignKey(Student,blank=True,null=True)
    question = models.ForeignKey(SSCquestions,blank=True,null=True)
    notes = models.TextField()

    def __str__(self):
        return str(self.student) + ' ' + str(self.question.id)

class TestRank(models.Model):
    test = models.ForeignKey(SSCKlassTest,blank=True,null=True)
    sortedMarks = ArrayField(models.FloatField(),blank=True,null=True)
    students = ArrayField(models.IntegerField(null=True),null=True,blank=True)


    def __str__(self):
        return str(self.sortedMarks)

class SubjectRank(models.Model):
    subject = models.CharField(max_length=100,blank=True,null=True)
    sortedAccuracies = ArrayField(models.FloatField(),blank=True,null=True)
    students = ArrayField(models.IntegerField(null=True),null=True,blank=True)
    minimumTests = models.IntegerField(null=True,blank=True)
    maximumTests = models.IntegerField(null=True,blank=True)


    def __str__(self):
        return str(self.sortedAccuracies)


class ChapterRank(models.Model):
    subject = models.CharField(max_length=100,blank=True,null=True)
    chapterCode = models.FloatField(null=True,blank=True)
    chapterName = models.CharField(max_length=200,null=True,blank=True)
    sortedAccuracies = ArrayField(models.FloatField(),blank=True,null=True)
    students = ArrayField(models.IntegerField(null=True),null=True,blank=True)
    minimumTests = models.IntegerField(null=True,blank=True)
    maximumTests = models.IntegerField(null=True,blank=True)


    def __str__(self):
        return str(self.chapterCode) + ' ' + str(self.sortedAccuracies)

class PatternTestPattern(models.Model):
    exam_name = models.CharField(max_length=100,null=True,blank=True)
    subjects = ArrayField(models.CharField(max_length=100),null=True,blank=True)
    numberQuestions = ArrayField(models.IntegerField(),null=True,blank=True)


    def __str__(self):
        return self.exam_name 

class TestRating(models.Model):
    test = models.ForeignKey(SSCKlassTest)
    student = models.ForeignKey(Student)
    rating = models.IntegerField()

    def __str__(self):
        return str(self.student) + ' '+ str(self.rating) + ' ' + str(self.test.id)

