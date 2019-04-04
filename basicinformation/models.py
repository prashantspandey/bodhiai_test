from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import ArrayField

class School(models.Model):
    category_choices = (('School','School'),('SSC','SSC')) 
    name = models.CharField(max_length=200)
    pincode = models.IntegerField()
    category = models.CharField(max_length = 10, choices =
                                category_choices,null=True,blank=True)
    logo = models.URLField(max_length = 500,null=True,blank=True)
    
    def __str__(self):
        return self.name


class klass(models.Model):
    level_choices =\
    (('9','Ninth'),('10','Tenth'),('11','Eleventh'),('12','Twelveth'),('SSC','SSC'))
    school = models.ForeignKey(School)
    name = models.CharField(max_length=50)
    level = models.CharField(max_length=10, choices =
                             level_choices,null=True,blank=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    studentuser = models.OneToOneField(User,blank=True,null=True)
    klass = models.ForeignKey(klass,related_name='klass')
    rollNumber = models.BigIntegerField(null=True,blank=True)
    name = models.CharField(max_length=200)
    dob = models.DateField(null=True,blank=True)
    pincode = models.IntegerField(null=True,blank=True)
    school = \
    models.ForeignKey(School,related_name='school',blank=True,null=True)
    def __str__(self):
        return self.name

class Teacher(models.Model):
    teacheruser = models.OneToOneField(User,blank=True,null=True)
    name = models.CharField(max_length=200)
    experience = models.FloatField()
    school = models.ForeignKey(School,blank=True,null=True)
    subBatch = models.CharField(max_length=5,null=True,blank=True)
    

    def __str__(self):
        return self.name


class Subject(models.Model):
    student = models.ForeignKey(Student)
    teacher = models.ForeignKey(Teacher,blank=True,null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return \
    '{}---{}----{}----{}'.format(self.name,self.student,self.teacher,self.student.school)

class StudentCustomProfile(models.Model):
    kl_choices =\
    (('10','Tenth'),('11','Eleventh'),('12','Twelveth'))
    student = models.OneToOneField(User,null=True,blank=True)
    address = models.CharField(max_length = 400,null=True,blank=True)
    phone = models.BigIntegerField(null=True, blank=True,
                            validators=[MaxValueValidator(9999999999),MinValueValidator(1000000000)])
    kl = models.CharField(max_length = 10,choices =\
                          kl_choices,null=True,blank=True)
    fatherName = models.CharField(max_length = 200,null=True,blank=True)
    fullName = models.CharField(max_length = 200,null=True,blank=True)
     
    def __str__(self):
        return str(self.fullName)+' ' + str(self.fatherName)


class StudentDetails(models.Model):
    student = models.OneToOneField(User)
    photo = models.URLField(max_length = 500,null=True,blank=True)
    fullName = models.CharField(max_length = 100,null=True,blank=True)
    address = models.CharField(max_length = 400,null=True,blank=True)
    phone = models.BigIntegerField(null=True, blank=True,
                            validators=[MaxValueValidator(9999999999),MinValueValidator(1000000000)])
    fatherName = models.CharField(max_length = 200,null=True,blank=True)
    parentPhone = models.BigIntegerField(null=True, blank=True,
                            validators=[MaxValueValidator(9999999999),MinValueValidator(1000000000)])
    email = models.EmailField(max_length = 70, blank = True)
    language = models.CharField(max_length=100,null=True,blank=True)
    course= models.CharField(max_length=100,null=True,blank=True)
    username= models.CharField(max_length=150,null=True,blank=True)



    def __str__(self):
        return str(self.student) + '' + str(self.phone)

   
class StudentConfirmation(models.Model):
    name = models.CharField(max_length = 200)
    student = models.OneToOneField(User,null=True,blank=True)
    teacher = models.ForeignKey(Teacher,null=True,blank=True)
    batch = models.ForeignKey(klass,null=True,blank=True)
    school = models.ForeignKey(School)
    phone = models.BigIntegerField(null=True, blank=True,
                            validators=[MaxValueValidator(9999999999),MinValueValidator(1000000000)])
    confirm = models.NullBooleanField()

    def __str__(self):
        return str(self.student) + str(self.school.name) 



class StudentProfile(models.Model):
    student = models.OneToOneField(User,null=True,blank=True)
    phone = models.BigIntegerField(null=True, blank=True,
                            validators=[MaxValueValidator(9999999999),MinValueValidator(1000000000)])
    school = models.ForeignKey(School,null=True,blank=True)
    batch = models.ForeignKey(klass,null=True,blank=True)
    code = models.CharField(max_length = 100)

     
    def __str__(self):
        return str(self.student.first_name)


class SchoolManagement(models.Model):
    management = models.OneToOneField(User)
    school = models.ForeignKey(School)

    def __str__(self):
        return 'management of {}'.format(self.school.name)

class InterestedPeople(models.Model):
    number = models.BigIntegerField()
    time = models.DateTimeField()

    def __str__(self):
        return str(self.number)+str(self.time)


class TeacherClasses(models.Model):
    teacher = models.ForeignKey(Teacher)
    klass = models.CharField(max_length=50)
    numStudents = models.IntegerField()

    def __str__(self):
        return str(self.teacher)+str(self.klass)


class AndroidAppVersion(models.Model):
    package_name = models.CharField(max_length=200)
    version_code = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.package_name) + ' ' + str(self.version_code)


class StudentTestTakenSubjectsCache(models.Model):
    student = models.ForeignKey(Student)
    subjects = ArrayField(models.CharField(max_length=200))


    def __str__(self):
        return str(self.student) 

class CustomBatch(models.Model):
    klass = models.ForeignKey(klass)
    subjects = ArrayField(models.CharField(max_length=200))
    school = models.ForeignKey(School)
    teacher = models.ManyToManyField(Teacher,blank=True)

    def __str__(self):
        return str(self.school) + ' ' + str(self.subjects)

class PrefferredLanguage(models.Model):
    student = models.ForeignKey(Student)
    language = models.CharField(max_length = 100)

    def __str__(self):
        return str(self.student) + ' ' + str(self.language)

class StudentTakenSubjectsCache(models.Model):
    student = models.ForeignKey(Student)
    subjects = ArrayField(models.CharField(max_length=200))
    
    def __str__(self):
        return str(self.student) + ' ' + str(self.subjects)

class StudentTapTracker(models.Model):
    student = models.ForeignKey(Student,blank=True,null=True)
    accuractyData = ArrayField(models.CharField(max_length=400),blank=True,null=True)
    averageTimeData = ArrayField(models.CharField(max_length=400),blank=True,null=True)
    performancdData = ArrayField(models.CharField(max_length=400),blank=True,null=True)
    progressData = ArrayField(models.CharField(max_length=400),blank=True,null=True)
    testData = ArrayField(models.CharField(max_length=400),blank=True,null=True)
    learnData = ArrayField(models.CharField(max_length=400),blank=True,null=True)
    date = models.DateField(blank=True,null=True)

    def __str__(self):
        return str(self.student)+' ' + str(self.events)+ ' ' + str(self.date)

class StudentLanguage(models.Model):
    student = models.ForeignKey(Student,blank=True,null=True)
    language = models.CharField(max_length=30)

    def __str__(self):
        return str(self.student) + ' ' + self.language

class StudentCourse(models.Model):
    course_choices = (('IITJEE','IITJEE'),('SSC','SSC'),("NEET","NEET"))
    student = models.ForeignKey(Student,blank=True,null=True)
    course = models.CharField(max_length = 30, choices =
                                course_choices,null=True,blank=True)

    def __str__(self):
        return str(self.student) + ' ' + self.course

class SubjectLogo(models.Model):
    name = models.CharField(max_length = 100,null=True,blank=True)
    logo = models.URLField(max_length = 500,null=True,blank=True)
    logo2 = models.URLField(max_length = 500,null=True,blank=True)

    def __str__(self):
        return self.name 

#class StudentSubjectWiseAccuracyCache(models.Model):
#    student = models.ForeignKey(Student,null=True,blank=True)
#    subject = models.CharField(max_length=100,null=True,blank=True)
#    numberRightAnswers = models.IntegerField(null=True,blank=True)
#    numberTotalAttempted = models.IntegerField(null=True,blank=True)
#    numberTests = models.IntegerField(null=True,blank=True)
#    accuracy = models.FloatField(null=True,blank=True)
#
#    def __str__(self):
#        return str(self.student) + ' ' + self.subject


class SubjectAccuracyStudent(models.Model):
    student = models.ForeignKey(Student,null=True,blank=True)
    subject = models.CharField(max_length=100,null=True,blank=True)
    rightAnswers = models.IntegerField(null=True,blank=True)
    totalAttempted = models.IntegerField(null=True,blank=True)
    testNumbers = models.IntegerField(null=True,blank=True)
    accuracy = models.FloatField(null=True,blank=True)

    def __str__(self):
        return str(self.student) + ' ' + self.subject


class ChapterAccuracyStudent(models.Model):
    student = models.ForeignKey(Student,null=True,blank=True)
    subject = models.CharField(max_length=100,null=True,blank=True)
    chapterCode = models.FloatField(blank=True,null=True)
    chapterName = models.CharField(max_length=200,blank=True,null=True)
    rightAnswers = models.IntegerField(null=True,blank=True)
    totalAttempted = models.IntegerField(null=True,blank=True)
    testNumbers = models.IntegerField(null=True,blank=True)
    accuracy = models.FloatField(null=True,blank=True)

    def __str__(self):
        return str(self.student) + ' ' + self.subject + ' ' + self.chapterName


class GroupBadge(models.Model):
    logo = models.URLField(max_length = 500,null=True,blank=True)
    group = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return str(self.group)

class StudentExpoToken(models.Model):
    student = models.ForeignKey(Student,null=True,blank=True)
    token = models.CharField(max_length=500,null=True,blank=True)

    def __str__(self):
        return self.token + ' ' + self.student.name

class StudentSubjectAim(models.Model):
    student = models.ForeignKey(Student,null=True,blank=True)
    subject = models.CharField(max_length=200)
    aim = models.IntegerField()

    def __str__(self):
        return self.subject + ' ' + str(self.aim)

class NextExamDate(models.Model):
    course = models.CharField(max_length =50)
    examDate = models.DateTimeField()


    def __str__(self):
        return self.course + ' ' + str(self.examDate)


class AWSKey(models.Model):
    accessKey = models.CharField(max_length=500)
    secretKey = models.CharField(max_length=500)


    def __str__(self):
        return self.accessKey


class StudentChallenge(models.Model):
    studentOne = models.ForeignKey(Student,related_name='studentone',null=True,blank=True)
    studentTwo = models.ForeignKey(Student,related_name='studenttwo',null=True,blank=True)
    when = models.DateTimeField()


    def __str__(self):
        return str(self.studentOne) + ' ' + str(self.studentTwo)


class PromoInstitute(models.Model):
    name = models.CharField(max_length=50)
    logo = models.URLField(max_length = 500,null=True,blank=True)
    phone = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class PromoCode(models.Model):
    code = models.CharField(max_length=10,null=True,blank=True)
    date = models.DateTimeField(null=True,blank=True)
    phone = models.CharField(max_length=10,null=True,blank=True)
    student = models.ForeignKey(Student,null=True,blank=True)
    institute = models.ForeignKey(PromoInstitute,null=True,blank=True)

    def __str__(self):
        return self.code + ' ' + str(self.student.name)


class PotentialUserData(models.Model):
    ipAddress = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=100,blank=True,null=True)
    region = models.CharField(max_length=100,blank=True,null=True)
    country = models.CharField(max_length=100,blank=True,null=True)
    loc = models.CharField(max_length=100,blank=True,null=True)
    postal = models.CharField(max_length=100,blank=True,null=True)
    org = models.CharField(max_length=100,blank=True,null=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ipAddress

class CourseLength(models.Model):
    student = models.ForeignKey(Student)
    course = models.CharField(max_length=100,null=True,blank=True)
    length = models.CharField(max_length=10,null=True,blank=True)

    def __str__(self):
        return str(self.student) + ' ' + self.course
