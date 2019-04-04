import numpy as np
import pickle
import math
import itertools
import random
from datetime import datetime, date
from django.utils import timezone
from .models import Subject
from more_itertools import unique_everseen
from QuestionsAndPapers.models import *
from xhtml2pdf import pisa
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.db.models import Q
from django.db.models.signals import post_save
#'''
#load pickles for data transformation and prediction (hindi)
#'''
#pickle_in_hindi =  open('basicinformation/preprocesshindihy.pickle','rb')
#svm_pickle_hindi = open('basicinformation/svmhindihhy.pickle', 'rb')
#sca_hindi = pickle.load(pickle_in_hindi)
#svmhindihhy = pickle.load(svm_pickle_hindi)
#
#'''
#load pickles for data transformation and prediction (maths)
#'''
#pickle_in_maths = open('basicinformation/preprocesshindihy.pickle', 'rb')
#knn7_pickle_maths = open('basicinformation/svmhindihhy.pickle', 'rb')
#sca_maths = pickle.load(pickle_in_maths)
#knn7mathshhy = pickle.load(knn7_pickle_maths)
#
#'''
#load pickles for data transformation and prediction (english)
#'''
#pickle_in_english = open('basicinformation/preprocesshindihy.pickle', 'rb')
#knn7_pickle_english = open('basicinformation/svmhindihhy.pickle', 'rb')
#sca_english = pickle.load(pickle_in_english)
#knn7englishhhy = pickle.load(knn7_pickle_english)
#
#'''
#load pickles for data transformation and prediction (science)
#'''
#pickle_in_science = open('basicinformation/preprocesshindihy.pickle', 'rb')
#knn7_pickle_science = open('basicinformation/svmhindihhy.pickle', 'rb')
#sca_science = pickle.load(pickle_in_science)
#knn7sciencehhy = pickle.load(knn7_pickle_science)

# test1,test2,test3,age,section
# x = np.array([[9, 10, 10, 12, 1]])
# x = sca.transform(x)
# print(x)
# prd = svmhindihhy.predict(x)
# print(prd)


def hindi_3testhyprediction(test1, test2, test3, DOB, section):
    '''
    convert test marks into numpy arrays
    '''
    t1 = int(test1)
    t2 = int(test2)
    t3 = int(test3)

    if section == 'a':
        section = 1
    elif section == 'b':
        section = 2

    '''
    calculate age using DOB (dd/mm/year)
    '''
    days_in_year = 365.2425
    age = int((date(2018, 4, 1) - DOB).days / days_in_year)
    # age = int((date.today() - DOB).days / days_in_year)

    overall = np.array([[t1, t2, t3, age, section]])

    '''
        transform(scale) data to original data of school
    '''
    overall = sca_hindi.transform(overall)
    '''
        predict the hy marks using the trained ml algorithm
    '''
    prediction = svmhindihhy.predict(overall)
    return prediction


def maths_3testhyprediction(test1, test2, test3, DOB, section):
    '''
    convert test marks into numpy arrays
    '''
    t1 = int(test1)
    t2 = int(test2)
    t3 = int(test3)

    if section == 'a':
        section = 1
    elif section == 'b':
        section = 2

    '''
        calculate age using DOB (dd/mm/year)
    '''
    days_in_year = 365.2425
    age = int((date(2018, 4, 1) - DOB).days / days_in_year)

    overall = np.array([[t1, t2, t3, age, section]])

    '''
        transform(scale) data to original data of school
    '''
    overall = sca_maths.transform(overall)
    '''
        predict the hy marks using the trained ml algorithm
    '''
    prediction = knn7mathshhy.predict(overall)
    return prediction


def english_3testhyprediction(test1, test2, test3, DOB, section):
    '''
    convert test marks into numpy arrays
    '''
    t1 = int(test1)
    t2 = int(test2)
    t3 = int(test3)

    if section == 'a':
        section = 1
    elif section == 'b':
        section = 2

    '''
        calculate age using DOB (dd/mm/year)
    '''
    days_in_year = 365.2425
    age = int((date(2018, 4, 1) - DOB).days / days_in_year)

    overall = np.array([[t1, t2, t3, age, section]])

    '''
        transform(scale) data to original data of school
    '''
    overall = sca_english.transform(overall)
    '''
        predict the hy marks using the trained ml algorithm
    '''
    prediction = knn7englishhhy.predict(overall)
    return prediction


def science_3testhyprediction(test1, test2, test3, DOB, section):
    '''
    convert test marks into numpy arrays
    '''
    t1 = int(test1)
    t2 = int(test2)
    t3 = int(test3)

    if section == 'a':
        section = 1
    elif section == 'b':
        section = 2

        '''
            calculate age using DOB (dd/mm/year)
        '''
    days_in_year = 365.2425

    age = int((date(2018, 4, 1) - DOB).days / days_in_year)

    overall = np.array([[t1, t2, t3, age, section]])

    '''
        transform(scale) data to original data of school
    '''
    overall = sca_science.transform(overall)
    '''
        predict the hy marks using the trained ml algorithm
    '''
    prediction = knn7sciencehhy.predict(overall)
    return prediction


def predictionConvertion(prediction):
    try:
        prediction = prediction[0]
    except:
        pass

    if prediction == 0:
        conversion = 35
    elif prediction == 1:
        conversion = 45
    elif prediction == 2:
        conversion = 55
    elif prediction == 3:
        conversion = 65
    elif prediction == 4:
        conversion = 75
    elif prediction == 5:
        conversion = 85
    elif prediction == 6:
        conversion = 95
    else:
        conversion = '404'
    return conversion


# function for updating all the half yearly predictions (whole database)


def update_all_predictedmarks():
    subject = Subject.objects.all()
    alluniquestudents = []
    alluniquestudents = list(unique_everseen(alluniquestudents))
    for i in subject:
        alluniquestudents.append(i.student)
    allsubjects = []
    for j in alluniquestudents:
        allsubjects.extend(j.subject_set.all())

    for thisSubject in allsubjects:
        if thisSubject.name == 'Hindi':
            cl = str(thisSubject.student.klass)
            if cl[-1] == 'a':
                section = 'a'
            else:
                section = 'b'
            thisSubject.predicted_hy = int(
                hindi_3testhyprediction(thisSubject.test1, thisSubject.test2, thisSubject.test3,
                                        thisSubject.student.dob, section))

            thisSubject.save()
        elif thisSubject.name == 'English':
            cl = str(thisSubject.student.klass)
            if cl[-1] == 'a':
                section = 'a'
            else:
                section = 'b'
            thisSubject.predicted_hy = int(
                english_3testhyprediction(thisSubject.test1, thisSubject.test2, thisSubject.test3,
                                          thisSubject.student.dob, section))
            thisSubject.save()

        elif thisSubject.name == 'Maths':
            cl = str(thisSubject.student.klass)
            if cl[-1] == 'a':
                section = 'a'
            else:
                section = 'b'
            thisSubject.predicted_hy = int(
                maths_3testhyprediction(thisSubject.test1, thisSubject.test2, thisSubject.test3,
                                        thisSubject.student.dob, section))
            thisSubject.save()

        elif thisSubject.name == 'Science':
            cl = str(thisSubject.student.klass)
            if cl[-1] == 'a':
                section = 'a'
            else:
                section = 'b'
            thisSubject.predicted_hy = int(
                science_3testhyprediction(thisSubject.test1, thisSubject.test2, thisSubject.test3,
                                          thisSubject.student.dob, section))
            thisSubject.save()

        else:
            pass


def get_predicted_marks(user, subjects):
    try:
        hindi = subjects.get(name='Hindi')
        predicted_hindihy = predictionConvertion(hindi.predicted_hy)
    except:
        predicted_hindihy = 0
    try:
        maths = subjects.get(name='Maths')
        predicted_mathshy = predictionConvertion(maths.predicted_hy)
    except:
        predicted_mathshy = 0
    try:
        english = subjects.get(name='English')
        predicted_englishhy = predictionConvertion(english.predicted_hy)
    except:
        predicted_englishhy = 0
    try:
        science = subjects.get(name='Science')
        predicted_sciencehy = predictionConvertion(science.predicted_hy)
    except:
        predicted_sciencehy = 0

    return predicted_hindihy, predicted_mathshy, predicted_englishhy, predicted_sciencehy


def averageoftest(test, test2=None, test3=None):
    if test2 is None and test3 is None:
        testmarks = np.array(test)
        return np.mean(testmarks)
    elif test3 is None:
        testmarks = np.array(test)
        testmarks2 = np.array(test2)
        return np.mean(testmarks), np.mean(testmarks2)
    else:
        testmarks = np.array(test)
        testmarks2 = np.array(test2)
        testmarks3 = np.array(test3)
        return np.mean(testmarks), np.mean(testmarks2), np.mean(testmarks3)


# all the helper functions for teacher pages

def teacher_get_students_classwise(req):
    user = req.user
    profile = user.teacher
    subject = profile.subject_set.all()

    allstudents = []  # list of subjects of all students (taught by the teacher)
    klass_dict = {}  # dictionary for subjects of individual classes
    all_klasses = []  # list of all unique classes taught by the teacher
    all_klasses = list(unique_everseen(all_klasses))

    for i in subject:
        allstudents.append(i)
        all_klasses.append(str(i.student.klass))

    # fill out the dictionary for subjects of each class
    for k in all_klasses:
        sub9a = []
        for j in subject:
            if str(j.student.klass) == str(k):
                sub9a.append(j)
                temp_dict = {str(k): sub9a}
                klass_dict.update(temp_dict)
    return klass_dict, all_klasses


def teacher_get_testmarks_classwise(req, klass_dict):
    klass_test1_dict = {}  # dictionary to hold test1 marks of different classes
    klass_test2_dict = {}
    klass_test3_dict = {}

    # fill out the above dictionaries

    for i in klass_dict.values():
        kk = i
        klasstest1 = []
        klasstest2 = []
        klasstest3 = []

        for j in kk:
            klasstest1.append(j.test1)
            klasstest2.append(j.test2)
            klasstest3.append(j.test3)
            testm1 = {str(j.student.klass): klasstest1}
            testm2 = {str(j.student.klass): klasstest2}
            testm3 = {str(j.student.klass): klasstest3}
        klass_test1_dict.update(testm1)
        klass_test2_dict.update(testm2)
        klass_test3_dict.update(testm3)
    return klass_test1_dict, klass_test2_dict, klass_test2_dict


def teacher_get_classwise_studnetNames(request, klass_dict):
    ktdict = {}
    for i in klass_dict.values():
        kk = i
        kt = []
        for k in kk:
            kt.append(k.student)
            stu1 = {str(k.student.klass): kt}
        ktdict.update(stu1)
    return ktdict


def teacher_get_classwise_listofStudents(request, studict):
    kl0 = []
    kl1 = []
    kl2 = []
    kl3 = []
    kl4 = []
    kl5 = []
    nine_a = []
    nine_b = []
    nine_c = []
    ten_a = []
    ten_b = []
    ten_c = []

    for i, n in enumerate(studict.values()):
        eval('kl' + str(i)).extend(n)
    for i in kl0:

        if str(i.klass) == '9th a':
            nine_a = kl0
            break

    for i in kl1:
        if str(i.klass) == '9th b':
            nine_b = kl1
            break
    return nine_a, nine_b


def teacher_listofStudents(profile, klass):
    listofstudents = []
    subject_list = profile.subject_set.filter(student__klass__name=klass)
    for i in subject_list:
        listofstudents.append(i)
    return listofstudents


def teacher_listofStudentsMarks(profile, which_class):
    marks_class_test1 = []
    marks_class_test2 = []
    marks_class_test3 = []
    marks_class_predictedHy = []
    sub_class = profile.subject_set.filter(student__klass__name=which_class)
    if not sub_class:
        pass
    else:
        for i in sub_class:
            if i.test1:
                marks_class_test1.append(i.test1)
            if i.test2:
                marks_class_test2.append(i.test2)
            if i.test3:
                marks_class_test3.append(i.test3)
            if i.predicted_hy:
                marks_class_predictedHy.append(i.predicted_hy)
    return marks_class_test1, marks_class_test2, marks_class_test3, marks_class_predictedHy


def find_grade_from_marks(test1, test2=None, test3=None):
    test1_grade = []
    test2_grade = []
    test3_grade = []
    test1 = np.array(test1)
    if test2 is None:
        for i, n in enumerate(test1):
            if n < 4:
                test1_grade.append('F')
            if 4 <= n < 5:
                test1_grade.append('E')
            if 5 <= n < 6:
                test1_grade.append('D')
            if 6 <= n < 7:
                test1_grade.append('C')
            if 7 <= n < 8:
                test1_grade.append('B')
            if 8 <= n < 9:
                test1_grade.append('A')
            if 9 <= n <= 10:
                test1_grade.append('S')
        return test1_grade
    elif test3 is None:

        test2 = np.array(test2)

        for i, n in enumerate(test1):
            if n < 4:
                test1_grade.append('F')
            if 4 <= n < 5:
                test1_grade.append('E')
            if 5 <= n < 6:
                test1_grade.append('D')
            if 6 <= n < 7:
                test1_grade.append('C')
            if 7 <= n < 8:
                test1_grade.append('B')
            if 8 <= n < 9:
                test1_grade.append('A')
            if 9 <= n <= 10:
                test1_grade.append('S')

        for i, n in enumerate(test2):
            if n < 4:
                test2_grade.append('F')
            if 4 <= n < 5:
                test2_grade.append('E')
            if 5 <= n < 6:
                test2_grade.append('D')
            if 6 <= n < 7:
                test2_grade.append('C')
            if 7 <= n < 8:
                test2_grade.append('B')
            if 8 <= n < 9:
                test2_grade.append('A')
            if 9 <= n <= 10:
                test2_grade.append('S')
        return test1_grade, test2_grade
    else:
        test2 = np.array(test2)
        test3 = np.array(test3)
        for i, n in enumerate(test1):
            if n < 4:
                test1_grade.append('F')
            if 4 <= n < 5:
                test1_grade.append('E')
            if 5 <= n < 6:
                test1_grade.append('D')
            if 6 <= n < 7:
                test1_grade.append('C')
            if 7 <= n < 8:
                test1_grade.append('B')
            if 8 <= n < 9:
                test1_grade.append('A')
            if 9 <= n <= 10:
                test1_grade.append('S')

        for i, n in enumerate(test2):
            if n < 4:
                test2_grade.append('F')
            if 4 <= n < 5:
                test2_grade.append('E')
            if 5 <= n < 6:
                test2_grade.append('D')
            if 6 <= n < 7:
                test2_grade.append('C')
            if 7 <= n < 8:
                test2_grade.append('B')
            if 8 <= n < 9:
                test2_grade.append('A')
            if 9 <= n < 11:
                test2_grade.append('S')
        for i, n in enumerate(test3):
            if n < 4:
                test3_grade.append('F')
            if 4 <= n < 5:
                test3_grade.append('E')
            if 5 <= n < 6:
                test3_grade.append('D')
            if 6 <= n < 7:
                test3_grade.append('C')
            if 7 <= n < 8:
                test3_grade.append('B')
            if 8 <= n < 9:
                test3_grade.append('A')
            if 9 <= n <= 10:
                test3_grade.append('S')
        return test1_grade, test2_grade, test3_grade


def find_grade_fromMark_predicted(predicted):
    predicted = np.array(predicted)
    retpred = []
    for i, n in enumerate(predicted):
        if n == 0:
            retpred.append('F')
        elif n == 1:
            retpred.append('E')
        elif n == 2:
            retpred.append('D')
        elif n == 3:
            retpred.append('C')
        elif n == 4:
            retpred.append('B')
        elif n == 5:
            retpred.append('A')
        elif n == 6:
            retpred.append('S')
    return retpred


def find_frequency_grades(test1, test2=None, test3=None):
    t1_fg_a = 0
    t1_fg_b = 0
    t1_fg_c = 0
    t1_fg_d = 0
    t1_fg_e = 0
    t1_fg_f = 0
    t1_fg_s = 0

    t2_fg_a = 0
    t2_fg_b = 0
    t2_fg_c = 0
    t2_fg_d = 0
    t2_fg_f = 0
    t2_fg_e = 0
    t2_fg_s = 0

    t3_fg_a = 0
    t3_fg_b = 0
    t3_fg_c = 0
    t3_fg_d = 0
    t3_fg_e = 0
    t3_fg_f = 0
    t3_fg_s = 0
    if test2 is None:

        for i in test1:
            if i == 'E':
                t1_fg_e = t1_fg_e + 1
            elif i == 'F':
                t1_fg_f = t1_fg_f + 1
            elif i == 'A':
                t1_fg_a = t1_fg_a + 1
            elif i == 'B':
                t1_fg_b = t1_fg_b + 1
            elif i == 'C':
                t1_fg_c = t1_fg_c + 1
            elif i == 'D':
                t1_fg_d = t1_fg_d + 1
            elif i == 'S':
                t1_fg_s = t1_fg_s + 1
        return t1_fg_a, t1_fg_b, t1_fg_c, t1_fg_d, t1_fg_e, t1_fg_f, t1_fg_s

    elif test3 is None:
        for i in test1:
            if i == 'E':
                t1_fg_e = t1_fg_e + 1
            elif i == 'F':
                t1_fg_f = t1_fg_f + 1
            elif i == 'A':
                t1_fg_a = t1_fg_a + 1
            elif i == 'B':
                t1_fg_b = t1_fg_b + 1
            elif i == 'C':
                t1_fg_c = t1_fg_c + 1
            elif i == 'D':
                t1_fg_d = t1_fg_d + 1
            elif i == 'S':
                t1_fg_s = t1_fg_s + 1

        for i in test2:
            if i == 'E':
                t2_fg_e = t2_fg_e + 1
            elif i == 'F':
                t2_fg_f = t2_fg_f + 1
            elif i == 'A':
                t2_fg_a = t2_fg_a + 1
            elif i == 'B':
                t2_fg_b = t2_fg_b + 1
            elif i == 'C':
                t2_fg_c = t2_fg_c + 1
            elif i == 'D':
                t2_fg_d = t2_fg_d + 1
            elif i == 'S':
                t2_fg_s = t2_fg_s + 1

        return t1_fg_a, t1_fg_b, t1_fg_c, t1_fg_d, t1_fg_e, t1_fg_f, t1_fg_s, \
               t2_fg_a, t2_fg_b, t2_fg_c, t2_fg_d, t2_fg_e, t2_fg_f, t2_fg_s
    else:
        for i in test1:
            if i == 'E':
                t1_fg_e = t1_fg_e + 1
            elif i == 'F':
                t1_fg_f = t1_fg_f + 1
            elif i == 'A':
                t1_fg_a = t1_fg_a + 1
            elif i == 'B':
                t1_fg_b = t1_fg_b + 1
            elif i == 'C':
                t1_fg_c = t1_fg_c + 1
            elif i == 'D':
                t1_fg_d = t1_fg_d + 1
            elif i == 'S':
                t1_fg_s = t1_fg_s + 1

        for i in test2:
            if i == 'E':
                t2_fg_e = t2_fg_e + 1
            elif i == 'F':
                t2_fg_f = t2_fg_f + 1
            elif i == 'A':
                t2_fg_a = t2_fg_a + 1
            elif i == 'B':
                t2_fg_b = t2_fg_b + 1
            elif i == 'C':
                t2_fg_c = t2_fg_c + 1
            elif i == 'D':
                t2_fg_d = t2_fg_d + 1
            elif i == 'S':
                t2_fg_s = t2_fg_s + 1
        for i in test3:
            if i == 'E':
                t3_fg_e = t3_fg_e + 1
            elif i == 'F':
                t3_fg_f = t3_fg_f + 1
            elif i == 'A':
                t3_fg_a = t3_fg_a + 1
            elif i == 'B':
                t3_fg_b = t3_fg_b + 1
            elif i == 'C':
                t3_fg_c = t3_fg_c + 1
            elif i == 'D':
                t3_fg_d = t3_fg_d + 1
            elif i == 'S':
                t3_fg_s = t3_fg_s + 1
        return t1_fg_a, t1_fg_b, t1_fg_c, t1_fg_d, t1_fg_e, t1_fg_f, t1_fg_s, \
               t2_fg_a, t2_fg_b, t2_fg_c, t2_fg_d, t2_fg_e, t2_fg_f, t2_fg_s, \
               t3_fg_a, t3_fg_b, t3_fg_c, t3_fg_d, t3_fg_e, t3_fg_f, t3_fg_s
















        # def create_teacher(num):
        #     for i in range(3, num):
        #         us = User.objects.create_user(username='teacher' + str(i),
        #                                       email='teacher' + str(i) + '@gmail.com',
        #                                       password='dnpandey')
        #         us.save()
        #         gr = Group.objects.get(name='Teachers')
        #         gr.user_set.add(us)
        #
        #         teach = Teacher(teacheruser=us, experience=5, name=us.username)
        #         teach.save()
        #
        #
        # def create_student(num):
        #     for i in range(4, num):
        #         us = User.objects.create_user(username='student' + str(i),
        #                                       email='studentss' + str(i) + '@gmail.com',
        #                                       password='dnpandey')
        #         us.save()
        #         gr = Group.objects.get(name='Students')
        #         gr.user_set.add(us)
        #         cl = klass.objects.all()
        #         classes = []
        #         for k in cl:
        #             classes.append(k)
        #         stu = Student(studentuser=us, klass=classes[0], rollNumber=int(str(i) + '00'), name='stu' + str(i),
        #                       dob=timezone.now(), pincode=int(str(405060)))
        #         stu.save()
        #         sub = Subject(name='Science', student=stu)
        #         sub.save()


# class way

class Studs:
    def __init__(self, user):
        self.profile = user.student
        self.institution = self.profile.school.category
        self.school = self.profile.school.name


    def get_dob(self):
        return self.profile.dob

    def get_school(self):
        return self.profile.school

    def get_section(self):
        return self.profile.klass.name[-1]

    def get_batch(self):
        return self.profile.klass

    def my_subjects_objects(self):
        subs = self.profile.subject_set.all()
        subjects = []
        for sub in subs:
            subjects.append(sub)
        return subjects

    def my_subjects_names(self):
        subs = self.profile.subject_set.all()
        subjects = []
        for sub in subs:
            subjects.append(sub.name)
        subjects = list(unique_everseen(subjects))
        return subjects
    def get_taken_subjects(self):
        tests = SSCOnlineMarks.objects.filter(student = self.profile)
        subs = []
        for i in tests:
            subs.append(i.test.sub)
        sub = list(unique_everseen(subs))
        return sub

    def readmarks(self,subject):
        subjects = self.profile.subject_set.get(name = subject)
        test1 =test2 = test3 = testhy = test4 = testpredhy = -1
        test1 = subjects.test1
        test2 = subjects.test2
        test3 = subjects.test3
        testhy = subjects.hy
        test4 = subjects.test4
        testpredhhy = subjects.predicted_hy

        return test1,test2,test3,testhy,test4,testpredhy


    def hindi_3testhyprediction(self,test1, test2, test3, DOB, section):
        '''
        convert test marks into numpy arrays
        '''
        t1 = int(test1)
        t2 = int(test2)
        t3 = int(test3)

        if section == 'a':
            section = 1
        elif section == 'b':
            section = 2

        '''
        calculate age using DOB (dd/mm/year)
        '''
        days_in_year = 365.2425
        age = int((date(2018, 4, 1) - DOB).days / days_in_year)
        # age = int((date.today() - DOB).days / days_in_year)

        overall = np.array([[t1, t2, t3, age, section]])

        '''
            transform(scale) data to original data of school
        '''
        overall = sca_hindi.transform(overall)
        '''
            predict the hy marks using the trained ml algorithm
        '''
        prediction = svmhindihhy.predict(overall)
        return prediction


    def maths_3testhyprediction(self,test1, test2, test3, DOB, section):
        '''
        convert test marks into numpy arrays
        '''
        t1 = int(test1)
        t2 = int(test2)
        t3 = int(test3)

        if section == 'a':
            section = 1
        elif section == 'b':
            section = 2

        '''
            calculate age using DOB (dd/mm/year)
        '''
        days_in_year = 365.2425
        age = int((date(2018, 4, 1) - DOB).days / days_in_year)

        overall = np.array([[t1, t2, t3, age, section]])

        '''
            transform(scale) data to original data of school
        '''
        overall = sca_maths.transform(overall)
        '''
            predict the hy marks using the trained ml algorithm
        '''
        prediction = knn7mathshhy.predict(overall)
        return prediction


    def english_3testhyprediction(self,test1, test2, test3, DOB, section):
        '''
        convert test marks into numpy arrays
        '''
        t1 = int(test1)
        t2 = int(test2)
        t3 = int(test3)

        if section == 'a':
            section = 1
        elif section == 'b':
            section = 2

        '''
            calculate age using DOB (dd/mm/year)
        '''
        days_in_year = 365.2425
        age = int((date(2018, 4, 1) - DOB).days / days_in_year)

        overall = np.array([[t1, t2, t3, age, section]])

        '''
            transform(scale) data to original data of school
        '''
        overall = sca_english.transform(overall)
        '''
            predict the hy marks using the trained ml algorithm
        '''
        prediction = knn7englishhhy.predict(overall)
        return prediction


    def science_3testhyprediction(self,test1, test2, test3, DOB, section):
        #convert test marks into numpy arrays
        t1 = int(test1)
        t2 = int(test2)
        t3 = int(test3)

        if section == 'a':
            section = 1
        elif section == 'b':
            section = 2

            '''
                calculate age using DOB (dd/mm/year)
            '''
        days_in_year = 365.2425

        age = int((date(2018, 4, 1) - DOB).days / days_in_year)

        overall = np.array([[t1, t2, t3, age, section]])

        '''
            transform(scale) data to original data of school
        '''
        overall = sca_science.transform(overall)
        '''
            predict the hy marks using the trained ml algorithm
        '''
        prediction = knn7sciencehhy.predict(overall)
        return prediction


    def predictionConvertion(self, prediction):
        try:
            prediction = prediction[0]
        except:
            pass

        if prediction == 0:
            conversion = 35
        elif prediction == 1:
            conversion = 45
        elif prediction == 2:
            conversion = 55
        elif prediction == 3:
            conversion = 65
        elif prediction == 4:
            conversion = 75
        elif prediction == 5:
            conversion = 85
        elif prediction == 6:
            conversion = 95
        else:
            conversion = '404'
        return conversion

    def isQuestionTaken(self,question):
        all_test = SSCOnlineMarks.objects.filter(student = self.profile)
        for test in all_test:
            if question in test.test.sscquestions_set.all():
                return True

    def studentOldTests(self,teacher):
        kl = self.profile.klass
        all_tests = SSCKlassTest.objects.filter(creator = teacher.teacheruser,klas = kl)
        for i in all_tests:
            i.testTakers.add(self.profile)

# return all tests that are not taken by the student to be shown on home page

    def allOnlinetests(self,schoolName = None,klas = None):
        if schoolName is None:
            schoolName = 'BodhiAI'
        if self.profile.school.category == 'School':
            my_tests = KlassTest.objects.filter(testTakers=self.profile)
        elif self.profile.school.category == 'SSC':

            #  adding all tests papers created by BodhiAI
            #for all the students who register

            if self.profile.school.name== schoolName:
                # gets all the questions created by BodhiAI and also gets all
                # the OnlineMarks by student to compare what tests has the
                # student taken. If student has not taken any test then that
                # test is added to new_test list and is checked for
                # legitimitacy and then finally returned.
                if schoolName == 'JITO':
                    all_tests = SSCKlassTest.objects.filter(Q(creator__username =
                                                        schoolName)&Q(klas=klas))
                else:
                    all_tests = SSCKlassTest.objects.filter(creator__username= schoolName)
                print('new tests length {}'.format(len(all_tests)))
                already_taken_marks =\
                SSCOnlineMarks.objects.filter(student=self.profile)
                already_taken_tests = []
                takeable_tests = []
                for i in already_taken_marks:
                    already_taken_tests.append(i.test)
                new_tests = []
                for at in all_tests:
                    if at in already_taken_tests:
                        pass
                    else:
                        new_tests.append(at)
                # checks if test is legitimate
                for i in new_tests:
                    if i.sub != None or i.sub != '' or i.totalTime != 0:
                        takeable_tests.append(i)
                    else:
                        pass

                if schoolName == 'JITO':
                    try:
                        test_random = random.choice(takeable_tests)
                        test_random.testTakers.add(self.profile)
                        take_test = [test_random]
                        return take_test

                    except:
                        return takeable_tests
                else:
                    for t in takeable_tests:
                        t.testTakers.add(self.profile)
                    return takeable_tests
            else:
                all_tests = SSCKlassTest.objects.filter(testTakers =
                                                        self.profile)
                return all_tests

    def find_my_rank(self,test_id):
        all_mark = SSCOnlineMarks.objects.filter(test__id = test_id)
        my_marks = 0

        others_marks = []
        for i in all_mark:
            if i.student == self.profile:
                my_marks = i.marks
                published = i.test.published
                subject = i.test.sub
            else:
                others_marks.append(i.marks)
        others_marks.append(my_marks)
        ranked_marks = sorted(others_marks,reverse = True)
        total = len(ranked_marks)
        rank = ranked_marks.index(my_marks)
        rank = rank +1

        context =\
                {'rank':rank,'marks':my_marks,'total_students':total,'published':published,'subject':subject,'test_id':test_id}
        return context




    def already_takenTests_Subjects(self):
        taken_tests = SSCOnlineMarks.objects.filter(test__testTakers =
                                                    self.profile)
        subs = []
        for i in taken_tests:
            if i.test.sub != '':
                subs.append(i.test.sub)
        return list(unique_everseen(subs))

    def my_taken_subjects(self):
        subject_cache = StudentTakenSubjectsCache.objects.get(student =
                                                              self.profile)
        subjects = subject_cache.subjects
        return subjects
    def subjects_NotTakenTests(self):
        tests = SSCKlassTest.objects.filter(testTakers=self.profile)
        sub_list = []
        for i in tests:
            if i.sub != None or i.sub != '':
                sub_list.append(i.sub)
        return list(unique_everseen(sub_list))
    def subjects_OnlineTest(self,schoolName = None,klas = None):
        my_tests = self.allOnlinetests(schoolName=schoolName,klas = klas)
        subs = []
        if my_tests:
            for i in my_tests:
                subs.append(i.sub)
            subs = list(unique_everseen(subs))
            return subs
        else:
            return None

    def OnlineTestsSubwise(self, subject):
        if self.profile.school.category == 'School':
            my_tests = KlassTest.objects.filter(testTakers=self.profile, sub=
        subject)
        elif self.profile.school.category == 'SSC':
            my_tests = SSCKlassTest.objects.filter(testTakers =
                                                   self.profile,sub = subject)
        return my_tests

# Finds if student has already taken the test
    def is_onlineTestTaken(self, test_id):
        try:
            if self.institution == 'School':
                test = OnlineMarks.objects.get(test__id=test_id, student=
            self.profile)
                return test
            elif self.institution == 'SSC':
                test = SSCOnlineMarks.objects.get(test__id = test_id ,student =
                                                  self.profile)
                return test
        except Exception as e:
            print(str(e))
            return None


# Returns tests that are already taken

    def takenTests(self):
        if self.institution == 'SSC':
            takenT = SSCOnlineMarks.objects.filter(student = self.profile)
            return takenT


# Tests that are not taken and return a dictionary with test with it's
# subject,topics,number of questions and teacher name

    def toTake_Tests(self,num_tests,allTests = False):
        if self.institution == 'School':
           pass
        elif self.institution == 'SSC':
            all_tests = SSCKlassTest.objects.filter(testTakers = self.profile)
            takeable_tests = []
            for i in all_tests:
                if i.sub != None or i.sub == '':
                    takeable_tests.append(i)
            new_tests = {}
            for n,i in enumerate(takeable_tests):
                topics = []
                already_taken = SSCOnlineMarks.objects.filter(student =\
                                                           self.profile,test__id =i.id)
                if len(already_taken)>0:
                    continue
                else:
                    teacher = Teacher.objects.get(teacheruser = i.creator)
                    count_quest = 0
                    for j in i.sscquestions_set.all():
                        count_quest += 1
                        cat =\
                        self.changeIndividualNames(j.topic_category,j.section_category)
                        topics.append(cat)
                    topics = list(unique_everseen(topics))
                    new_tests[i.id] =\
                            {'subject':i.sub,'topics':topics,'num_questions':count_quest,'creator':teacher.name}
            if allTests:
                return new_tests
            else:
                return {k:new_tests[k] for k in list(new_tests)[:int(num_tests)]}





# Finds average of a test
    def online_findAverageofTest(self, test_id, percent=None):
        if percent:
            if self.institution == 'School':
                test = OnlineMarks.objects.filter(test__id=test_id)
            elif self.institution == 'SSC':
                test = SSCOnlineMarks.objects.filter(test__id=test_id)
            all_marks = []
            all_marks_percent = []
            for te in test:
                all_marks.append(int(te.marks))
                all_marks_percent.append((te.marks / te.test.max_marks) * 100)
            average = np.mean(all_marks)
            percent_average = np.mean(all_marks_percent)
            return average, percent_average


        else:
            if self.institution == 'School':
                test = OnlineMarks.objects.filter(test__id=test_id)
            elif self.institution == 'SSC':
                test = SSCOnlineMarks.objects.filter(test__id=test_id)
            all_marks = []
            for te in test:
                all_marks.append(int(te.marks))
            average = np.mean(all_marks)

            return average

# Finds student's percentile in a particular test
    def online_findPercentile(self, test_id):
        if self.institution == 'School':
            test = OnlineMarks.objects.filter(test__id=test_id)
            my_score = OnlineMarks.objects.get(test__id=test_id, student=self.profile)
        elif self.institution == 'SSC':
            test = SSCOnlineMarks.objects.filter(test__id=test_id)
            my_score = SSCOnlineMarks.objects.filter(test__id=test_id,
                                                     student=self.profile)[0]
        all_marks = []
        for te in test:
            all_marks.append(te.marks)
        num_students = len(all_marks)
        my_score = my_score.marks
        same_marks = -1
        less_marks = 0
        for i in all_marks:
            if i == my_score:
                same_marks += 1
            elif i < my_score:
                less_marks += 1
        if same_marks == -1:
            percentile = ((less_marks-same_marks) / num_students)
        else:
            percentile = ((less_marks + (0.5 * same_marks)) / num_students)
        print(percentile)
        print(all_marks)
        return percentile, all_marks
    def online_findPercentileDetail(self, test_id):
        test = SSCOnlineMarks.objects.filter(test__id=test_id)
        my_score = SSCOnlineMarks.objects.filter(test__id=test_id,
                                                     student=self.profile)[0]
        all_marks = []
        for te in test:
            all_marks.append(te.marks)
        num_students = len(all_marks)
        my_score = my_score.marks
        same_marks = -1
        less_marks = 0
        more_marks = 0
        for i in all_marks:
            if i == my_score:
                same_marks += 1
            elif i < my_score:
                less_marks += 1
            elif i > my_score:
                more_marks += 1
        if same_marks == -1:
            percentile = ((less_marks-same_marks) / num_students)
        else:
            percentile = ((less_marks + (0.5 * same_marks)) / num_students)
        print(percentile)
        print(all_marks)
        return percentile, all_marks,same_marks,less_marks,more_marks


    def online_QuestionPercentage(self, test_id):
        if self.institution == 'School':
            online_marks = OnlineMarks.objects.filter(test__id=test_id)
        elif self.institution == 'SSC':
            online_marks = SSCOnlineMarks.objects.filter(test__id=test_id)
        all_answers = []
        for aa in online_marks:
            all_answers.extend(aa.allAnswers)
        unique, counts = np.unique(all_answers, return_counts=True)
        freq = np.asarray((unique, counts)).T
        return freq


    def offline_QuestionPercentage(self, test_id):
        if self.institution == 'School':
            offline_marks = OnlineMarks.objects.filter(test__id=test_id)
        elif self.institution == 'SSC':
            offline_marks = SSCOfflineMarks.objects.filter(test__id=test_id)
        all_answers = []
        for aa in offline_marks:
            all_answers.extend(aa.allAnswers)
        unique, counts = np.unique(all_answers, return_counts=True)
        freq = np.asarray((unique, counts)).T
        return freq

    def offline_findPercentile(self,test_id):
        if self.institution == 'School':
            test = OnlineMarks.objects.filter(test__id=test_id)
            my_score = OnlineMarks.objects.get(test__id=test_id, student=self.profile)
        elif self.institution == 'SSC':
            test = SSCOfflineMarks.objects.filter(test__id=test_id)
            my_score = SSCOfflineMarks.objects.get(test__id=test_id, student=self.profile)
        all_marks = []
        for te in test:
            all_marks.append(te.marks)
        num_students = len(all_marks)
        my_score = my_score.marks
        same_marks = -1
        less_marks = 0
        for i in all_marks:
            if i == my_score:
                same_marks += 1
            elif i < my_score:
                less_marks += 1
        if same_marks == -1:
            percentile = ((less_marks-same_marks) / num_students)
        else:
            percentile = ((less_marks + (0.5 * same_marks)) / num_students)
        return percentile, all_marks


    def offline_findAverageofTest(self, test_id, percent=None):
        if percent:
            if self.institution == 'School':
                test = OnlineMarks.objects.filter(test__id=test_id)
            elif self.institution == 'SSC':
                test = SSCOfflineMarks.objects.filter(test__id=test_id)
            all_marks = []
            all_marks_percent = []
            for te in test:
                all_marks.append(int(te.marks))
                all_marks_percent.append((te.marks / te.test.max_marks) * 100)
            average = np.mean(all_marks)
            percent_average = np.mean(all_marks_percent)
            return average, percent_average


        else:
            if self.institution == 'School':
                test = OnlineMarks.objects.filter(test__id=test_id)
            elif self.institution == 'SSC':
                test = SSCOfflineMarks.objects.filter(test__id=test_id)
            all_marks = []
            for te in test:
                all_marks.append(int(te.marks))
            average = np.mean(all_marks)

            return average

# Finds number of right, wrong and skipped answers, also finds accuracy in a
# test
    def test_statistics(self,testid):
        if self.institution == 'Schoool':
            pass
        elif self.institution == 'SSC':
            # get instance of onlinemarks with testid
            marks = SSCOnlineMarks.objects.get(student = self.profile,test__id
                                               = testid)
            if marks:
                right_answers = 0
                wrong_answers = 0
                skipped_answers = 0
            # counts number of right,wrong and skipped answers
                for ra in marks.rightAnswers:
                    right_answers += 1
                for wa in marks.wrongAnswers:
                    wrong_answers += 1
                for sp in marks.skippedAnswers:
                    skipped_answers += 1
            # finds accuracy on the basis of counting done above
                try:
                    accuracy = ((right_answers)/(right_answers+wrong_answers))*100
                except Exception as e:
                    accuracy = 0
                return right_answers,wrong_answers,skipped_answers,accuracy
    def offline_test_statistics(self,test_id):
        if self.institution == 'Schoool':
            pass
        elif self.institution == 'SSC':
            # get instance of onlinemarks with testid
            marks = SSCOfflineMarks.objects.get(student = self.profile,test__id
                                               = test_id)
            if marks:
                right_answers = 0
                wrong_answers = 0
                skipped_answers = 0
            # counts number of right,wrong and skipped answers
                for ra in marks.rightAnswers:
                    right_answers += 1
                for wa in marks.wrongAnswers:
                    wrong_answers += 1
                for sp in marks.skippedAnswers:
                    skipped_answers += 1
            # finds accuracy on the basis of counting done above
                try:
                    accuracy = ((right_answers)/(right_answers+wrong_answers))*100
                except Exception as e:
                    accuracy = 0
                return right_answers,wrong_answers,skipped_answers,accuracy


# Finds the subjectwise accuracy (eg. SSCMultipleSections) of a test
    def test_SubjectAccuracy(self,testid):
        if self.institution == 'School':
            pass
        elif self.institution == 'SSC':
            # get onlinemarks object of a particular test
            marks = SSCOnlineMarks.objects.get(student = self.profile,test__id
                                               = testid)
            right_answers = []
            wrong_answers = []
            skipped_answers = []
            subjectra = []
            subjectwa = []
            subjectsa = []
            # find all the right answers with their subjects
            for ra in marks.rightAnswers:
                question = SSCquestions.objects.get(choices__id = ra)
                sub = question.section_category
                right_answers.append(question.id)
                subjectra.append(sub)
            # find all the wrong answers with their subjects
            for wa in marks.wrongAnswers:
                question = SSCquestions.objects.get(choices__id = wa)
                sub = question.section_category
                wrong_answers.append(question.id)
                subjectwa.append(sub)
            # find all the skipped answers with their subjects
            for sa in marks.skippedAnswers:
                question = SSCquestions.objects.get(id = sa)
                sub = question.section_category
                skipped_answers.append(question.id)
                subjectsa.append(sub)
            # zip answers with their subjects
            ra = list(zip(subjectra,right_answers))
            wa = list(zip(subjectwa,wrong_answers))
            sp= list(zip(subjectsa,skipped_answers))
            # find unique questions ids and thier counts
            unique, counts = np.unique(ra, return_counts=True)
            raf = np.asarray((unique, counts)).T
            unique, counts = np.unique(wa, return_counts=True)
            waf = np.asarray((unique, counts)).T
            unique, counts = np.unique(sp, return_counts=True)
            spf = np.asarray((unique, counts)).T
            new_ra = {}
            # if subject is in student's subject then add subject count to a
            # dictionary
            for i,j in raf:
                if  i in self.my_subjects_names():
                    new_ra[i] = j
            new_wa = {}
            for i,j in waf:
                if  i in self.my_subjects_names():
                    new_wa[i] = j
            new_sa = {}
            for i,j in spf:
                if  i in self.my_subjects_names():
                    new_sa[i] = j
            # if length of right or wrong answer dictionaries are not same then
            # add the missing subject to the shorter dictionary (works when
            # accuracy of one of the subjects is 100%)
            if len(new_ra) > len(new_wa):
                for i in new_ra.keys():
                    if not i in new_wa.keys():
                        new_wa[i] = 0
            elif len(new_ra) < len(new_wa):
                for i in new_wa.keys():
                    if not i in new_ra.keys():
                        new_ra[i] = 0
            # find subject accuracy by comparing number of right and wrong  answers per
            # subject
            sub_accuracy = {}
            for rk,rv in new_ra.items():
                for wk,wv in new_wa.items():
                    if rk == wk:
                        accuracy =\
                        ((int(new_ra[wk]))/((int(new_ra[wk])+int(new_wa[wk])))*100)
                        sub_accuracy[wk] = accuracy
            return sub_accuracy
    def offline_test_SubjectAccuracy(self,testid):
        if self.institution == 'School':
            pass
        elif self.institution == 'SSC':
            # get onlinemarks object of a particular test
            marks = SSCOfflineMarks.objects.get(student = self.profile,test__id
                                               = testid)
            right_answers = []
            wrong_answers = []
            skipped_answers = []
            subjectra = []
            subjectwa = []
            subjectsa = []
            # find all the right answers with their subjects
            for ra in marks.rightAnswers:
                try:
                    question = SSCquestions.objects.get(choices__id = ra)
                except Exception as e:
                    print(str(e))
                    continue
                sub = question.section_category
                right_answers.append(question.id)
                subjectra.append(sub)
            # find all the wrong answers with their subjects
            for wa in marks.wrongAnswers:
                try:
                    question = SSCquestions.objects.get(choices__id = wa)
                except Exception as e:
                    print(str(e))
                    continue
                sub = question.section_category
                wrong_answers.append(question.id)
                subjectwa.append(sub)
            # find all the skipped answers with their subjects
            for sa in marks.skippedAnswers:
                try:
                    question = SSCquestions.objects.get(id = sa)
                except Exception as e:
                    print(str(e))
                    continue
                sub = question.section_category
                skipped_answers.append(question.id)
                subjectsa.append(sub)
            # zip answers with their subjects
            ra = list(zip(subjectra,right_answers))
            wa = list(zip(subjectwa,wrong_answers))
            sp= list(zip(subjectsa,skipped_answers))
            # find unique questions ids and thier counts
            unique, counts = np.unique(ra, return_counts=True)
            raf = np.asarray((unique, counts)).T
            unique, counts = np.unique(wa, return_counts=True)
            waf = np.asarray((unique, counts)).T
            unique, counts = np.unique(sp, return_counts=True)
            spf = np.asarray((unique, counts)).T
            new_ra = {}
            # if subject is in student's subject then add subject count to a
            # dictionary
            for i,j in raf:
                if  i in self.my_subjects_names():
                    new_ra[i] = j
            new_wa = {}
            for i,j in waf:
                if  i in self.my_subjects_names():
                    new_wa[i] = j
            new_sa = {}
            for i,j in spf:
                if  i in self.my_subjects_names():
                    new_sa[i] = j
            # if length of right or wrong answer dictionaries are not same then
            # add the missing subject to the shorter dictionary (works when
            # accuracy of one of the subjects is 100%)
            if len(new_ra) > len(new_wa):
                for i in new_ra.keys():
                    if not i in new_wa.keys():
                        new_wa[i] = 0
            elif len(new_ra) < len(new_wa):
                for i in new_wa.keys():
                    if not i in new_ra.keys():
                        new_ra[i] = 0
            # find subject accuracy by comparing number of right and wrong  answers per
            # subject
            sub_accuracy = {}
            for rk,rv in new_ra.items():
                for wk,wv in new_wa.items():
                    if rk == wk:
                        accuracy =\
                        ((int(new_ra[wk]))/((int(new_ra[wk])+int(new_wa[wk])))*100)
                        sub_accuracy[wk] = accuracy
            return sub_accuracy

# Finds the overall weak topics of a student,else if singleTest is true then
# finds weak topics of single  test

    def weakAreas(self,subject,singleTest = None):
        if self.institution == 'School':
            my_marks = OnlineMarks.objects.filter(student = self.profile,test__sub
                                             = subject)
        elif self.institution == 'SSC':
            if singleTest == None:
                my_marks = SSCOnlineMarks.objects.filter(student = self.profile,test__sub
                                                 = subject)
                if 'Defence' in subject:
                    all_marks = SSCOnlineMarks.objects.filter(student= self.profile,
                                                    test__sub =
                                                    'Defence-MultipleSubjects')
                else:
                    all_marks = SSCOnlineMarks.objects.filter(student= self.profile,
                                                        test__sub =
                                                        'SSCMultipleSections')
                offline_my_marks =\
                SSCOfflineMarks.objects.filter(student=self.profile,test__sub=subject)
                offline_all_marks = SSCOfflineMarks.objects.filter(student =
                                                                   self.profile,test__sub
                                                                   =
                                                                   'SSCMultipleSections')


                indi_my_marks = None
            else:
                indi_my_marks = SSCOnlineMarks.objects.get(student=
                                                         self.profile,test__id =
                                                         singleTest)
                my_marks = None
                all_marks = None
                offline_my_marks = None
                offline_all_marks = None

        wrong_Answers = []
        skipped_Answers = []
        # if onetest object is present then adds all the wrong and skipped
        # answers to separate lists
        if indi_my_marks:
            for wa in indi_my_marks.wrongAnswers:
                wrong_Answers.append(wa)
            for sp in indi_my_marks.skippedAnswers:
                skipped_Answers.append(sp)
        # same as above, but when single subject tests are present
        if my_marks:
            for om in my_marks:
                for wa in om.wrongAnswers:
                    wrong_Answers.append(wa)
                for sp in om.skippedAnswers:
                    skipped_Answers.append(sp)

        # same as above, but when multiple subject tests are present
        if all_marks:
            for om in all_marks:
                for wa in om.wrongAnswers:
                    wrong_Answers.append(wa)
                for sp in om.skippedAnswers:
                    skipped_Answers.append(sp)
        # same as above, but when for offline my marks
        if offline_my_marks:
            for om in offline_my_marks:
                for wa in om.wrongAnswers:
                    wrong_Answers.append(wa)
                for sp in om.skippedAnswers:
                    skipped_Answers.append(sp)
        # same as above, but when for offline marks for multiple subjects
        if offline_all_marks:
            for om in offline_all_marks:
                for wa in om.wrongAnswers:
                    wrong_Answers.append(wa)
                for sp in om.skippedAnswers:
                    skipped_Answers.append(sp)

        wq=[]
        for i in wrong_Answers:
            if self.institution == 'School':
                qu = Questions.objects.get(choices__id = i)
            elif self.institution == 'SSC':
            # finds the questions objects of wrong questions
                try:
                    qu = SSCquestions.objects.get(choices__id = i)
                except Exception as e:
                    print(str(e))
                    continue
                if subject == 'SSCMultipleSections' or subject ==\
                'Defence-MultipleSubjects':
                    quid = qu.id
                    wq.append(quid)
                else:
                    if qu.section_category == subject:
                        quid = qu.id
                        wq.append(quid)
        for i in skipped_Answers:
            if self.institution == 'School':
                try:
                    qu = Questions.objects.get(id = i)
                except Exception as e:
                    print(str(e))
                    continue
            elif self.institution == 'SSC':
            # finds the questions objects of skipped questions
                try:
                    qu = SSCquestions.objects.get(id = i)
                except Exception as e:
                    print(str(e))
                    continue
                if subject == 'SSCMultipleSections'or subject ==\
                'Defence-MultipleSubjects':
                    quid = qu.id
                    wq.append(quid)
                else:
                    if qu.section_category == subject:
                        quid = qu.id
                        wq.append(quid)
        # finds unique questions with thier frequency
        unique, counts = np.unique(wq, return_counts=True)
        waf = np.asarray((unique, counts)).T
        nw_ind = []
        # sorts the list
        kk = np.sort(waf,0)[::-1]
        for u in kk[:,1]:
            for z,w in waf:
                if u == w:
                    if z in nw_ind:
                        continue
                    else:
                        nw_ind.append(z)
                        break
        final_freq = np.asarray((nw_ind,kk[:,1])).T
        return final_freq



# Finds the weak topic intensity, i.e. returns a list with topic name and
# number of wrong questions
    def weakAreas_Intensity(self,subject,singleTest = None):
        if singleTest == None:
            arr = self.weakAreas(subject)
        else:
            arr = self.weakAreas(subject,singleTest = singleTest)
            catSubject = []
            catCategory = []
        anal = []
        num = []
        for u,k in arr:
            if self.institution == 'School':
                qu = Questions.objects.get(id = u)
            elif self.institution == 'SSC':
                qu = SSCquestions.objects.get(id = u)
            if subject == 'SSCMultipleSections'or subject ==\
                'Defence-MultipleSubjects':
                quest_cat = qu.topic_category
                quest_sub = qu.section_category
                name_cat = self.changeIndividualNames(quest_cat,quest_sub)
                anal.append(name_cat)
                num.append(k)
            else:
                category = qu.topic_category
                anal.append(category)
                num.append(k)
        analysis = list(zip(anal,num))
        final_analysis = []
        final_num = []
        for u,k in analysis:
            if u in final_analysis:
                ind = final_analysis.index(u)
                temp = final_num[ind]
                final_num[ind] = temp + k
            else:
                final_analysis.append(u)
                final_num.append(k)

        waf = list(zip(final_analysis,final_num))
        return waf


    def weakAreas_IntensityAverage(self,subject):
        if self.institution  == 'School':
            pass
        elif self.institution == 'SSC':
            try:
                weak_cache =\
                StudentWeakAreasCache.objects.get(student=self.profile,subject=subject)
                cache_tests = weak_cache.numTests
                marks = SSCOnlineMarks.objects.filter(student =
                                                  self.profile,test__sub =
                                                  subject)
                if 'Defence' in subject:
                    all_marks = SSCOnlineMarks.objects.filter(student=
                                                          self.profile,test__sub='Defence-MultipleSubjects')
                else:

                    all_marks = SSCOnlineMarks.objects.filter(student=
                                                          self.profile,test__sub='SSCMultipleSections')



                all_tests_cache = len(marks) + len(all_marks)
                if cache_tests == all_tests_cache:
                    average_cat = weak_cache.categories
                    average_percent = weak_cache.accuracies

                    weak_average = list(zip(average_cat,average_percent))
                    print('{} this is the weak_average'.format(weak_average))
                    return weak_average
                else:
                    all_old_ids = weak_cache.allTest
                    new_ids = []
# putting new tests in a single list
                    for s_mark in marks:
                        if s_mark.id in all_old_ids:
                            continue
                        else:
                            new_ids.append(s_mark)
                    for s_mark in all_marks:
                        if s_mark.id in all_old_ids:
                            continue
                        else:
                            new_ids.append(s_mark)
# putting all tests in a single list
                    all_ids = []
                    ssc_marks_ids = []
                    for marks in marks:
                        all_ids.append(marks)
                        ssc_marks_ids.append(marks.id)
                    for marks in all_marks:
                        all_ids.append(marks)
                        ssc_marks_ids.append(marks.id)
                    new_test_arr = helper_weakAreas_Intensity(new_ids,subject)
                    waf = self.helper_alltestweakness(subject)
                    arr = np.array(new_test_arr)
                    average_cat = []
                    average_percent = []
                    wrong_total = []
                    total_cat = []

                    for i,j in waf:
                        if k in arr[:,0]:
                            ind = np.where(arr==i)
                            now_arr = arr[ind[0],1]
                            average =(int(now_arr[0])/int(j)*100)
                            wrong_total.append(now_arr[0])
                            total_cat.append(j)
                            average_cat.append(i)
                            average_percent.append(100-average)
                    overall =\
                    list(zip(average_cat,average_percent,wrong_total,total_cat))
                    weak_average = list(zip(average_cat,average_percent))
                    weak_cache = StudentWeakAreasCache.objects.get(student =
                                                                   self.profile,subject
                                                                  = subject)
                    weak_cache.categories = average_cat
                    weak_cache.accuracies = average_percent
                    weak_cache.subject = subject
                    weak_cache.allTests = ssc_marks_ids
                    weak_cache.numTests = len(ssc_marks_ids)
                    weak_cache.student = self.profile
                    weak_cache.save()
                    return weak_average





            except Exception as e:
                arr = self.weakAreas_Intensity(subject)

                marks = SSCOnlineMarks.objects.filter(student =
                                                  self.profile,test__sub =
                                                  subject)
                if 'Defence' in subject:
                    all_marks = SSCOnlineMarks.objects.filter(student=
                                                          self.profile,test__sub='Defence-MultipleSubjects')
                else:

                    all_marks = SSCOnlineMarks.objects.filter(student=
                                                          self.profile,test__sub='SSCMultipleSections')

                all_ids = []
                all_tests_ids = []
                for mark in marks:
                    all_tests_ids.append(mark.id)
                    for total in mark.allAnswers:
                        try:
                            quest = SSCquestions.objects.get(choices__id = total)
                        except Exception as e:
                            print(str(e))
                            continue
                        all_ids.append(quest.topic_category)
                    for sk in mark.skippedAnswers:
                        try:
                            quest = SSCquestions.objects.get(id = sk)
                        except Exception as e:
                            print(str(e))
                            continue
                        all_ids.append(quest.topic_category)
                # finds question ids from mixed category tests
                if all_marks:
                    for mark in all_marks:
                        all_tests_ids.append(mark.id)
                        for total in mark.allAnswers:
                            try:
                                quest = SSCquestions.objects.get(choices__id = total)
                            except Exception as e:
                                print(str(e))
                                continue
                            if quest.section_category == subject:
                                all_ids.append(quest.topic_category)
                        for sk in mark.skippedAnswers:
                            try:
                                quest = SSCquestions.objects.get(id = sk)
                            except Exception as e:
                                print(str(e))
                                continue
                            if quest.section_category == subject:
                                all_ids.append(quest.topic_category)
                #if offline_marks:
                #    for mark in offline_marks:
                #        for total in mark.allAnswers:
                #            try:
                #                quest = SSCquestions.objects.get(choices__id = total)
                #            except Exception as e:
                #                print(str(e))
                #                continue
                #            all_ids.append(quest.topic_category)
                #        for sk in mark.skippedAnswers:
                #            try:
                #                quest = SSCquestions.objects.get(id = sk)
                #            except Exception as e:
                #                print(str(e))
                #                continue
                #            all_ids.append(quest.topic_category)
                #if offline_all_marks:
                #    for mark in offline_all_marks:
                #        for total in mark.allAnswers:
                #            try:
                #                quest = SSCquestions.objects.get(choices__id = total)
                #            except Exception as e:
                #                print(str(e))
                #                continue
                #            if quest.section_category == subject:
                #                all_ids.append(quest.topic_category)
                #        for sk in mark.skippedAnswers:
                #            try:
                #                quest = SSCquestions.objects.get(id = sk)
                #            except Exception as e:
                #                print(str(e))
                #                continue
                #            if quest.section_category == subject:
                #                all_ids.append(quest.topic_category)





                unique, counts = np.unique(all_ids, return_counts=True)
                cat_quests = np.asarray((unique, counts)).T
                arr = np.array(arr)
                average_cat = []
                average_percent = []

                if len(arr)>0:
                    for i,j in cat_quests:
                        if i in arr[:,0]:
                            ind = np.where(arr==i)
                            now_arr = arr[ind[0],1]
                            average =(int(now_arr[0])/int(j)*100)
                            average_cat.append(i)
                            average_percent.append(100-average)

                    weak_average = list(zip(average_cat,average_percent))
                    weak_cache = StudentWeakAreasCache()
                    weak_cache = StudentWeakAreasCache()
                    weak_cache.categories = average_cat
                    weak_cache.accuracies = average_percent
                    weak_cache.subject = subject
                    weak_cache.allTests = all_tests_ids
                    weak_cache.numTests = len(all_tests_ids)
                    weak_cache.student = self.profile
                    weak_cache.save()




                    return weak_average
                else:
                    return 0
    def helper_alltestweakness(self,subject):
            marks = SSCOnlineMarks.objects.filter(student =
                                                  self.profile,test__sub =
                                                  subject)

            if 'Defence' in subject:
                all_marks = SSCOnlineMarks.objects.filter(student=
                                                      self.profile,test__sub='Defence-MultipleSubjects')
            else:

                all_marks = SSCOnlineMarks.objects.filter(student=
                                                      self.profile,test__sub='SSCMultipleSections')

            all_ids = []
            all_tests_ids = []
            for mark in marks:
                all_tests_ids.append(mark.id)
                for total in mark.allAnswers:
                    try:
                        quest = SSCquestions.objects.get(choices__id = total)
                    except Exception as e:
                        print(str(e))
                        continue
                    all_ids.append(quest.topic_category)
                for sk in mark.skippedAnswers:
                    try:
                        quest = SSCquestions.objects.get(id = sk)
                    except Exception as e:
                        print(str(e))
                        continue
                    all_ids.append(quest.topic_category)
            # finds question ids from mixed category tests
            if all_marks:
                for mark in all_marks:
                    all_tests_ids.append(mark.id)
                    for total in mark.allAnswers:
                        try:
                            quest = SSCquestions.objects.get(choices__id = total)
                        except Exception as e:
                            print(str(e))
                            continue
                        if quest.section_category == subject:
                            all_ids.append(quest.topic_category)
                    for sk in mark.skippedAnswers:
                        try:
                            quest = SSCquestions.objects.get(id = sk)
                        except Exception as e:
                            print(str(e))
                            continue
                        if quest.section_category == subject:
                            all_ids.append(quest.topic_category)
            #if offline_marks:
            #    for mark in offline_marks:
            #        for total in mark.allAnswers:
            #            try:
            #                quest = SSCquestions.objects.get(choices__id = total)
            #            except Exception as e:
            #                print(str(e))
            #                continue
            #            all_ids.append(quest.topic_category)
            #        for sk in mark.skippedAnswers:
            #            try:
            #                quest = SSCquestions.objects.get(id = sk)
            #            except Exception as e:
            #                print(str(e))
            #                continue
            #            all_ids.append(quest.topic_category)
            #if offline_all_marks:
            #    for mark in offline_all_marks:
            #        for total in mark.allAnswers:
            #            try:
            #                quest = SSCquestions.objects.get(choices__id = total)
            #            except Exception as e:
            #                print(str(e))
            #                continue
            #            if quest.section_category == subject:
            #                all_ids.append(quest.topic_category)
            #        for sk in mark.skippedAnswers:
            #            try:
            #                quest = SSCquestions.objects.get(id = sk)
            #            except Exception as e:
            #                print(str(e))
            #                continue
            #            if quest.section_category == subject:
            #                all_ids.append(quest.topic_category)





            unique, counts = np.unique(all_ids, return_counts=True)
            cat_quests = np.asarray((unique, counts)).T
            return cat_quests

    def weakAreas_timing(self,subject):
        arr = self.weakAreas(subject)
        anal = []
        num = []
        for u,k in arr:
            if self.institution == 'School':
                qu = Questions.objects.get(id = u)
            elif self.institution == 'SSC':
                qu = SSCquestions.objects.get(id = u)

            category = qu.topic_category
            anal.append(category)
            num.append(k)
        analysis = list(zip(anal,num))
        quest = []
        time_list = []
        if self.institution == 'SSC':
            myMarks = SSCOnlineMarks.objects.filter(student =
                                                    self.profile,test__sub = subject)
            if 'Defence' in subject:
                allMyMarks =\
                 SSCOnlineMarks.objects.filter(student=self.profile,test__sub=
                                              'Defence-MultipleSubjects')
            else:

                allMyMarks =\
                SSCOnlineMarks.objects.filter(student=self.profile,test__sub=
                                              'SSCMultipleSections')
            if myMarks:
                for t in myMarks:
                    for time in t.sscansweredquestion_set.all():
                        if time.quest.id in arr[:,0]:
                            quest.append(int(time.quest.id))
                            time_list.append(int(time.time))
            if allMyMarks:
                for t in myMarks:
                    for time in t.sscansweredquestion_set.all():
                        if time.quest.id in arr[:,0] and time.quest.section_category == subject:
                            quest.append(int(time.quest.id))
                            time_list.append(int(time.time))

        timer = list(zip(quest,time_list))

    def areawise_timing(self,subject,singleTest = None):
        all_questions = []
        all_timing = []
        if singleTest == None:
            if self.institution == 'School':
                marks = OnlineMarks.objects.filter(test__sub = subject,student =
                                                self.profile)
                for om in marks:
                    for aq in om.sscansweredquestion_set.all():
                        all_questions.append(aq.quest.topic_category)
                        all_timing.append(aq.time)

            elif self.institution == 'SSC':
                marks = SSCOnlineMarks.objects.filter(test__sub = subject, student =
                                                      self.profile)
                if marks:
                    for om in marks:
                        for aq in om.sscansweredquestion_set.all():
                            all_questions.append(aq.quest.topic_category)
                            all_timing.append(aq.time)

                if 'Defence' in subject:
                    all_marks =\
                    SSCOnlineMarks.objects.filter(student=self.profile,test__sub=
                                                  'Defence-MultipleSubjects')
                else:

                    all_marks =\
                    SSCOnlineMarks.objects.filter(student=self.profile,test__sub=
                                                  'SSCMultipleSections')
                if all_marks:
                    for om in all_marks:
                        for aq in om.sscansweredquestion_set.all():
                            if aq.quest.section_category == subject:
                                all_questions.append(aq.quest.topic_category)
                                all_timing.append(aq.time)
        else:
            if self.institution == 'SSC':
                indi_marks = SSCOnlineMarks.objects.get(student = self.profile,test__id =
                                                        singleTest)

                if indi_marks:
                    for aq in indi_marks.sscansweredquestion_set.all():
                        if subject == 'SSCMultipleSections' or subject ==\
                        'Defence-MultipleSubjects':
                            category =\
                                self.changeIndividualNames(aq.quest.topic_category,aq.quest.section_category)
                            all_questions.append(category)
                            all_timing.append(aq.time)

                        else:
                            if aq.quest.section_category == subject:
                                all_questions.append(aq.quest.topic_category)
                                all_timing.append(aq.time)


        areawise_timing = list(zip(all_questions,all_timing))
        dim1 = list(unique_everseen(all_questions))
        dim3 = []
        dim4 = []
        freq = []
        for j in dim1:
            k_val = 0
            n = 0
            for x,y in areawise_timing:
                if j == x and y != -1:
                    k_val += y
                    n += 1
            dim3.append(j)
            try:
                average_time = float(k_val/n)
                dim4.append(round(average_time,2))
                freq.append(n)
            except:
                pass
        timing = list(zip(dim3,dim4))
        freq_list = list(zip(dim3,freq))
        return timing,freq_list

    def offline_weakAreas(self,subject,singleTest = None):
        if self.institution == 'School':
            my_marks = OnlineMarks.objects.filter(student = self.profile,test__sub
                                             = subject)
        elif self.institution == 'SSC':
            if singleTest == None:
                my_marks = SSCOfflineMarks.objects.filter(student = self.profile,test__sub
                                                 = subject)
                all_marks = SSCOfflineMarks.objects.filter(student= self.profile,
                                                    test__sub =
                                                    'SSCMultipleSections')
                indi_my_marks = None
            else:
                indi_my_marks = SSCOfflineMarks.objects.get(student=
                                                         self.profile,test__id =
                                                         singleTest)
                my_marks = None
                all_marks = None

        wrong_Answers = []
        skipped_Answers = []
        # if onetest object is present then adds all the wrong and skipped
        # answers to separate lists
        if indi_my_marks:
            for wa in indi_my_marks.wrongAnswers:
                wrong_Answers.append(wa)
            for sp in indi_my_marks.skippedAnswers:
                skipped_Answers.append(sp)
        # same as above, but when single subject tests are present
        if my_marks:
            for om in my_marks:
                for wa in om.wrongAnswers:
                    wrong_Answers.append(wa)
                for sp in om.skippedAnswers:
                    skipped_Answers.append(sp)

        # same as above, but when multiple subject tests are present
        if all_marks:
            for om in all_marks:
                for wa in om.wrongAnswers:
                    wrong_Answers.append(wa)
                for sp in om.skippedAnswers:
                    skipped_Answers.append(sp)
        wq=[]
        for i in wrong_Answers:
            if self.institution == 'School':
                qu = Questions.objects.get(choices__id = i)
            elif self.institution == 'SSC':
            # finds the questions objects of wrong questions
                try:
                    qu = SSCquestions.objects.get(choices__id = i)
                except Exception as e:
                    print(str(e))
                    continue
                if subject == 'SSCMultipleSections' or subject ==\
                'Defence-MultitpleSubjects':
                    quid = qu.id
                    wq.append(quid)
                else:
                    if qu.section_category == subject:
                        quid = qu.id
                        wq.append(quid)
        for i in skipped_Answers:
            if self.institution == 'School':
                qu = Questions.objects.get(id = i)
            elif self.institution == 'SSC':
            # finds the questions objects of skipped questions
                try:
                    qu = SSCquestions.objects.get(id = i)
                except Exception as e:
                    print(str(e))
                    continue
                if subject == 'SSCMultipleSections' or subject ==\
                'Defence-MultitpleSubjects':
                    quid = qu.id
                    wq.append(quid)
                else:
                    if qu.section_category == subject:
                        quid = qu.id
                        wq.append(quid)
        # finds unique questions with thier frequency
        unique, counts = np.unique(wq, return_counts=True)
        waf = np.asarray((unique, counts)).T
        nw_ind = []
        # sorts the list
        kk = np.sort(waf,0)[::-1]
        for u in kk[:,1]:
            for z,w in waf:
                if u == w:
                    if z in nw_ind:
                        continue
                    else:
                        nw_ind.append(z)
                        break
        final_freq = np.asarray((nw_ind,kk[:,1])).T
        return final_freq

    def offline_weakAreas_Intensity(self,subject,singleTest = None):
        if singleTest == None:
            arr = self.offline_weakAreas(subject)
        else:
            arr = self.offline_weakAreas(subject,singleTest = singleTest)
            catSubject = []
            catCategory = []
        anal = []
        num = []
        for u,k in arr:
            if self.institution == 'School':
                qu = Questions.objects.get(id = u)
            elif self.institution == 'SSC':
                qu = SSCquestions.objects.get(id = u)
            if subject == 'SSCMultipleSections' or subject == 'Defence-MultipleSubjects':
                quest_cat = qu.topic_category
                quest_sub = qu.section_category
                name_cat = self.changeIndividualNames(quest_cat,quest_sub)
                anal.append(name_cat)
                num.append(k)
            else:
                category = qu.topic_category
                anal.append(category)
                num.append(k)
        analysis = list(zip(anal,num))
        final_analysis = []
        final_num = []
        for u,k in analysis:
            if u in final_analysis:
                ind = final_analysis.index(u)
                temp = final_num[ind]
                final_num[ind] = temp + k
            else:
                final_analysis.append(u)
                final_num.append(k)

        waf = list(zip(final_analysis,final_num))
        return waf

    def offline_weakAreas_IntensityAverage(self,subject):
        arr = self.offline_weakAreas_Intensity(subject)
        if self.institution == 'School':
            pass
        elif self.institution == 'SSC':
            marks = SSCOfflineMarks.objects.filter(student =
                                                  self.profile,test__sub =
                                                  subject)
            if 'Defence' in subject:
                all_marks = SSCOfflineMarks.objects.filter(student=
                                                          self.profile,test__sub='Defence-MultipleSubjects')
            else:

                all_marks = SSCOfflineMarks.objects.filter(student=
                                                          self.profile,test__sub='SSCMultipleSections')
            all_ids = []
            for mark in marks:
                for total in mark.allAnswers:
                    try:
                        quest = SSCquestions.objects.get(choices__id = total)
                    except Exception as e:
                        print(str(e))
                        continue
                    all_ids.append(quest.topic_category)
                for sk in mark.skippedAnswers:
                    try:
                        quest = SSCquestions.objects.get(id = sk)
                    except Exception as e:
                        print(str(e))
                        continue
                    all_ids.append(quest.topic_category)
            # finds question ids from mixed category tests
            if all_marks:
                for mark in all_marks:
                    for total in mark.allAnswers:
                        try:
                            quest = SSCquestions.objects.get(choices__id = total)
                        except Exception as e:
                            print(str(e))
                            continue
                        if quest.section_category == subject:
                            all_ids.append(quest.topic_category)
                    for sk in mark.skippedAnswers:
                        try:
                            quest = SSCquestions.objects.get(id = sk)
                        except Exception as e:
                            print(str(e))
                            continue
                        if quest.section_category == subject:
                            all_ids.append(quest.topic_category)

            unique, counts = np.unique(all_ids, return_counts=True)
            cat_quests = np.asarray((unique, counts)).T
            arr = np.array(arr)
            average_cat = []
            average_percent = []

            if len(arr)>0:
                for i,j in cat_quests:
                    if i in arr[:,0]:
                        ind = np.where(arr==i)
                        now_arr = arr[ind[0],1]
                        average =(int(now_arr[0])/int(j)*100)
                        average_cat.append(i)
                        average_percent.append(average)
                weak_average = list(zip(average_cat,average_percent))
                return weak_average
            else:
                return 0


# gets marks of all the tests taken by student to be displayed on home page
    def test_information(self,subjects,all_subjects = None):
        if 'Defence' in subjects:
            multiple_marks = SSCOnlineMarks.objects.filter(test__sub =
                                                               'Defence-MultipleSubjects',student=self.profile)
        else:

            multiple_marks = SSCOnlineMarks.objects.filter(test__sub =
                                                           'SSCMultipleSections',student=self.profile)

        teacher_name = {}
        subject_marks = {}
        if all_subjects:
            subjects = all_subjects
        for sub in subjects:
            #teacher_name[sub.name] = sub.teacher
            # get all the marks objects subjectwise
            marks = SSCOnlineMarks.objects.filter(test__sub = sub,student =
                                                 self.profile).order_by('testTaken')
            if len(marks) >0:
                one_marks = []
                time = []
                # add date and marks to a dictionary with index subject
                for i in marks:
                    try:
                        one_marks.append(float(i.marks)/float(i.test.max_marks)*100)
                    except Exception as e:
                        print(str(e))
                        one_marks.append(float(0))
                    time.append(i.testTaken)
                    subject_marks[sub] = {'marks':one_marks,'time':time}
            if len(multiple_marks) > 0:
                multiple_one_marks = []
                multiple_time = []
                # add date and marks to a dictionary with index
                # subject(multiple sections)
                for i in multiple_marks:
                    multiple_one_marks.append(float(i.marks)/float(i.test.max_marks)*100)
                    multiple_time.append(i.testTaken)
                    subject_marks['SSCMultipleSections'] =\
                    {'marks':multiple_one_marks,'time':multiple_time}

        return subject_marks

# same as above but for api view
    def test_marks_api(self,subjects):
        if 'Defence' in subjects:
            multiple_marks = SSCOnlineMarks.objects.filter(test__sub =
                                                               'Defence-MultipleSubjects',student=self.profile)
        else:

            multiple_marks = SSCOnlineMarks.objects.filter(test__sub =
                                                           'SSCMultipleSections',student=self.profile)

        prev_performance = []
        for sub in subjects:
            # get all the marks objects subjectwise
            marks = SSCOnlineMarks.objects.filter(test__sub = sub,student =
                                                 self.profile).order_by('testTaken')
            if len(marks) >0:
                one_marks = []
                time = []
                # add date and marks to a dictionary with index subject
                for i in marks:
                    subject_marks = {}
                    try:
                        one_marks.append(float(i.marks)/float(i.test.max_marks)*100)
                    except Exception as e:
                        print(str(e))
                        one_marks.append(float(0))
                    time.append(i.testTaken)
                    subject_marks = {'subject':sub,'marks':one_marks,'time':time}
                prev_performance.append(subject_marks)
            if len(multiple_marks) > 0:
                multiple_one_marks = []
                multiple_time = []
                # add date and marks to a dictionary with index
                # subject(multiple sections)
                for i in multiple_marks:
                    multiple_one_marks.append(float(i.marks)/float(i.test.max_marks)*100)
                    multiple_time.append(i.testTaken)
                    subject_marks =\
                            {'subject':sub,'marks':multiple_one_marks,'time':multiple_time}
                    #prev_performance.append(subject_marks)


        return prev_performance





    def changeTopicNumbersNames(self,arr,subject):
        namedarr = []
        timing = []
        if subject == 'English':
            for i,j in arr:
                i = str(i)
                j = str(j)
                if i == '1.1':
                    namedarr.append('Antonym')
                    timing.append(j)
                elif i == '1.2':
                    namedarr.append('Synonym')
                    timing.append(j)
                elif i == '1.3':
                    namedarr.append('One word substitution')
                    timing.append(j)
                elif i == '1.4':
                    namedarr.append('Idioms & Phrases')
                    timing.append(j)
                elif i == '1.5':
                    namedarr.append('Phrasal Verbs')
                    timing.append(j)
                elif i == '1.6':
                    namedarr.append('Use of some verbs with particular nouns')
                    timing.append(j)
                elif i == '1.7':
                    namedarr.append('Tense')
                    timing.append(j)
                elif i == '2.1':
                    namedarr.append('Noun')
                    timing.append(j)
                elif i == '2.2':
                    namedarr.append('Pronoun')
                    timing.append(j)
                elif i == '2.3':
                    namedarr.append('Adjective')
                    timing.append(j)
                elif i == '2.4':
                    namedarr.append('Articles')
                    timing.append(j)
                elif i == '2.5':
                    namedarr.append('Verb')
                    timing.append(j)
                elif i == '2.6':
                    namedarr.append('Adverb')
                    timing.append(j)
                elif i == '2.7':
                    namedarr.append('Time & Tense')
                    timing.append(j)
                elif i == '2.8':
                    namedarr.append('Voice')
                    timing.append(j)
                elif i == '2.9':
                    namedarr.append('Non-Finites')
                    timing.append(j)
                elif i == '3.1':
                    namedarr.append('Narration')
                    timing.append(j)
                elif i == '3.2':
                    namedarr.append('Preposition')
                    timing.append(j)
                elif i == '3.3':
                    namedarr.append('Conjunction')
                    timing.append(j)
                elif i == '3.4':
                    namedarr.append('Subject verb agreement')
                    timing.append(j)
                elif i == '3.5':
                    namedarr.append('Common Errors')
                    timing.append(j)
                elif i == '3.6':
                    namedarr.append('Superfluous Expressions & Slang')
                    timing.append(j)



            return list(zip(namedarr,timing))
        if subject == 'General-Intelligence':
            for i,j in arr:
                if i == '1.1':
                    namedarr.append('Paper Cutting and Folding')
                    timing.append(j)
                elif i == '1.2':
                    namedarr.append('Mirror and Water Image')
                    timing.append(j)
                elif i == '1.3':
                    namedarr.append('Embedded Figures')
                    timing.append(j)
                elif i == '1.4':
                    namedarr.append('Figure Completion')
                    timing.append(j)
                elif i == '1.5':
                    namedarr.append('Counting Embedded Figures')
                    timing.append(j)
                elif i == '1.6':
                    namedarr.append('Counting in figures')
                    timing.append(j)
                elif i == '2.1':
                    namedarr.append('Analogy')
                    timing.append(j)
                elif i == '2.2':
                    namedarr.append('Multiple Analogy')
                    timing.append(j)
                elif i == '2.3':
                    namedarr.append('Choosing the analogous pair')
                    timing.append(j)
                elif i == '2.4':
                    namedarr.append('Number analogy (series pattern)')
                    timing.append(j)
                elif i =='2.5':
                    namedarr.append('Number analogy (missing)')
                    timing.append(j)
                elif i == '2.6':
                    namedarr.append('Alphabet based analogy')
                    timing.append(j)
                elif i == '2.7':
                    namedarr.append('Mixed analogy')
                    timing.append(j)
                elif i == '3.1':
                    namedarr.append('Series Completion (Diagram)')
                    timing.append(j)
                elif i == '3.2':
                    namedarr.append('Analogy (Diagram)')
                    timing.append(j)
                elif i == '3.3':
                    namedarr.append('Classification (Diagram)')
                    timing.append(j)
                elif i == '3.4':
                    namedarr.append('Dice & Boxes')
                    timing.append(j)
                elif i == '2.8':
                    namedarr.append('Ruled based analogy')
                    timing.append(j)
                elif i == '2.9':
                    namedarr.append('Alphabet Test')
                    timing.append(j)
                elif i == '4.1':
                    namedarr.append('Ranking')
                    timing.append(j)
                elif i == '5.1':
                    namedarr.append('Matrix')
                    timing.append(j)
                elif i == '6.1':
                    namedarr.append('Word Creation')
                    timing.append(j)
                elif i == '7.1':
                    namedarr.append('Odd one out')
                    timing.append(j)
                elif i == '8.1':
                    namedarr.append('Height')
                    timing.append(j)
                elif i == '9.1':
                    namedarr.append('Direction')
                    timing.append(j)
                elif i =='10.1':
                    namedarr.append('Statement & Conclusion')
                    timing.append(j)
                elif i == '11.1':
                    namedarr.append('Venn Diagram')
                    timing.append(j)
                elif i == '12.1':
                    namedarr.append('Missing number')
                    timing.append(j)
                elif i == '13.1':
                    namedarr.append('Logical Sequence of words')
                    timing.append(j)
                elif i == '14.1':
                    namedarr.append('Clock/Time')
                    timing.append(j)
                elif i == '15.1':
                    namedarr.append('Mathematical Operations')
                    timing.append(j)
                elif i == '16.1':
                    namedarr.append('Coding Decoding')
                    timing.append(j)
                elif i == '17.1':
                    namedarr.append('Series Test')
                    timing.append(j)
                elif i == '18.1':
                    namedarr.append('Syllogism')
                    timing.append(j)
                elif i == '19.1':
                    namedarr.append('Blood Relation')
                    timing.append(j)
                elif i == '20.1':
                    namedarr.append('Seating Arrangement')
                    timing.append(j)
                elif i == '22.1':
                    namedarr.append('Calender Test')
                    timing.append(j)
                elif i == '28.1':
                    namedarr.append('Symbols & Notations')
                    timing.append(j)





            return list(zip(namedarr,timing))
        if subject == 'Quantitative-Analysis':
            for i,j in arr:
                if i == '1.1':
                    namedarr.append('Age')
                    timing.append(j)
                elif i == '2.1':
                    namedarr.append('Alligation')
                    timing.append(j)
                elif i == '3.1':
                    namedarr.append('Area')
                    timing.append(j)
                elif i == '4.1':
                    namedarr.append('Average')
                    timing.append(j)
                elif i == '5.1':
                    namedarr.append('Boat & Stream')
                    timing.append(j)
                elif i == '6.1':
                    namedarr.append('Discount')
                    timing.append(j)
                elif i == '7.1':
                    namedarr.append('Fraction')
                    timing.append(j)
                elif i == '8.1':
                    namedarr.append('LCM & LCF')
                    timing.append(j)
                elif i == '9.1':
                    namedarr.append('Number System')
                    timing.append(j)
                elif i == '10.1':
                    namedarr.append('Percentage')
                    timing.append(j)
                elif i == '11.1':
                    namedarr.append('Pipes & Cistern')
                    timing.append(j)
                elif i == '12.1':
                    namedarr.append('Profit & Loss')
                    timing.append(j)
                elif i == '13.1':
                    namedarr.append('Ratio')
                    timing.append(j)
                elif i == '14.1':
                    namedarr.append('Simple Interest')
                    timing.append(j)
                elif i == '15.1':
                    namedarr.append('Simplification')
                    timing.append(j)
                elif i == '16.1':
                    namedarr.append('Speed & Distance')
                    timing.append(j)
                elif i == '17.1':
                    namedarr.append('Square & Cube root')
                    timing.append(j)
                elif i == '18.1':
                    namedarr.append('Surds & Indices')
                    timing.append(j)
                elif i == '19.1':
                    namedarr.append('Time & Work')
                    timing.append(j)
                elif i == '20.1':
                    namedarr.append('Train')
                    timing.append(j)
                elif i == '21.1':
                    namedarr.append('Volume')
                    timing.append(j)
                elif i == '22.1':
                    namedarr.append('Trigonometry')
                    timing.append(j)
                elif i == '23.1':
                    namedarr.append('Partnership')
                    timing.append(j)
                elif i == '24.1':
                    namedarr.append('Compound Interest')
                    timing.append(j)
                elif i == '25.1':
                    namedarr.append('Decimals')
                    timing.append(j)


            return list(zip(namedarr,timing))
        if subject == 'General-Knowledge':
            for i,j in arr:
                if i == '1.1':
                    namedarr.append('Inventions & Innovators')
                    timing.append(j)
                if i == '2.1':
                   namedarr.append('Bird Sanctuary')
                   timing.append(j)
                if i == '3.1':
                   namedarr.append('Books & Authors')
                   timing.append(j)
                if i == '4.1':
                   namedarr.append('Countries, Capitals & Currencies')
                   timing.append(j)
                if i == '5.1':
                   namedarr.append('Current Affairs')
                   timing.append(j)
                if i == '6.1':
                   namedarr.append('Economics')
                   timing.append(j)
                if i == '7.1':
                   namedarr.append('General Science')
                   timing.append(j)
                if i == '8.1':
                   namedarr.append('Biology')
                   timing.append(j)
                if i == '9.1':
                   namedarr.append('Chemistry')
                   timing.append(j)
                if i == '10.1':
                   namedarr.append('Science & Technology')
                   timing.append(j)
                if i == '11.1':
                   namedarr.append('Physics')
                   timing.append(j)
                if i == '12.1':
                   namedarr.append('Geography')
                   timing.append(j)
                if i == '13.1':
                   namedarr.append('National Organizations')
                   timing.append(j)
                if i == '14.1':
                   namedarr.append('History')
                   timing.append(j)
                if i == '15.1':
                   namedarr.append('Honors & Awards')
                   timing.append(j)
                if i == '16.1':
                   namedarr.append('Important Dates')
                   timing.append(j)
                if i == '17.1':
                   namedarr.append('Indian Agriculture')
                   timing.append(j)
                if i == '18.1':
                   namedarr.append('Indian Constitution')
                   timing.append(j)
                if i == '19.1':
                   namedarr.append('Indian Culture')
                   timing.append(j)
                if i == '20.1':
                   namedarr.append('Indian Museums')
                   timing.append(j)
                if i == '21.1':
                   namedarr.append('Polity (India)')
                   timing.append(j)
                if i == '22.1':
                   namedarr.append('Sports')
                   timing.append(j)
                if i == '23.1':
                   namedarr.append('Superlatives(India)')
                   timing.append(j)
                if i == '24.1':
                   namedarr.append('Symbols of States (India)')
                   timing.append(j)
                if i == '25.1':
                   namedarr.append('Tiger Reserve')
                   timing.append(j)
                if i == '26.1':
                   namedarr.append('UNESCO Word Heritage Sites(India)')
                   timing.append(j)
                if i == '27.1':
                   namedarr.append('World Organizations')
                   timing.append(j)
                if i == '28.1':
                   namedarr.append('Polity (World)')
                   timing.append(j)
            return list(zip(namedarr,timing))

        if subject == 'General-Science':
            for i,j in arr:
                if i == '1.1':
                    namedarr.append('गुरूत्व स्थूल पदार्थ के गुण व प्रकाशन')
                    timing.append(j)
                if i == '2.1':
                    namedarr.append('लेंस व दर्पण')
                    timing.append(j)
                if i == '3.1':
                    namedarr.append('आधुनिक भौतिकी')
                    timing.append(j)
                if i == '4.1':
                    namedarr.append('विमिय तथा द्विविमिय')
                    timing.append(j)
                if i == '5.1':
                    namedarr.append('कॉमन प्रश्नपत्र भौतिक शास्त्रा')
                    timing.append(j)
                if i == '6.1':
                    namedarr.append('दाब घटाव प्रत्यासा')
                    timing.append(j)
                if i == '7.1':
                    namedarr.append('ध्वनि')
                    timing.append(j)
                if i == '8.1':
                    namedarr.append('मात्रक विभाएं मापन')
                    timing.append(j)
                if i == '9.1':
                    namedarr.append('सदिश तथा अदिश')
                    timing.append(j)
                if i == '10.1':
                    namedarr.append('कार्य,ऊर्जा व शक्ति')
                    timing.append(j)
                if i == '11.1':
                    namedarr.append('कोशिका विज्ञान')
                    timing.append(j)
                if i == '12.1':
                    namedarr.append('पादप जगत')
                    timing.append(j)
                if i == '13.1':
                    namedarr.append('पादप शरीर क्रिया विज्ञान')
                    timing.append(j)
                if i == '14.1':
                    namedarr.append('आर्थिक वनस्पति विज्ञान')
                    timing.append(j)
                if i == '15.1':
                    namedarr.append('जन्तु विज्ञान')
                    timing.append(j)
                if i == '16.1':
                    namedarr.append('जन्तु उत्तक एवं पोषण')
                    timing.append(j)
                if i == '17.1':
                    namedarr.append('आनुवांशिकी')
                    timing.append(j)
                if i == '18.1':
                    namedarr.append('मानव स्वास्थ्य एवं रोग')
                    timing.append(j)
                if i == '19.1':
                    namedarr.append('जैव प्रोद्यौगिकी')
                    timing.append(j)
                if i == '20.1':
                    namedarr.append('कम्प्यूटर एवं सूचना प्रोद्यौगिकी')
                    timing.append(j)


            return list(zip(namedarr,timing))
# categories for GroupX

        if subject == 'Defence-English':
            for i,j in arr:
                if i == '1.1':
                    namedarr.append('Comprehension')
                    timing.append(j)
                if i == '2.1':
                    namedarr.append('Judge Comprehension')
                    timing.append(j)
                if i == '3.1':
                    namedarr.append('Inferences')
                    timing.append(j)
                if i == '4.1':
                    namedarr.append('Vocabulary')
                    timing.append(j)
                if i == '5.1':
                    namedarr.append('Composition')
                    timing.append(j)
                if i == '6.1':
                    namedarr.append('Subject and Verb')
                    timing.append(j)
                if i == '7.1':
                    namedarr.append('Verb and their use')
                    timing.append(j)
                if i == '8.1':
                    namedarr.append('Sequence of tenses')
                    timing.append(j)
                if i == '9.1':
                    namedarr.append('Transformation')
                    timing.append(j)
                if i == '10.1':
                    namedarr.append('Grammer')
                    timing.append(j)
                if i == '11.1':
                    namedarr.append('Spellings')
                    timing.append(j)
                if i == '12.1':
                    namedarr.append('Word formation')
                    timing.append(j)
                if i == '11.1':
                    namedarr.append('Antonyms& Synonyms')
                    timing.append(j)
                if i == '11.1':
                    namedarr.append('Word Substitution')
                    timing.append(j)
                if i == '12.1':
                    namedarr.append('Correct use of words')
                    timing.append(j)
                if i == '13.1':
                    namedarr.append('Confusing words')
                    timing.append(j)
                if i == '14.1':
                    namedarr.append('Word order')
                    timing.append(j)
                if i == '15.1':
                    namedarr.append('Correct use of Adverbs')
                    timing.append(j)
                if i == '16.1':
                    namedarr.append('Idioms and Phrases')
                    timing.append(j)
                if i == '17.1':
                    namedarr.append('Use of simple idioms')
                    timing.append(j)
                if i == '18.1':
                    namedarr.append('Use of common proverbs')
                    timing.append(j)
                if i == '19.1':
                    namedarr.append('Direct/Indirect sentences')
                    timing.append(j)
                if i == '20.1':
                    namedarr.append('Direct to Indirect form')
                    timing.append(j)
                if i == '21.1':
                    namedarr.append('Indirect to Direct')
                    timing.append(j)
                if i == '22.1':
                    namedarr.append('Active and Passive voice')
                    timing.append(j)
                if i == '23.1':
                    namedarr.append('Active to Passive voice')
                    timing.append(j)
                if i == '22.1':
                    namedarr.append('Passive to Active voice')
                    timing.append(j)
                if i == '50.1':
                    namedarr.append('To be categorized')
                    timing.append(j)

            return list(zip(namedarr,timing))

        if subject == 'Defence-Physics':
            for i,j in arr:
                if i == '1.1':
                    namedarr.append('Unit of Dimension')
                    timing.append(j)
                if i == '2.1':
                    namedarr.append('Scalers&Vectors')
                    timing.append(j)
                if i == '3.1':
                    namedarr.append('Motion in straight line')
                    timing.append(j)
                if i == '4.1':
                    namedarr.append('Law of Motion')
                    timing.append(j)
                if i == '5.1':
                    namedarr.append('Projectile Motion')
                    timing.append(j)
                if i == '6.1':
                    namedarr.append('Circular Motion')
                    timing.append(j)
                if i == '7.1':
                    namedarr.append('Friction ')
                    timing.append(j)
                if i == '8.1':
                    namedarr.append('Work power & Energy')
                    timing.append(j)
                if i == '9.1':
                    namedarr.append('Collision')
                    timing.append(j)
                if i == '10.1':
                    namedarr.append('Rotational motion % Moment of Inertia')
                    timing.append(j)
                if i == '11.1':
                    namedarr.append('Gravitation')
                    timing.append(j)
                if i == '12.1':
                    namedarr.append('Elasticity')
                    timing.append(j)
                if i == '13.1':
                    namedarr.append('Fluid Pressure ')
                    timing.append(j)
                if i == '14.1':
                    namedarr.append('Viscocity& Flow of fluids')
                    timing.append(j)
                if i == '15.1':
                    namedarr.append('Surface Tension')
                    timing.append(j)
                if i == '16.1':
                    namedarr.append('Oscillations')
                    timing.append(j)
                if i == '17.1':
                    namedarr.append('Thermometry')
                    timing.append(j)
                if i == '18.1':
                    namedarr.append('Thermal Expansion')
                    timing.append(j)
                if i == '19.1':
                    namedarr.append('Calorimetry')
                    timing.append(j)
                if i == '20.1':
                    namedarr.append('Transmission of Heat')
                    timing.append(j)
                if i == '21.1':
                    namedarr.append('Thermodynamics')
                    timing.append(j)
                if i == '22.1':
                    namedarr.append('Kinetic Theory of gases')
                    timing.append(j)
                if i == '23.1':
                    namedarr.append('Wave Motion')
                    timing.append(j)
                if i == '24.1':
                    namedarr.append('Superposition of waves')
                    timing.append(j)
                if i == '25.1':
                    namedarr.append('Speed of Sound')
                    timing.append(j)
                if i == '26.1':
                    namedarr.append('Vibrations in air columns')
                    timing.append(j)
                if i == '27.1':
                    namedarr.append('Vibration of Strings')
                    timing.append(j)
                if i == '28.1':
                    namedarr.append('Dopplers Effect')
                    timing.append(j)
                if i == '29.1':
                    namedarr.append('Musical Sound& Ultra sound')
                    timing.append(j)
                if i == '30.1':
                    namedarr.append('Electric charge & Electric Field')
                    timing.append(j)
                if i == '31.1':
                    namedarr.append('Gauss Theorem')
                    timing.append(j)
                if i == '32.1':
                    namedarr.append('Electric Capacitance')
                    timing.append(j)
                if i == '33.1':
                    namedarr.append('Electric Conduction')
                    timing.append(j)
                if i == '34.1':
                    namedarr.append('Ohms Law')
                    timing.append(j)
                if i == '35.1':
                    namedarr.append('Electromotive force & Electric cell')
                    timing.append(j)
                if i == '36.1':
                    namedarr.append('Kirchoffs law & wheatstone bridge')
                    timing.append(j)
                if i == '37.1':
                    namedarr.append('Potentiometer')
                    timing.append(j)
                if i == '38.1':
                    namedarr.append('Heating effect of current')
                    timing.append(j)
                if i == '39.1':
                    namedarr.append('Chemical effect of current')
                    timing.append(j)
                if i == '40.1':
                    namedarr.append('Magnetic effect of current')
                    timing.append(j)
                if i == '41.1':
                    namedarr.append('Electrical Instruments')
                    timing.append(j)
                if i == '42.1':
                    namedarr.append('Magnetic Field')
                    timing.append(j)
                if i == '43.1':
                    namedarr.append('Magnetic effects of matter & terrestrial\
                                    magnetism')
                    timing.append(j)
                if i == '44.1':
                    namedarr.append('Electromagnetic Induction')
                    timing.append(j)
                if i == '45.1':
                    namedarr.append('Alternating Current')
                    timing.append(j)
                if i == '46.1':
                    namedarr.append('Reflection of light')
                    timing.append(j)
                if i == '47.1':
                    namedarr.append('Refraction of light')
                    timing.append(j)
                if i == '48.1':
                    namedarr.append('Refraction at Spherical surface & by\
                                    lenses')
                    timing.append(j)
                if i == '49.1':
                    namedarr.append('Prism & scattering of light')
                    timing.append(j)
                if i == '50.1':
                    namedarr.append('Optical instruments')
                    timing.append(j)
                if i == '51.1':
                    namedarr.append('Human eye & defects of vision')
                    timing.append(j)
                if i == '52.1':
                    namedarr.append('Wave theory of light')
                    timing.append(j)
                if i == '53.1':
                    namedarr.append('Interferance & Deflection of light')
                    timing.append(j)
                if i == '54.1':
                    namedarr.append('Polarization of light')
                    timing.append(j)
                if i == '55.1':
                    namedarr.append('Photometry')
                    timing.append(j)
                if i == '56.1':
                    namedarr.append('Dual nature of radiation & matter')
                    timing.append(j)
                if i == '57.1':
                    namedarr.append('Electromagnetic waves')
                    timing.append(j)
                if i == '58.1':
                    namedarr.append('Structure of Atom')
                    timing.append(j)
                if i == '59.1':
                    namedarr.append('Radioactivity')
                    timing.append(j)
                if i == '60.1':
                    namedarr.append('Nuclear fission & fusion')
                    timing.append(j)
                if i == '61.1':
                    namedarr.append('Semi-conductor,diode & Transistors')
                    timing.append(j)
                if i == '62.1':
                    namedarr.append('Digital electronics & logic gates')
                    timing.append(j)

            return list(zip(namedarr,timing))

        if subject == 'Defence-GK-CA':
            for i,j in arr:
                if i == '1.1':
                    namedarr.append('General Science')
                    timing.append(j)
                if i == '1.2':
                    namedarr.append('Civics')
                    timing.append(j)
                if i == '1.3':
                    namedarr.append('Geography')
                    timing.append(j)
                if i == '1.4':
                    namedarr.append('Current Events')
                    timing.append(j)
                if i == '1.5':
                    namedarr.append('History')
                    timing.append(j)
                if i == '1.6':
                    namedarr.append('Basic Computer Operation')
                    timing.append(j)
                if i == '1.7':
                    namedarr.append('General Knowledge')
                    timing.append(j)

            return list(zip(namedarr,timing))



        if subject == 'GroupX-Maths':
            for i,j in arr:
                if i == '1.1':
                    namedarr.append('Sets-Relations-Functions')
                    timing.append(j)
                if i == '2.1':
                    namedarr.append('Trigonometric functions')
                    timing.append(j)
                if i == '3.1':
                    namedarr.append('Inverse Trigonometric functions')
                    timing.append(j)
                if i == '4.1':
                    namedarr.append('Complex numbers')
                    timing.append(j)
                if i == '5.1':
                    namedarr.append('Quadratic eqations')
                    timing.append(j)
                if i == '6.1':
                    namedarr.append('Sequence & Series')
                    timing.append(j)
                if i == '7.1':
                    namedarr.append('Permutations')
                    timing.append(j)
                if i == '8.1':
                    namedarr.append('Combination')
                    timing.append(j)
                if i == '9.1':
                    namedarr.append('Binomial Theorem')
                    timing.append(j)
                if i == '10.1':
                    namedarr.append('Coordinate Geometry')
                    timing.append(j)
                if i == '11.1':
                    namedarr.append('Exponential Series')
                    timing.append(j)
                if i == '12.1':
                    namedarr.append('Logarithmic Series')
                    timing.append(j)
                if i == '13.1':
                    namedarr.append('Matrices')
                    timing.append(j)
                if i == '14.1':
                    namedarr.append('Determinants')
                    timing.append(j)
                if i == '15.1':
                    namedarr.append('Limit & Continuity')
                    timing.append(j)
                if i == '16.1':
                    namedarr.append('Differentiation')
                    timing.append(j)
                if i == '17.1':
                    namedarr.append('Application of Differentiation')
                    timing.append(j)
                if i == '18.1':
                    namedarr.append('Indefinite Integrals')
                    timing.append(j)
                if i == '19.1':
                    namedarr.append('Definite Integrals')
                    timing.append(j)
                if i == '20.1':
                    namedarr.append('Application of Integration')
                    timing.append(j)
                if i == '21.1':
                    namedarr.append('Diferential Equations')
                    timing.append(j)
                if i == '22.1':
                    namedarr.append('Probability Statistics')
                    timing.append(j)
                if i == '23.1':
                    namedarr.append('Properties of Triangle')
                    timing.append(j)
                if i == '24.1':
                    namedarr.append('Height&Distance')
                    timing.append(j)


            return list(zip(namedarr,timing))

        if subject == 'MathsIITJEE10':
            for i,j in arr:
                if i == '1.1':
                    namedarr.append('All Categories')
                    timing.append(j)

            return list(zip(namedarr,timing))

        if subject == 'MathsIITJEE11':
            for i,j in arr:
                if i == '1.1':
                    namedarr.append('All Categories')
                    timing.append(j)

            return list(zip(namedarr,timing))

        if subject == 'MathsIITJEE12':
            for i,j in arr:
                if i == '1.1':
                    namedarr.append('All Categories')
                    timing.append(j)

            return list(zip(namedarr,timing))

        if subject == 'PhysicsIITJEE10':
            for i,j in arr:
                if i == '1.1':
                    namedarr.append('All Categories')
                    timing.append(j)

            return list(zip(namedarr,timing))

        if subject == 'PhysicsIITJEE11':
            for i,j in arr:
                if i == '1.1':
                    namedarr.append('All Categories')
                    timing.append(j)

            return list(zip(namedarr,timing))
        if subject == 'PhysicsIITJEE12':
            for i,j in arr:
                if i == '1.1':
                    namedarr.append('All Categories')
                    timing.append(j)

            return list(zip(namedarr,timing))

        if subject == 'ChemistryIITJEE10':
            for i,j in arr:
                if i == '1.1':
                    namedarr.append('All Categories')
                    timing.append(j)

            return list(zip(namedarr,timing))

        if subject == 'ChemistryIITJEE11':
            for i,j in arr:
                if i == '1.1':
                    namedarr.append('All Categories')
                    timing.append(j)

            return list(zip(namedarr,timing))

        if subject == 'ChemistryIITJEE12':
            for i,j in arr:
                if i == '1.1':
                    namedarr.append('All Categories')
                    timing.append(j)

            return list(zip(namedarr,timing))

        if subject == 'ElectricalLocoPilot':
            for i,j in arr:
                if i == '1.1':
                    namedarr.append('चालक,अचालक एवं कुचालक')
                    timing.append(j)
                if i == '2.1':
                    namedarr.append('बेसिक इलेक्ट्रिकल')
                    timing.append(j)
                if i == '3.1':
                    namedarr.append('विद्युत सेल')
                    timing.append(j)
                if i == '4.1':
                    namedarr.append('संधारित्र')
                    timing.append(j)
                if i == '5.1':
                    namedarr.append('चुम्बक')
                    timing.append(j)
                if i == '6.1':
                    namedarr.append('डी.सी.जनित्र')
                    timing.append(j)
                if i == '7.1':
                    namedarr.append('डी.सी.मोटर')
                    timing.append(j)
                if i == '8.1':
                    namedarr.append('ए.सी थ्योरी')
                    timing.append(j)
                if i == '9.1':
                    namedarr.append('भू-सम्पर्कन')
                    timing.append(j)
                if i == '10.1':
                    namedarr.append('विद्युय वायरिंग')
                    timing.append(j)
                if i == '11.1':
                    namedarr.append('विद्युत मापक यंत्र')
                    timing.append(j)
                if i == '12.1':
                    namedarr.append('ट्रांसफार्मर')
                    timing.append(j)
                if i == '13.1':
                    namedarr.append('प्रत्यावर्तक')
                    timing.append(j)
                if i == '14.1':
                    namedarr.append('तुल्यकालिक प्रेरण')
                    timing.append(j)
                if i == '15.1':
                    namedarr.append('ए.सी. मोटर')
                    timing.append(j)
                if i == '16.1':
                    namedarr.append('वाइंडिंग')
                    timing.append(j)
                if i == '17.1':
                    namedarr.append('विद्युत उत्पादन,ट्रांसमिशन एवं वितरण')
                    timing.append(j)
                if i == '18.1':
                    namedarr.append('प्रदीप्ति')
                    timing.append(j)
                if i == '19.1':
                    namedarr.append('इलेक्ट्रिक्स')
                    timing.append(j)
                if i == '20.1':
                    namedarr.append('व्यावसायिक एवं सावधानियां')
                    timing.append(j)

            return list(zip(namedarr,timing))



        if subject == 'FitterLocoPilot':
            for i,j in arr:
                if i == '1.1':
                    namedarr.append('Introduction')
                    timing.append(j)
                if i == '2.1':
                    namedarr.append('Fitter tools')
                    timing.append(j)
                if i == '3.1':
                    namedarr.append('Sheet Metal Shop')
                    timing.append(j)
                if i == '4.1':
                    namedarr.append('Welding Theory')
                    timing.append(j)
                if i == '5.1':
                    namedarr.append('Soldering And Brazing')
                    timing.append(j)
                if i == '6.1':
                    namedarr.append('Physical and Mechanical Properties of Metals')
                    timing.append(j)
                if i == '7.1':
                    namedarr.append('Heat Treatment')
                    timing.append(j)
                if i == '8.1':
                    namedarr.append('Bearings')
                    timing.append(j)
                if i == '9.1':
                    namedarr.append('Drilling Machine')
                    timing.append(j)
                if i == '10.1':
                    namedarr.append('Lathe Machine')
                    timing.append(j)
                if i == '11.1':
                    namedarr.append('Grinding Machine')
                    timing.append(j)
                if i == '12.1':
                    namedarr.append('Power Transmission')
                    timing.append(j)
                if i == '13.1':
                    namedarr.append('Pipe And Pipe Fitting')
                    timing.append(j)
                if i == '14.1':
                    namedarr.append('Screw Threads')
                    timing.append(j)
                if i == '15.1':
                    namedarr.append('Gauge')
                    timing.append(j)
                if i == '16.1':
                    namedarr.append('Limits,Fits And Tolerance')
                    timing.append(j)
                if i == '17.1':
                    namedarr.append('Other Important Questions')
                    timing.append(j)
                if i == '18.1':
                    namedarr.append('Previous Year Exams Questions')
                    timing.append(j)

            return list(zip(namedarr,timing))
        if subject == 'Civil_Loco_Pilot_Tech':
            for i,j in arr:
                if i == '2.1':
                    namedarr.append('Land Surveying Basic Principal And Classification')
                    timing.append(j)
                if i == '2.2':
                    namedarr.append('Chain Surveying')
                    timing.append(j)
                if i == '2.3':
                    namedarr.append('Compass Surveying')
                    timing.append(j)
                if i == '2.4':
                    namedarr.append('Levelling')
                    timing.append(j)
                if i == '2.5':
                    namedarr.append('Minor Instruments')
                    timing.append(j)
                if i == '2.6':
                    namedarr.append('Computation Of Land')
                    timing.append(j)
                if i == '2.7':
                    namedarr.append('Plane Table Survey')
                    timing.append(j)
                if i == '2.8':
                    namedarr.append('Contours And Contouring')
                    timing.append(j)
                if i == '2.9':
                    namedarr.append('Theodolite Survey')
                    timing.append(j)
                if i == '50.1':
                    namedarr.append('Curve And Curves Setting')
                    timing.append(j)
                if i == '12.1':
                    namedarr.append('Bending moment and sheer force')
                    timing.append(j)
                if i == '12.2':
                    namedarr.append('Bending and sheer stress')
                    timing.append(j)
                if i == '12.3':
                    namedarr.append('Combined direct and bending stress')
                    timing.append(j)
                if i == '12.4':
                    namedarr.append('Slope and deflection')
                    timing.append(j)
                if i == '12.5':
                    namedarr.append('Principal stress and principle planes')
                    timing.append(j)
                if i == '12.6':
                    namedarr.append('Columns and struts')
                    timing.append(j)
                if i == '12.7':
                    namedarr.append('Trosion')
                    timing.append(j)

                if i == '13.1':
                    namedarr.append('Rivet Connection')
                    timing.append(j)
                if i == '13.2':
                    namedarr.append('Weld Connection')
                    timing.append(j)
                if i == '13.3':
                    namedarr.append('Tension Members')
                    timing.append(j)
                if i == '13.4':
                    namedarr.append('Compression Member')
                    timing.append(j)
                if i == '13.5':
                    namedarr.append('Steel Beams')
                    timing.append(j)
                if i == '13.6':
                    namedarr.append('Column base and Foundation')
                    timing.append(j)
                if i == '13.7':
                    namedarr.append('Steel root of trusses')
                    timing.append(j)

            return list(zip(namedarr,timing))

        if subject == 'LocoPilot_Diesel':
            for i,j in arr:
                if i == '1.1':
                    namedarr.append('Introduction to Engine & Development')
                    timing.append(j)
                if i == '2.1':
                    namedarr.append('Cylinder Head & Valve Assembly')
                    timing.append(j)
                if i == '3.1':
                    namedarr.append('Piston & Connecting Rod')
                    timing.append(j)
                if i == '4.1':
                    namedarr.append('Crank Shaft,Cam Shaft Fly Wheel & Bearing')
                    timing.append(j)
                if i == '5.1':
                    namedarr.append('Gas Turbine Marine & Statonery Engine')
                    timing.append(j)
                if i == '6.1':
                    namedarr.append('Cooling & Snake System')
                    timing.append(j)
                if i == '7.1':
                    namedarr.append('Intake & Exhaust System')
                    timing.append(j)
                if i == '8.1':
                    namedarr.append('Diesel Fuel Supply System')
                    timing.append(j)
                if i == '9.1':
                    namedarr.append('Emission Charging & Starting System')
                    timing.append(j)
                if i == '10.1':
                    namedarr.append('Troubleshooting')
                    timing.append(j)

            return list(zip(namedarr,timing))


# for knimbus subjects
        if subject == 'Design and analysis of algorithm':
            for i,j in arr:
                if i == '1.1':
                    namedarr.append('Divide and Conquer')
                    timing.append(j)
                if i == '2.1':
                    namedarr.append('Dynamic Programming')
                    timing.append(j)
                if i == '3.1':
                    namedarr.append('Introduction')
                    timing.append(j)
                if i == '4.1':
                    namedarr.append('Greedy Method')
                    timing.append(j)

                return list(zip(namedarr,timing))

        if subject == 'CAT_Quantitative_Aptitude':
            for i,j in arr:
                if i == '11.1':
                    namedarr.append('Geometry')
                    timing.append(j)

                return list(zip(namedarr,timing))



    def convertTopicNumbersNames(self,arr,subject):
        namedarr = []
        if subject == 'English':
            for i in arr:
                if i == '1.1':
                    namedarr.append('Antonym')
                elif i == '1.2':
                    namedarr.append('Synonym')
                elif i == '1.3':
                    namedarr.append('One word substitution')
                elif i == '1.4':
                    namedarr.append('Idioms & Phrases')
                elif i == '1.5':
                    namedarr.append('Phrasal Verbs')
                elif i == '1.6':
                    namedarr.append('Use of some verbs with particular nouns')
                elif i == '1.7':
                    namedarr.append('Tense')
                elif i == '2.1':
                    namedarr.append('Noun')
                elif i == '2.2':
                    namedarr.append('Pronoun')
                elif i == '2.3':
                    namedarr.append('Adjective')
                elif i == '2.4':
                    namedarr.append('Articles')
                elif i == '2.5':
                    namedarr.append('Verb')
                elif i == '2.6':
                    namedarr.append('Adverb')
                elif i == '2.7':
                    namedarr.append('Time & Tense')
                elif i == '2.8':
                    namedarr.append('Voice')
                elif i == '2.9':
                    namedarr.append('Non-Finites')
                elif i == '3.1':
                    namedarr.append('Narration')
                elif i == '3.2':
                    namedarr.append('Preposition')
                elif i == '3.3':
                    namedarr.append('Conjunction')
                elif i == '3.4':
                    namedarr.append('Subject verb agreement')
                elif i == '3.5':
                    namedarr.append('Common Errors')
                elif i == '3.6':
                    namedarr.append('Superfluous Expressions & Slang')


            return namedarr
        if subject == 'General-Intelligence':
            for i in arr:
                if i == '1.1':
                    namedarr.append('Paper Cutting and Folding')
                elif i == '1.2':
                    namedarr.append('Mirror and Water Image')
                elif i == '1.3':
                    namedarr.append('Embedded Figures')
                elif i == '1.4':
                    namedarr.append('Figure Completion')
                elif i == '1.5':
                    namedarr.append('Counting Embedded Figures')
                elif i == '1.6':
                    namedarr.append('Counting in figures')
                elif i == '2.1':
                    namedarr.append('Analogy')
                elif i == '2.2':
                    namedarr.append('Multiple Analogy')
                elif i == '2.3':
                    namedarr.append('Choosing the analogous pair')
                elif i == '2.4':
                    namedarr.append('Number analogy (series pattern)')
                elif i =='2.5':
                    namedarr.append('Number analogy (missing)')
                elif i == '2.6':
                    namedarr.append('Alphabet based analogy')
                elif i == '2.7':
                    namedarr.append('Mixed analogy')
                elif i == '3.1':
                    namedarr.append('Series Completion (Diagram)')
                elif i == '3.2':
                    namedarr.append('Analogy (Diagram)')
                elif i == '3.3':
                    namedarr.append('Classification (Diagram)')
                elif i == '3.4':
                    namedarr.append('Dice & Boxes')
                elif i == '2.8':
                    namedarr.append('Ruled based analogy')
                elif i == '2.9':
                    namedarr.append('Alphabet Test')
                elif i == '4.1':
                    namedarr.append('Ranking')
                elif i == '5.1':
                    namedarr.append('Matrix')
                elif i == '6.1':
                    namedarr.append('Word Creation')
                elif i == '7.1':
                    namedarr.append('Odd one out')
                elif i == '8.1':
                    namedarr.append('Height')
                elif i == '9.1':
                    namedarr.append('Direction')
                elif i =='10.1':
                    namedarr.append('Statement & Conclusion')
                elif i == '11.1':
                    namedarr.append('Venn Diagram')
                elif i == '12.1':
                    namedarr.append('Missing number')
                elif i == '13.1':
                    namedarr.append('Logical Sequence of words')
                elif i == '14.1':
                    namedarr.append('Clock/Time')
                elif i == '15.1':
                    namedarr.append('Mathematical Operations')
                elif i == '16.1':
                    namedarr.append('Coding Decoding')
                elif i == '17.1':
                    namedarr.append('Series Test')
                elif i == '18.1':
                    namedarr.append('Syllogism')
                elif i == '19.1':
                    namedarr.append('Blood Relation')
                elif i == '20.1':
                    namedarr.append('Seating Arrangement')
                elif i == '22.1':
                    namedarr.append('Calender Test')
                elif i == '28.1':
                    namedarr.append('Symbols & Notations')


            return namedarr
        if subject == 'Quantitative-Analysis':

            for i in arr:

                if i == '1.1':
                    namedarr.append('Age')
                elif i == '2.1':
                    namedarr.append('Alligation')
                elif i == '3.1':
                    namedarr.append('Area')
                elif i == '4.1':
                    namedarr.append('Average')
                elif i == '5.1':
                    namedarr.append('Boat & Stream')
                elif i == '6.1':
                    namedarr.append('Discount')
                elif i == '7.1':
                    namedarr.append('Fraction')
                elif i == '8.1':
                    namedarr.append('LCM & LCF')
                elif i == '9.1':
                    namedarr.append('Number System')
                elif i == '10.1':
                    namedarr.append('Percentage')
                elif i == '11.1':
                    namedarr.append('Pipes & Cistern')
                elif i == '12.1':
                    namedarr.append('Profit & Loss')
                elif i == '13.1':
                    namedarr.append('Ratio')
                elif i == '14.1':
                    namedarr.append('Simple Interest')
                elif i == '15.1':
                    namedarr.append('Simplification')
                elif i == '16.1':
                    namedarr.append('Speed & Distance')
                elif i == '17.1':
                    namedarr.append('Square & Cube root')
                elif i == '18.1':
                    namedarr.append('Surds & Indices')
                elif i == '19.1':
                    namedarr.append('Time & Work')
                elif i == '20.1':
                    namedarr.append('Train')
                elif i == '21.1':
                    namedarr.append('Volume')
                elif i == '22.1':
                    namedarr.append('Trigonometry')
                elif i == '23.1':
                    namedarr.append('Partnership')
                elif i == '24.1':
                    namedarr.append('Compound Interest')
                elif i == '25.1':
                    namedarr.append('Decimals')



            return namedarr




        if subject == 'General-Knowledge':
            for i in arr:
                if i == '1.1':
                    namedarr.append('Inventions & Innovators')
                if i == '2.1':
                   namedarr.append('Bird Sanctuary')
                if i == '3.1':
                   namedarr.append('Books & Authors')
                if i == '4.1':
                   namedarr.append('Countries, Capitals & Currencies')
                if i == '5.1':
                   namedarr.append('Current Affairs')
                if i == '6.1':
                   namedarr.append('Economics')
                if i == '7.1':
                   namedarr.append('General Science')
                if i == '8.1':
                   namedarr.append('Biology')
                if i == '9.1':
                   namedarr.append('Chemistry')
                if i == '10.1':
                   namedarr.append('Science & Technology')
                if i == '11.1':
                   namedarr.append('Physics')
                if i == '12.1':
                   namedarr.append('Geography')
                if i == '13.1':
                   namedarr.append('National Organizations')
                if i == '14.1':
                   namedarr.append('History')
                if i == '15.1':
                   namedarr.append('Honors & Awards')
                if i == '16.1':
                   namedarr.append('Important Dates')
                if i == '17.1':
                   namedarr.append('Indian Agriculture')
                if i == '18.1':
                   namedarr.append('Indian Constitution')
                if i == '19.1':
                   namedarr.append('Indian Culture')
                if i == '20.1':
                   namedarr.append('Indian Museums')
                if i == '21.1':
                   namedarr.append('Polity (India)')
                if i == '22.1':
                   namedarr.append('Sports')
                if i == '23.1':
                   namedarr.append('Superlatives(India)')
                if i == '24.1':
                   namedarr.append('Symbols of States (India)')
                if i == '25.1':
                   namedarr.append('Tiger Reserve')
                if i == '26.1':
                   namedarr.append('UNESCO Word Heritage Sites(India)')
                if i == '27.1':
                   namedarr.append('World Organizations')
                if i == '28.1':
                   namedarr.append('Polity (World)')
            return namedarr

        if subject == 'General-Science':
            for i in arr:
                if i == '1.1':
                    namedarr.append('गुरूत्व स्थूल पदार्थ के गुण व प्रकाशन')
                if i == '2.1':
                    namedarr.append('लेंस व दर्पण')
                if i == '3.1':
                    namedarr.append('आधुनिक भौतिकी')
                if i == '4.1':
                    namedarr.append('विमिय तथा द्विविमिय')
                if i == '5.1':
                    namedarr.append('कॉमन प्रश्नपत्र भौतिक शास्त्रा')
                if i == '6.1':
                    namedarr.append('दाब घटाव प्रत्यासा')
                if i == '7.1':
                    namedarr.append('ध्वनि')
                if i == '8.1':
                    namedarr.append('मात्रक विभाएं मापन')
                if i == '9.1':
                    namedarr.append('सदिश तथा अदिश')
                if i == '10.1':
                    namedarr.append('कार्य,ऊर्जा व शक्ति')
                if i == '11.1':
                    namedarr.append('कोशिका विज्ञान')
                if i == '12.1':
                    namedarr.append('पादप जगत')
                if i == '13.1':
                    namedarr.append('पादप शरीर क्रिया विज्ञान')
                if i == '14.1':
                    namedarr.append('आर्थिक वनस्पति विज्ञान')
                if i == '15.1':
                    namedarr.append('जन्तु विज्ञान')
                if i == '16.1':
                    namedarr.append('जन्तु उत्तक एवं पोषण')
                if i == '17.1':
                    namedarr.append('आनुवांशिक')
                if i == '18.1':
                    namedarr.append('मानव स्वास्थ्य एवं रोग')
                if i == '19.1':
                    namedarr.append('जैव प्रोद्यौगिक')
                if i == '20.1':
                    namedarr.append('कम्प्यूटर एवं सूचना प्रोद्यौगिकी')

            return namedarr

# group x subjects

        if subject == 'Defence-English':
            for i in arr:
                if i == '1.1':
                    namedarr.append('Comprehension')
                if i == '2.1':
                    namedarr.append('Judge Comprehension')
                if i == '3.1':
                    namedarr.append('Inferences')
                if i == '4.1':
                    namedarr.append('Vocabulary')
                if i == '5.1':
                    namedarr.append('Composition')
                if i == '6.1':
                    namedarr.append('Subject and Verb')
                if i == '7.1':
                    namedarr.append('Verb and their use')
                if i == '8.1':
                    namedarr.append('Sequence of tenses')
                if i == '9.1':
                    namedarr.append('Transformation')
                if i == '10.1':
                    namedarr.append('Grammer')
                if i == '11.1':
                    namedarr.append('Spellings')
                if i == '12.1':
                    namedarr.append('Word formation')
                if i == '11.1':
                    namedarr.append('Antonyms& Synonyms')
                if i == '11.1':
                    namedarr.append('Word Substitution')
                if i == '12.1':
                    namedarr.append('Correct use of words')
                if i == '13.1':
                    namedarr.append('Confusing words')
                if i == '14.1':
                    namedarr.append('Word order')
                if i == '15.1':
                    namedarr.append('Correct use of Adverbs')
                if i == '16.1':
                    namedarr.append('Idioms and Phrases')
                if i == '17.1':
                    namedarr.append('Use of simple idioms')
                if i == '18.1':
                    namedarr.append('Use of common proverbs')
                if i == '19.1':
                    namedarr.append('Direct/Indirect sentences')
                if i == '20.1':
                    namedarr.append('Direct to Indirect form')
                if i == '21.1':
                    namedarr.append('Indirect to Direct')
                if i == '22.1':
                    namedarr.append('Active and Passive voice')
                if i == '23.1':
                    namedarr.append('Active to Passive voice')
                if i == '22.1':
                    namedarr.append('Passive to Active voice')
                if i == '50.1':
                    namedarr.append('To be categorized')

            return namedarr

        if subject == 'Defence-Physics':
            for i in arr:
                if i == '1.1':
                    namedarr.append('Unit of Dimension')
                if i == '2.1':
                    namedarr.append('Scalers&Vectors')
                if i == '3.1':
                    namedarr.append('Motion in straight line')
                if i == '4.1':
                    namedarr.append('Law of Motion')
                if i == '5.1':
                    namedarr.append('Projectile Motion')
                if i == '6.1':
                    namedarr.append('Circular Motion')
                if i == '7.1':
                    namedarr.append('Friction ')
                if i == '8.1':
                    namedarr.append('Work power & Energy')
                if i == '9.1':
                    namedarr.append('Collision')
                if i == '10.1':
                    namedarr.append('Rotational motion % Moment of Inertia')
                if i == '11.1':
                    namedarr.append('Gravitation')
                if i == '12.1':
                    namedarr.append('Elasticity')
                if i == '13.1':
                    namedarr.append('Fluid Pressure ')
                if i == '14.1':
                    namedarr.append('Viscocity& Flow of fluids')
                if i == '15.1':
                    namedarr.append('Surface Tension')
                if i == '16.1':
                    namedarr.append('Oscillations')
                if i == '17.1':
                    namedarr.append('Thermometry')
                if i == '18.1':
                    namedarr.append('Thermal Expansion')
                if i == '19.1':
                    namedarr.append('Calorimetry')
                if i == '20.1':
                    namedarr.append('Transmission of Heat')
                if i == '21.1':
                    namedarr.append('Thermodynamics')
                if i == '22.1':
                    namedarr.append('Kinetic Theory of gases')
                if i == '23.1':
                    namedarr.append('Wave Motion')
                if i == '24.1':
                    namedarr.append('Superposition of waves')
                if i == '25.1':
                    namedarr.append('Speed of Sound')
                if i == '26.1':
                    namedarr.append('Vibrations in air columns')
                if i == '27.1':
                    namedarr.append('Vibration of Strings')
                if i == '28.1':
                    namedarr.append('Dopplers Effect')
                if i == '29.1':
                    namedarr.append('Musical Sound& Ultra sound')
                if i == '30.1':
                    namedarr.append('Electric charge & Electric Field')
                if i == '31.1':
                    namedarr.append('Gauss Theorem')
                if i == '32.1':
                    namedarr.append('Electric Capacitance')
                if i == '33.1':
                    namedarr.append('Electric Conduction')
                if i == '34.1':
                    namedarr.append('Ohms Law')
                if i == '35.1':
                    namedarr.append('Electromotive force & Electric cell')
                if i == '36.1':
                    namedarr.append('Kirchoffs law & wheatstone bridge')
                if i == '37.1':
                    namedarr.append('Potentiometer')
                if i == '38.1':
                    namedarr.append('Heating effect of current')
                if i == '39.1':
                    namedarr.append('Chemical effect of current')
                if i == '40.1':
                    namedarr.append('Magnetic effect of current')
                if i == '41.1':
                    namedarr.append('Electrical Instruments')
                if i == '42.1':
                    namedarr.append('Magnetic Field')
                if i == '43.1':
                    namedarr.append('Magnetic effects of matter & terrestrial\
                                    magnetism')
                if i == '44.1':
                    namedarr.append('Electromagnetic Induction')
                if i == '45.1':
                    namedarr.append('Alternating Current')
                if i == '46.1':
                    namedarr.append('Reflection of light')
                if i == '47.1':
                    namedarr.append('Refraction of light')
                if i == '48.1':
                    namedarr.append('Refraction at Spherical surface & by\
                                    lenses')
                if i == '49.1':
                    namedarr.append('Prism & scattering of light')
                if i == '50.1':
                    namedarr.append('Optical instruments')
                if i == '51.1':
                    namedarr.append('Human eye & defects of vision')
                if i == '52.1':
                    namedarr.append('Wave theory of light')
                if i == '53.1':
                    namedarr.append('Interferance & Deflection of light')
                if i == '54.1':
                    namedarr.append('Polarization of light')
                if i == '55.1':
                    namedarr.append('Photometry')
                if i == '56.1':
                    namedarr.append('Dual nature of radiation & matter')
                if i == '57.1':
                    namedarr.append('Electromagnetic waves')
                if i == '58.1':
                    namedarr.append('Structure of Atom')
                if i == '59.1':
                    namedarr.append('Radioactivity')
                if i == '60.1':
                    namedarr.append('Nuclear fission & fusion')
                if i == '61.1':
                    namedarr.append('Semi-conductor,diode & Transistors')
                if i == '62.1':
                    namedarr.append('Digital electronics & logic gates')

            return namedarr

        if subject == 'Defence-GK-CA':
            for i in arr:
                if i == '1.1':
                    namedarr.append('General Science')
                if i == '1.2':
                    namedarr.append('Civics')
                if i == '1.3':
                    namedarr.append('Geography')
                if i == '1.4':
                    namedarr.append('Current Events')
                if i == '1.5':
                    namedarr.append('History')
                if i == '1.6':
                    namedarr.append('Basic Computer Operation')
                if i == '1.7':
                    namedarr.append('General Knowledge')

            return namedarr



        if subject == 'GroupX-Maths':
            for i in arr:
                if i == '1.1':
                    namedarr.append('Sets-Relations-Functions')
                if i == '2.1':
                    namedarr.append('Trigonometric functions')
                if i == '3.1':
                    namedarr.append('Inverse Trigonometric functions')
                if i == '4.1':
                    namedarr.append('Complex numbers')
                if i == '5.1':
                    namedarr.append('Quadratic eqations')
                if i == '6.1':
                    namedarr.append('Sequence & Series')
                if i == '7.1':
                    namedarr.append('Permutations')
                if i == '8.1':
                    namedarr.append('Combination')
                if i == '9.1':
                    namedarr.append('Binomial Theorem')
                if i == '10.1':
                    namedarr.append('Coordinate Geometry')
                if i == '11.1':
                    namedarr.append('Exponential Series')
                if i == '12.1':
                    namedarr.append('Logarithmic Series')
                if i == '13.1':
                    namedarr.append('Matrices')
                if i == '14.1':
                    namedarr.append('Determinants')
                if i == '15.1':
                    namedarr.append('Limit & Continuity')
                if i == '16.1':
                    namedarr.append('Differentiation')
                if i == '17.1':
                    namedarr.append('Application of Differentiation')
                if i == '18.1':
                    namedarr.append('Indefinite Integrals')
                if i == '19.1':
                    namedarr.append('Definite Integrals')
                if i == '20.1':
                    namedarr.append('Application of Integration')
                if i == '21.1':
                    namedarr.append('Diferential Equations')
                if i == '22.1':
                    namedarr.append('Probability Statistics')
                if i == '23.1':
                    namedarr.append('Properties of Triangle')
                if i == '24.1':
                    namedarr.append('Height&Distance')



            return namedarr
        if subject == 'MathsIITJEE10':
            for i in arr:
                if i == '1.1':
                    namedarr.append('All Categories')
            return namedarr

        if subject == 'MathsIITJEE11':
            for i in arr:
                if i == '1.1':
                    namedarr.append('All Categories')
            return namedarr

        if subject == 'MathsIITJEE12':
            for i in arr:
                if i == '1.1':
                    namedarr.append('All Categories')
            return namedarr

        if subject == 'PhysicsIITJEE10':
            for i in arr:
                if i == '1.1':
                    namedarr.append('All Categories')
            return namedarr

        if subject == 'PhysicsIITJEE11':
            for i in arr:
                if i == '1.1':
                    namedarr.append('All Categories')
            return namedarr

        if subject == 'PhysicsIITJEE12':
            for i in arr:
                if i == '1.1':
                    namedarr.append('All Categories')
            return namedarr

        if subject == 'ChemistryIITJEE10':
            for i in arr:
                if i == '1.1':
                    namedarr.append('All Categories')
            return namedarr

        if subject == 'ChemistryIITJEE11':
            for i in arr:
                if i == '1.1':
                    namedarr.append('All Categories')
            return namedarr

        if subject == 'ChemistryIITJEE12':
            for i in arr:
                if i == '1.1':
                    namedarr.append('All Categories')
            return namedarr
# for locopilot subjects
        if subject == 'ElectricalLocoPilot':
            for i in arr:
                if i == '1.1':
                    namedarr.append('चालक,अचालक एवं कुचालक')
                if i == '2.1':
                    namedarr.append('बेसिक इलेक्ट्रिकल')
                if i == '3.1':
                    namedarr.append('विद्युत सेल')
                if i == '4.1':
                    namedarr.append('संधारित्र')
                if i == '5.1':
                    namedarr.append('चुम्बक')
                if i == '6.1':
                    namedarr.append('डी.सी.जनित्र')
                if i == '7.1':
                    namedarr.append('डी.सी.मोटर')
                if i == '8.1':
                    namedarr.append('ए.सी थ्योरी')
                if i == '9.1':
                    namedarr.append('भू-सम्पर्कन')
                if i == '10.1':
                    namedarr.append('विद्युय वायरिंग')
                if i == '11.1':
                    namedarr.append('विद्युत मापक यंत्र')
                if i == '12.1':
                    namedarr.append('ट्रांसफार्मर')
                if i == '13.1':
                    namedarr.append('प्रत्यावर्तक')
                if i == '14.1':
                    namedarr.append('तुल्यकालिक प्रेरण')
                if i == '15.1':
                    namedarr.append('ए.सी. मोटर')
                if i == '16.1':
                    namedarr.append('वाइंडिंग')
                if i == '17.1':
                    namedarr.append('विद्युत उत्पादन,ट्रांसमिशन एवं वितरण')
                if i == '18.1':
                    namedarr.append('प्रदीप्ति')
                if i == '19.1':
                    namedarr.append('इलेक्ट्रिक्स')
                if i == '20.1':
                    namedarr.append('व्यावसायिक एवं सावधानियां')

            return namedarr


        if subject == 'FitterLocoPilot':
            for i in arr:
                if i == '1.1':
                    namedarr.append('Introduction')

                if i == '2.1':
                    namedarr.append('Fitter tools')

                if i == '3.1':
                    namedarr.append('Sheet Metal Shop')

                if i == '4.1':
                    namedarr.append('Welding Theory')

                if i == '5.1':
                    namedarr.append('Soldering And Brazing')
                if i == '6.1':
                    namedarr.append('Physical and Mechanical Properties of Metals')
                if i == '7.1':
                    namedarr.append('Heat Treatment')
                if i == '8.1':
                    namedarr.append('Bearings')
                if i == '9.1':
                    namedarr.append('Drilling Machine')
                if i == '10.1':
                    namedarr.append('Lathe Machine')
                if i == '11.1':
                    namedarr.append('Grinding Machine')
                if i == '12.1':
                    namedarr.append('Power Transmission')
                if i == '13.1':
                    namedarr.append('Pipe And Pipe Fitting')
                if i == '14.1':
                    namedarr.append('Screw Threads')
                if i == '15.1':
                    namedarr.append('Gauge')
                if i == '16.1':
                    namedarr.append('Limits,Fits And Tolerance')
                if i == '17.1':
                    namedarr.append('Other Important Questions')
                if i == '18.1':
                    namedarr.append('Previous Year Exams Questions')

            return namedarr

        if subject == 'Civil_Loco_Pilot_Tech':
            for i in arr:
                if i == '2.1':
                    namedarr.append('Land Surveying Basic Principal And Classification')

                if i == '2.2':
                    namedarr.append('Chain Surveying')

                if i == '2.3':
                    namedarr.append('Compass Surveying')

                if i == '2.4':
                    namedarr.append('Levelling')

                if i == '2.5':
                    namedarr.append('Minor Instruments')

                if i == '2.6':
                    namedarr.append('Computation Of Land')

                if i == '2.7':
                    namedarr.append('Plane Table Survey')

                if i == '2.8':
                    namedarr.append('Contours And Contouring')

                if i == '2.9':
                    namedarr.append('Theodolite Survey')

                if i == '50.1':
                    namedarr.append('Curve And Curves Setting')
                if i == '12.1':
                    namedarr.append('Bending moment and sheer force')
                if i == '12.2':
                    namedarr.append('Bending and sheer stress')
                if i == '12.3':
                    namedarr.append('Combined direct and bending stress')
                if i == '12.4':
                    namedarr.append('Slope and deflection')
                if i == '12.5':
                    namedarr.append('Principal stress and principle planes')
                if i == '12.6':
                    namedarr.append('Columns and struts')
                if i == '12.7':
                    namedarr.append('Trosion')

                if i == '13.1':
                    namedarr.append('Rivet Connection')
                if i == '13.2':
                    namedarr.append('Weld Connection')
                if i == '13.3':
                    namedarr.append('Tension Members')
                if i == '13.4':
                    namedarr.append('Compression Member')
                if i == '13.5':
                    namedarr.append('Steel Beams')
                if i == '13.6':
                    namedarr.append('Column base and Foundation')
                if i == '13.7':
                    namedarr.append('Steel root of trusses')



            return namedarr
        if subject == 'LocoPilot_Diesel':
            for i in arr:
                if i == '1.1':
                    namedarr.append('Introduction to Engine & Development')
                if i == '2.1':
                    namedarr.append('Cylinder Head & Valve Assembly')
                if i == '3.1':
                    namedarr.append('Piston & Connecting Rod')
                if i == '4.1':
                    namedarr.append('Crank Shaft,Cam Shaft Fly Wheel & Bearing')
                if i == '5.1':
                    namedarr.append('Gas Turbine Marine & Statonery Engine')
                if i == '6.1':
                    namedarr.append('Cooling & Snake System')
                if i == '7.1':
                    namedarr.append('Intake & Exhaust System')
                if i == '8.1':
                    namedarr.append('Diesel Fuel Supply System')
                if i == '9.1':
                    namedarr.append('Emission Charging & Starting System')
                if i == '10.1':
                    namedarr.append('Troubleshooting')

            return list(zip(names,numbers))


# for knimbus subjects
        if subject == 'Design and analysis of algorithm':
            for i in arr:
                if i == '1.1':
                    namedarr.append('Divide and Conquer')
                if i == '2.1':
                    namedarr.append('Dynamic Programming')
                if i == '3.1':
                    namedarr.append('Introduction')
                if i == '4.1':
                    namedarr.append('Greedy Method')

                return namedarr

        if subject == 'CAT_Quantitative_Aptitude':
            for i in arr:
                if i == '11.1':
                    namedarr.append('Geometry')

                return namedarr


    def changeIndividualNames(self,i,subject):
        if subject == 'English':
            if i == '1.1':
                return 'Antonym'
            elif i == '1.2':
                return 'Synonym'
            elif i == '1.3':
                return 'One word substitution'
            elif i == '1.4':
                return 'Idioms & Phrases'
            elif i == '1.5':
                return 'Phrasal Verbs'
            elif i == '1.6':
                return 'Use of some verbs with particular nouns'
            elif i == '1.7':
                return 'Tense'
            elif i == '2.1':
                return 'Noun'
            elif i == '2.2':
                return 'Pronoun'
            elif i == '2.3':
                return 'Adjective'
            elif i == '2.4':
                return 'Articles'
            elif i == '2.5':
                return 'Verb'
            elif i == '2.6':
                return 'Adverb'
            elif i == '2.7':
                return 'Time & Tense'
            elif i == '2.8':
                return 'Voice'
            elif i == '2.9':
                return 'Non-Finites'
            elif i == '3.1':
                return 'Narration'
            elif i == '3.2':
                return 'Preposition'
            elif i == '3.3':
                return 'Conjunction'
            elif i == '3.4':
                return 'Subject verb agreement'
            elif i == '3.5':
                return 'Common Errors'
            elif i == '3.6':
                return 'Superfluous Expressions & Slang'



        if subject == 'General-Intelligence':
            if i == '1.1':
                return 'Paper Cutting and Folding'
            elif i == '1.2':
                return 'Mirror and Water Image'
            elif i == '1.3':
                return 'Embedded Figures'
            elif i == '1.4':
                return 'Figure Completion'
            elif i == '1.5':
                return 'Counting Embedded Figures'
            elif i == '1.6':
                return 'Counting in figures'
            elif i == '2.1':
                return 'Analogy'
            elif i == '2.2':
                return 'Multiple Analogy'
            elif i == '2.3':
                return 'Choosing the analogous pair'
            elif i == '2.4':
                return 'Number analogy (series pattern)'
            elif i =='2.5':
                return 'Number analogy (missing)'
            elif i == '2.6':
                return 'Alphabet based analogy'
            elif i == '2.7':
                return 'Mixed analogy'
            elif i == '3.1':
                return 'Series Completion (Diagram)'
            elif i == '3.2':
                return 'Analogy (Diagram)'
            elif i == '3.3':
                return 'Classification (Diagram)'
            elif i == '3.4':
                return 'Dice & Boxes'
            elif i == '2.8':
                return 'Ruled based analogy'
            elif i == '2.9':
                return 'Alphabet Test'
            elif i == '4.1':
                return 'Ranking'
            elif i == '5.1':
                return 'Matrix'
            elif i == '6.1':
                return 'Word Creation'
            elif i == '7.1':
                return 'Odd one out'
            elif i == '8.1':
                return 'Height'
            elif i == '9.1':
                return 'Direction'
            elif i =='10.1':
                return 'Statement & Conclusion'
            elif i == '11.1':
                return 'Venn Diagram'
            elif i == '12.1':
                return 'Missing number'
            elif i == '13.1':
                return 'Logical Sequence of words'
            elif i == '14.1':
                return 'Clock/Time'
            elif i == '15.1':
                return 'Mathematical Operations'
            elif i == '16.1':
                return 'Coding Decoding'
            elif i == '17.1':
                return 'Series Test'
            elif i == '18.1':
                return 'Syllogism'
            elif i == '19.1':
                return 'Blood Relation'
            elif i == '20.1':
                return 'Seating Arrangement'
            elif i == '22.1':
                return 'Calender Test'
            elif i == '28.1':
                return 'Symbols & Notations'












        if subject == 'Quantitative-Analysis':
                if i == '1.1':
                    return 'Age'
                elif i == '2.1':
                    return 'Alligation'
                elif i == '3.1':
                    return 'Area'
                elif i == '4.1':
                    return 'Average'
                elif i == '5.1':
                    return 'Boat & Stream'
                elif i == '6.1':
                    return 'Discount'
                elif i == '7.1':
                    return 'Fraction'
                elif i == '8.1':
                    return 'LCM & LCF'
                elif i == '9.1':
                    return 'Number System'
                elif i == '10.1':
                    return 'Percentage'
                elif i == '11.1':
                    return 'Pipes & Cistern'
                elif i == '12.1':
                    return 'Profit & Loss'
                elif i == '13.1':
                    return 'Ratio'
                elif i == '14.1':
                    return 'Simple Interest'
                elif i == '15.1':
                    return 'Simplification'
                elif i == '16.1':
                    return 'Speed & Distance'
                elif i == '17.1':
                    return 'Square & Cube root'
                elif i == '18.1':
                    return 'Surds & Indices'
                elif i == '19.1':
                    return 'Time & Work'
                elif i == '20.1':
                    return 'Train'
                elif i == '21.1':
                    return 'Volume'
                elif i == '22.1':
                    return 'Trigonometry'
                elif i == '23.1':
                    return 'Partnership'
                elif i == '24.1':
                    return 'Compound Interest'
                elif i == '25.1':
                    return 'Decimals'


        if subject == 'General-Knowledge':
                if i == '1.1':
                    return 'Inventions & Innovators'
                if i == '2.1':
                   return 'Bird Sanctuary'
                if i == '3.1':
                   return 'Books & Authors'
                if i == '4.1':
                   return 'Countries, Capitals & Currencies'
                if i == '5.1':
                   return 'Current Affairs'
                if i == '6.1':
                   return 'Economics'
                if i == '7.1':
                   return 'General Science'
                if i == '8.1':
                   return 'Biology'
                if i == '9.1':
                   return 'Chemistry'
                if i == '10.1':
                   return 'Science & Technology'
                if i == '11.1':
                   return 'Physics'
                if i == '12.1':
                   return 'Geography'
                if i == '13.1':
                   return 'National Organizations'
                if i == '14.1':
                   return 'History'
                if i == '15.1':
                   return 'Honors & Awards'
                if i == '16.1':
                   return 'Important Dates'
                if i == '17.1':
                   return 'Indian Agriculture'
                if i == '18.1':
                   return 'Indian Constitution'
                if i == '19.1':
                   return 'Indian Culture'
                if i == '20.1':
                   return 'Indian Museums'
                if i == '21.1':
                   return 'Polity (India)'
                if i == '22.1':
                   return 'Sports'
                if i == '23.1':
                   return 'Superlatives(India)'
                if i == '24.1':
                   return 'Symbols of States (India)'
                if i == '25.1':
                   return 'Tiger Reserve'
                if i == '26.1':
                   return 'UNESCO Word Heritage Sites(India)'
                if i == '27.1':
                   return 'World Organizations'
                if i == '28.1':
                   return 'Polity (World)'

        if subject == 'General-Science':
                if i == '1.1':
                    return 'गुरूत्व स्थूल पदार्थ के गुण व प्रकाशन'
                if i == '2.1':
                    return 'लेंस व दर्पण'
                if i == '3.1':
                    return 'आधुनिक भौतिकी'
                if i == '4.1':
                    return 'विमिय तथा द्विविमिय'
                if i == '5.1':
                    return 'कॉमन प्रश्नपत्र भौतिक शास्त्रा'
                if i == '6.1':
                    return 'दाब घटाव प्रत्यासा'
                if i == '7.1':
                    return 'ध्वनि'
                if i == '8.1':
                    return 'मात्रक विभाएं मापन'
                if i == '9.1':
                    return 'सदिश तथा अदिश'
                if i == '10.1':
                    return 'कार्य,ऊर्जा व शक्ति'
                if i == '11.1':
                    return 'कोशिका विज्ञान'
                if i == '12.1':
                    return 'पादप जगत'
                if i == '13.1':
                    return 'पादप शरीर क्रिया विज्ञान'
                if i == '14.1':
                    return 'आर्थिक वनस्पति विज्ञान'
                if i == '15.1':
                    return 'जन्तु विज्ञान'
                if i == '16.1':
                    return 'जन्तु उत्तक एवं पोषण'
                if i == '17.1':
                    return 'आनुवांशिक'
                if i == '18.1':
                    return 'मानव स्वास्थ्य एवं रोग'
                if i == '19.1':
                    return 'जैव प्रोद्यौगिक'
                if i == '20.1':
                    return 'कम्प्यूटर एवं सूचना प्रोद्यौगिकी'



# group x subjects

        if subject == 'Defence-English':
                if i == '1.1':
                    return 'Comprehension'
                if i == '2.1':
                    return 'Judge Comprehension'
                if i == '3.1':
                    return 'Inferences'
                if i == '4.1':
                    return 'Vocabulary'
                if i == '5.1':
                    return 'Composition'
                if i == '6.1':
                    return 'Subject and Verb'
                if i == '7.1':
                    return 'Verb and their use'
                if i == '8.1':
                    return 'Sequence of tenses'
                if i == '9.1':
                    return 'Transformation'
                if i == '10.1':
                    return 'Grammer'
                if i == '11.1':
                    return 'Spellings'
                if i == '12.1':
                    return 'Word formation'
                if i == '11.1':
                    return 'Antonyms& Synonyms'
                if i == '11.1':
                    return 'Word Substitution'
                if i == '12.1':
                    return 'Correct use of words'
                if i == '13.1':
                    return 'Confusing words'
                if i == '14.1':
                    return 'Word order'
                if i == '15.1':
                    return 'Correct use of Adverbs'
                if i == '16.1':
                    return 'Idioms and Phrases'
                if i == '17.1':
                    return 'Use of simple idioms'
                if i == '18.1':
                    return 'Use of common proverbs'
                if i == '19.1':
                    return 'Direct/Indirect sentences'
                if i == '20.1':
                    return 'Direct to Indirect form'
                if i == '21.1':
                    return 'Indirect to Direct'
                if i == '22.1':
                    return 'Active and Passive voice'
                if i == '23.1':
                    return 'Active to Passive voice'
                if i == '22.1':
                    return 'Passive to Active voice'
                if i == '50.1':
                    return 'To be categorized'


        if subject == 'Defence-Physics':
                if i == '1.1':
                    return 'Unit of Dimension'
                if i == '2.1':
                    return 'Scalers&Vectors'
                if i == '3.1':
                    return 'Motion in straight line'
                if i == '4.1':
                    return 'Law of Motion'
                if i == '5.1':
                    return 'Projectile Motion'
                if i == '6.1':
                    return 'Circular Motion'
                if i == '7.1':
                    return 'Friction '
                if i == '8.1':
                    return 'Work power & Energy'
                if i == '9.1':
                    return 'Collision'
                if i == '10.1':
                    return 'Rotational motion % Moment of Inertia'
                if i == '11.1':
                    return 'Gravitation'
                if i == '12.1':
                    return 'Elasticity'
                if i == '13.1':
                    return 'Fluid Pressure '
                if i == '14.1':
                    return 'Viscocity& Flow of fluids'
                if i == '15.1':
                    return 'Surface Tension'
                if i == '16.1':
                    return 'Oscillations'
                if i == '17.1':
                    return 'Thermometry'
                if i == '18.1':
                    return 'Thermal Expansion'
                if i == '19.1':
                    return 'Calorimetry'
                if i == '20.1':
                    return 'Transmission of Heat'
                if i == '21.1':
                    return 'Thermodynamics'
                if i == '22.1':
                    return 'Kinetic Theory of gases'
                if i == '23.1':
                    return 'Wave Motion'
                if i == '24.1':
                    return 'Superposition of waves'
                if i == '25.1':
                    return 'Speed of Sound'
                if i == '26.1':
                    return 'Vibrations in air columns'
                if i == '27.1':
                    return 'Vibration of Strings'
                if i == '28.1':
                    return 'Dopplers Effect'
                if i == '29.1':
                    return 'Musical Sound& Ultra sound'
                if i == '30.1':
                    return 'Electric charge & Electric Field'
                if i == '31.1':
                    return 'Gauss Theorem'
                if i == '32.1':
                    return 'Electric Capacitance'
                if i == '33.1':
                    return 'Electric Conduction'
                if i == '34.1':
                    return 'Ohms Law'
                if i == '35.1':
                    return 'Electromotive force & Electric cell'
                if i == '36.1':
                    return 'Kirchoffs law & wheatstone bridge'
                if i == '37.1':
                    return 'Potentiometer'
                if i == '38.1':
                    return 'Heating effect of current'
                if i == '39.1':
                    return 'Chemical effect of current'
                if i == '40.1':
                    return 'Magnetic effect of current'
                if i == '41.1':
                    return 'Electrical Instruments'
                if i == '42.1':
                    return 'Magnetic Field'
                if i == '43.1':
                    return 'Magnetic effects of matter & terrestrial\
                                    magnetism'
                if i == '44.1':
                    return 'Electromagnetic Induction'
                if i == '45.1':
                    return 'Alternating Current'
                if i == '46.1':
                    return 'Reflection of light'
                if i == '47.1':
                    return 'Refraction of light'
                if i == '48.1':
                    return 'Refraction at Spherical surface & by\
                                    lenses'
                if i == '49.1':
                    return 'Prism & scattering of light'
                if i == '50.1':
                    return 'Optical instruments'
                if i == '51.1':
                    return 'Human eye & defects of vision'
                if i == '52.1':
                    return 'Wave theory of light'
                if i == '53.1':
                    return 'Interferance & Deflection of light'
                if i == '54.1':
                    return 'Polarization of light'
                if i == '55.1':
                    return 'Photometry'
                if i == '56.1':
                    return 'Dual nature of radiation & matter'
                if i == '57.1':
                    return 'Electromagnetic waves'
                if i == '58.1':
                    return 'Structure of Atom'
                if i == '59.1':
                    return 'Radioactivity'
                if i == '60.1':
                    return 'Nuclear fission & fusion'
                if i == '61.1':
                    return 'Semi-conductor,diode & Transistors'
                if i == '62.1':
                    return 'Digital electronics & logic gates'
        if subject == 'Defence-GK-CA':
                if i == '1.1':
                    return 'General Science'
                if i == '1.2':
                    return 'Civics'
                if i == '1.3':
                    return 'Geography'
                if i == '1.4':
                    return 'Current Events'
                if i == '1.5':
                    return 'History'
                if i == '1.6':
                    return 'Basic Computer Operation'
                if i == '1.7':
                    return 'General Knowledge'








        if subject == 'GroupX-Maths':
                if i == '1.1':
                    return 'Sets-Relations-Functions'
                if i == '2.1':
                    return 'Trigonometric functions'
                if i == '3.1':
                    return 'Inverse Trigonometric functions'
                if i == '4.1':
                    return 'Complex numbers'
                if i == '5.1':
                    return 'Quadratic eqations'
                if i == '6.1':
                    return 'Sequence & Series'
                if i == '7.1':
                    return 'Permutations'
                if i == '8.1':
                    return 'Combination'
                if i == '9.1':
                    return 'Binomial Theorem'
                if i == '10.1':
                    return 'Coordinate Geometry'
                if i == '11.1':
                    return 'Exponential Series'
                if i == '12.1':
                    return 'Logarithmic Series'
                if i == '13.1':
                    return 'Matrices'
                if i == '14.1':
                    return 'Determinants'
                if i == '15.1':
                    return 'Limit & Continuity'
                if i == '16.1':
                    return 'Differentiation'
                if i == '17.1':
                    return 'Application of Differentiation'
                if i == '18.1':
                    return 'Indefinite Integrals'
                if i == '19.1':
                    return 'Definite Integrals'
                if i == '20.1':
                    return 'Application of Integration'
                if i == '21.1':
                    return 'Diferential Equations'
                if i == '22.1':
                    return 'Probability Statistics'
                if i == '23.1':
                    return 'Properties of Triangle'
                if i == '24.1':
                    return 'Height&Distance'

        if subject == 'MathsIITJEE10':
            if i == '1.1':
                return 'All Categories'


        if subject == 'MathsIITJEE11':
                if i == '1.1':
                    return 'All Categories'


        if subject == 'MathsIITJEE12':
            if i == '1.1':
                return 'All Categories'


        if subject == 'PhysicsIITJEE10':
                if i == '1.1':
                    return 'All Categories'


        if subject == 'PhysicsIITJEE11':
            if i == '1.1':
                return 'All Categories'

        if subject == 'PhysicsIITJEE12':
                if i == '1.1':
                    return 'All Categories'


        if subject == 'ChemistryIITJEE10':
            if i == '1.1':
                return 'All Categories'


        if subject == 'ChemistryIITJEE11':
                if i == '1.1':
                    return 'All Categories'

        if subject == 'ChemistryIITJEE12':
                if i == '1.1':
                    return 'All Categories'

    # for locopilot
        if subject == 'ElectricalLocoPilot':
                if i == '1.1':
                    return 'चालक,अचालक एवं कुचालक'
                if i == '2.1':
                    return 'बेसिक इलेक्ट्रिकल'
                if i == '3.1':
                    return 'विद्युत सेल'
                if i == '4.1':
                    return 'संधारित्र'
                if i == '5.1':
                    return 'चुम्बक'
                if i == '6.1':
                    return 'डी.सी.जनित्र'
                if i == '7.1':
                    return 'डी.सी.मोटर'
                if i == '8.1':
                    return 'ए.सी थ्योरी'
                if i == '9.1':
                    return 'भू-सम्पर्कन'
                if i == '10.1':
                    return 'विद्युय वायरिंग'
                if i == '11.1':
                    return 'विद्युत मापक यंत्र'
                if i == '12.1':
                    return 'ट्रांसफार्मर'
                if i == '13.1':
                    return 'प्रत्यावर्तक'
                if i == '14.1':
                    return 'तुल्यकालिक प्रेरण'
                if i == '15.1':
                    return 'ए.सी. मोटर'
                if i == '16.1':
                    return 'वाइंडिंग'
                if i == '17.1':
                    return 'विद्युत उत्पादन,ट्रांसमिशन एवं वितरण'
                if i == '18.1':
                    return 'प्रदीप्ति'
                if i == '19.1':
                    return 'इलेक्ट्रिक्स'
                if i == '20.1':
                    return 'व्यावसायिक एवं सावधानियां'

        if subject == 'FitterLocoPilot':
                if i == '1.1':
                    return 'Introduction'
                if i == '2.1':
                    return 'Fitter tools'
                if i == '3.1':
                    return 'Sheet Metal Shop'
                if i == '4.1':
                    return 'Welding Theory'
                if i == '5.1':
                    return 'Soldering And Brazing'
                if i == '6.1':
                    return 'Physical and Mechanical Properties of Metals'
                if i == '7.1':
                    return'Heat Treatment'
                if i == '8.1':
                    return 'Bearings'
                if i == '9.1':
                    return 'Drilling Machine'
                if i == '10.1':
                    return 'Lathe Machine'
                if i == '11.1':
                    return 'Grinding Machine'
                if i == '12.1':
                    return 'Power Transmission'
                if i == '13.1':
                    return 'Pipe And Pipe Fitting'
                if i == '14.1':
                    return 'Screw Threads'
                if i == '15.1':
                    return 'Gauge'
                if i == '16.1':
                    return 'Limits,Fits And Tolerance'
                if i == '17.1':
                    return 'Other Important Questions'
                if i == '18.1':
                    return 'Previous Year Exams Questions'
        if subject == 'Civil_Loco_Pilot_Tech':
                if i == '2.1':
                    return 'Land Surveying Basic Principal And Classification'
                if i == '2.2':
                    return 'Chain Surveying'
                if i == '2.3':
                    return 'Compass Surveying'
                if i == '2.4':
                    return 'Levelling'
                if i == '2.5':
                    return 'Minor Instruments'
                if i == '2.6':
                    return 'Computation Of Land'
                if i == '2.7':
                    return 'Plane Table Survey'
                if i == '2.8':
                    return 'Contours And Contouring'
                if i == '2.9':
                    return 'Theodolite Survey'
                if i == '50.1':
                    return 'Curve And Curves Setting'
                if i == '12.1':
                    return 'Bending moment and sheer force'
                if i == '12.2':
                    return 'Bending and sheer stress'
                if i == '12.3':
                    return 'Combined direct and bending stress'
                if i == '12.4':
                    return 'Slope and deflection'
                if i == '12.5':
                    return 'Principal stress and principle planes'
                if i == '12.6':
                    return 'Columns and struts'
                if i == '12.7':
                    return 'Trosion'
                if i == '13.1':
                    return 'Rivet Connection'
                if i == '13.2':
                    return 'Weld Connection'
                if i == '13.3':
                    return 'Tension Members'
                if i == '13.4':
                    return 'Compression Member'
                if i == '13.5':
                    return 'Steel Beams'
                if i == '13.6':
                    return 'Column base and Foundation'
                if i == '13.7':
                    return 'Steel root of trusses'


        if subject == 'LocoPilot_Diesel':
                if i == '1.1':
                    return 'Introduction to Engine & Development'
                if i == '2.1':
                    return 'Cylinder Head & Valve Assembly'
                if i == '3.1':
                    return 'Piston & Connecting Rod'
                if i == '4.1':
                    return 'Crank Shaft,Cam Shaft Fly Wheel & Bearing'
                if i == '5.1':
                    return 'Gas Turbine Marine & Statonery Engine'
                if i == '6.1':
                    return 'Cooling & Snake System'
                if i == '7.1':
                    return 'Intake & Exhaust System'
                if i == '8.1':
                    return 'Diesel Fuel Supply System'
                if i == '9.1':
                    return 'Emission Charging & Starting System'
                if i == '10.1':
                    return 'Troubleshooting'




# for knimbus students
        if subject == 'Design and analysis of algorithm':
                if i == '1.1':
                    return 'Divide and Conquer'
                if i == '2.1':
                    return 'Dynamic Programming'
                if i == '3.1':
                    return 'Introduction'
                if i == '4.1':
                    return 'Greedy Method'

        if subject == 'CAT_Quantitative_Aptitude':
                if i == '11.1':
                    return 'Geometry'











    def improvement(self,subject):
        if self.institution == 'School':
            pass
        elif self.institution == 'SSC':
            marks = SSCOnlineMarks.objects.filter(student =
                                                  self.profile,test__sub =
                                                  subject)
            if 'Defence' in subject:
                mixed_marks =\
                SSCOnlineMarks.objects.filter(student=self.profile,test__sub =
                                              'Defence-MultipleSubjects')
            else:

                mixed_marks =\
                SSCOnlineMarks.objects.filter(student=self.profile,test__sub =
                                              'SSCMultipleSections')
            if marks:
                if len(marks)>1:
                    change = []
                    when = []
                    for j,k in enumerate(marks):
                        if j == len(marks)-1:
                            break
                        this = (k.marks/k.test.max_marks)*100
                        that = marks[j+1]
                        that = (that.marks/that.test.max_marks)*100
                        diff = that-this
                        this_time = k.testTaken
                        that_time = marks[j+1]
                        that_time = that_time.testTaken
                        time_diff = that_time - this_time
                        when.append(time_diff)
                        change.append(diff)
                    total_diff = list(zip(when,change))
                    return total_diff
                else:
                    return 'more than one needed'
            #if mixed_marks:
            #    if len(mixed_marks)>1:
            #        change = []
            #        for j,k in enumerate(mixed_marks):
            #            if j == len(mixed_marks)-1:
            #                break
            #            this = (k.marks/k.test.max_marks)*100
            #            that = marks[j+1]
            #            that = (that.marks/that.test.max_marks)*100
            #            diff = that-this
            #            change.append(diff)
            #        return diff
            #    else:
            #        return 'more than one needed'


    def section_improvement(self,subject):
        if self.institution == 'School':
            pass
        elif self.institution == 'SSC':
            # get marks query
            marks =\
            SSCOnlineMarks.objects.filter(student=self.profile,test__sub=subject).order_by('testTaken')
            if 'Defence' in subject:
                mixed_marks =\
                SSCOnlineMarks.objects.filter(student=self.profile,test__sub='Defence-MultipleSubjects').order_by('testTaken')
            else:
                mixed_marks =\
                SSCOnlineMarks.objects.filter(student=self.profile,test__sub='SSCMultipleSections').order_by('testTaken')
            # get all marks in list and sort it by test taken
            total = []
            if marks:
                for i in marks:
                    total.append(i)
            if mixed_marks:
                for j in mixed_marks:
                    total.append(j)
            total.sort(key=lambda r:r.testTaken)

            # put all right and wrong questions in a separate list(also adding
            # topics)

            overall_accuracy = []

            for i in total:
                topics = []
                day = []
                ra = []
                wa = []

                for r in i.rightAnswers:
                    try:
                        rq = SSCquestions.objects.get(choices__id = r)
                        if rq.section_category == subject:
                            ra.append(rq)
                            cat = rq.topic_category
                            topics.append(cat)
                    except:
                        pass
                for w in i.wrongAnswers:
                    try:
                        wq = SSCquestions.objects.get(choices__id = w)
                        if wq.section_category == subject:
                            wa.append(wq)
                            cat = wq.topic_category
                            topics.append(cat)
                    except:
                        pass
                # get unique topics
                topics = list(unique_everseen(topics))
                accuracy_dict = {}
                # get topic wise accuracy
                for j in topics:
                    right = 0
                    wrong = 0
                    for r in ra:
                        if r.topic_category == j:
                            right += 1
                    for w in wa:
                        if w.topic_category == j:
                            wrong += 1
                    total = right + wrong
                    accuracy = ((right-wrong)/total)*100
                    tp_j = self.changeIndividualNames(j,subject)
                    topic_accuracy = np.array([tp_j,accuracy,i.testTaken])
                    overall_accuracy.append(topic_accuracy)
            overall_accuracy = np.array(overall_accuracy)
            tp = []
            final_accuracy = []
            another_dict = {}
            try:
                for i in overall_accuracy[:,0]:
                    tp.append(i)
            except:
                return 0
            tp = list(unique_everseen(tp))
            for i in tp:
                name = eval("'topic'+str(i)")
                name_d = name
                name = []
                for n,j in enumerate(overall_accuracy[:,0]):
                    if j == i:
                        name.append(overall_accuracy[n])
                final_accuracy.append(name)
                another_dict[i] = {'dic':name}
            final_accuracy = np.array(final_accuracy)
            return another_dict









    def sectionwise_improvement(self,subject):
        if self.institution == 'School':
            pass
        elif self.institution == 'SSC':
            marks = SSCOnlineMarks.objects.filter(student =
                                                  self.profile,test__sub=
                                                  subject).order_by('id')
            if 'Defence' in subject:
                mixed_marks = SSCOnlineMarks.objects.filter(student=
                                                        self.profile,test__sub
                                                        ='Defence-MultipleSubjects').order_by('id')
            else:
                mixed_marks = SSCOnlineMarks.objects.filter(student=
                                                        self.profile,test__sub
                                                        ='SSCMultipleSections').order_by('id')
            # get all the categories of questions that student has taken
            all_categories = []
            if len(marks) > 1:
                all_answers = []
                quests = []
                skipped_answers = []
                for i in marks:
                    for aa in i.allAnswers:
                        all_answers.append(aa)
                    for sp in i.skippedAnswers:
                        skipped_answers.append(sp)
                for quest_id in all_answers:
                    quests.append(SSCquestions.objects.get(choices__id =
                                                           quest_id))
                #for quest_id in skipped_answers:
                #    quests.append(SSCquestions.objects.get(id = quest_id))
                for q in quests:
                    all_categories.append(q.topic_category)

            if mixed_marks:
                all_answers = []
                quests = []
                skipped_answers = []
                for i in mixed_marks:
                    for aa in i.allAnswers:
                        all_answers.append(aa)
                    for sp in i.skippedAnswers:
                        skipped_answers.append(sp)
                for quest_id in all_answers:
                    quests.append(SSCquestions.objects.get(choices__id =
                                                           quest_id))
                #for quest_id in skipped_answers:
                #    quests.append(SSCquestions.objects.get(id = quest_id))
                for q in quests:
                    all_categories.append(q.topic_category)
            all_categories = list(unique_everseen(all_categories))
            changes = {}
            changes_mixed = {}

            # get changes in accuracy topic wise (all questions answered
            # excluding not attempted questions)
            for tp in all_categories:
                test_count = 0
                for i in marks:
                    test_count += 1
                    rightCount = 0
                    allCount = 0
                    wCount = 0
                    for ra in i.rightAnswers:
                        quest = SSCquestions.objects.get(choices__id = ra)
                        if quest.topic_category == tp:
                            rightCount += 1
                            allCount += 1
                    for wa in i.wrongAnswers:
                        quest = SSCquestions.objects.get(choices__id = wa)
                        if quest.topic_category == tp:
                            wCount += 1
                            allCount += 1
                    #for sp in i.skippedAnswers:
                    #    quest = SSCquestions.objects.get(id = sp)
                    #    if quest.topic_category == tp:
                    #        wCount += 1
                    #        allCount += 1
                    try:
                        total = (((rightCount - wCount)/(rightCount+wCount))*100)
                        tpp = self.changeIndividualNames(tp,subject)

                        changes[str(tp)+','+str(test_count)] = {'topic':
                                                                tpp,'index':
                                                                test_count,'percent':total,'time':i.testTaken,'test_id':i.id}
                    except Exception as e:
                        print(str(e))
                test_count_mixed = 0
                for i in mixed_marks:
                    test_count_mixed += 1
                    rightCount = 0
                    allCount = 0
                    wCount = 0
                    for ra in i.rightAnswers:
                        quest = SSCquestions.objects.get(choices__id = ra)
                        if quest.topic_category == tp:
                            rightCount += 1
                            allCount += 1
                    for wa in i.wrongAnswers:
                        quest = SSCquestions.objects.get(choices__id = wa)
                        if quest.topic_category == tp:
                            wCount += 1
                            allCount += 1
                    for sp in i.skippedAnswers:
                        quest = SSCquestions.objects.get(id = sp)
                        if quest.topic_category == tp:
                            wCount += 1
                            allCount += 1
                    try:
                        total = (((rightCount - wCount)/(rightCount + wCount))*100)
                        tpp = self.changeIndividualNames(tp, subject)
                        changes_mixed[str(tp)+','+str(test_count)] = {'topic':
                                                                tpp,'index':
                                                                test_count_mixed,'percent':total,'time':i.testTaken,
                                                                      'test_id':i.id}
                    except Exception as e:
                        print(str(e))
            names_categories =\
            self.convertTopicNumbersNames(all_categories,subject)
            return changes,changes_mixed,names_categories

    def plot_improvement(self,subject):
        changes,mixed_changes,all_categories = self.sectionwise_improvement(subject)
        all_ids = []
        for key,value in changes.items():
            all_ids.append(value['test_id'])
        all_ids = list(unique_everseen(all_ids))
        all_ids.sort()

        #for i in all_ids:
        #    for k,v in changes.items():
        #        if v['test_id'] == i:
        #          time.append(v['time'])
        #          topic.append(v['topic'])
        #          percent.append(v['percent'])
        #          ind.append(i)
        #    overall = list(zip(ind,topic,percent,time))
        overall = {}
        final_list = []
        if all_categories:
            for i in all_categories:
                time = []
                testid = []
                ind = []
                percent = []

                for k,v in changes.items():
                    if changes[k]['topic'] == i:
                        time.append(changes[k]['time'])
                        testid.append(changes[k]['test_id'])
                        percent.append(changes[k]['percent'])
                overall[i] =\
                        {'time':time,'testid':testid,'percent':percent}
        if overall:
            return overall
        else:
            return None
    def skipped_testwise(self,testid,student):
        marks = SSCOnlineMarks.objects.get(student = student,test__id = testid)
        quest_cat = []
        for qid in marks.skippedAnswers:
            quest = SSCquestions.objects.get(id = qid)
            cat = quest.topic_category
            quest_cat.append(cat)
        unique,count = np.unique(quest_cat,return_counts=True)
        sk_cat = np.asarray((unique,count)).T
        return sk_cat

    def student_weak_timing_details(self,student_id,subject,chapter):
        student = Student.objects.get(id = student_id)
        my_marks = SSCOnlineMarks.objects.filter(student = student)
        right_time = []
        wrong_time = []
        for mark in my_marks:
            for rid in mark.rightAnswers:
                quest = SSCquestions.objects.get(choices__id = rid)
                print(quest.section_category)
                print(quest.topic_category)
                if quest.section_category == subject and quest.topic_category\
                == chapter:
                    answered = SSCansweredQuestion.objects.get(onlineMarks =
                                                               mark,quest=quest)
                    right_time.append(answered.time)
            for wid in mark.wrongAnswers:
                quest = SSCquestions.objects.get(choices__id = rid)
                if quest.section_category == subject and quest.topic_category\
                == chapter:
                    answered = SSCansweredQuestion.objects.get(onlineMarks =
                                                               mark,quest=quest)
                    wrong_time.append(answered.time)
        len_right = len(right_time)
        len_wrong = len(wrong_time)
        if len_right == 0:
            ave_right = 'No right questions'
        else:
            ave_right = sum(right_time) / len_right
        if len_wrong == 0:
            ave_wrong = 'No wrong questions'
        else:
            ave_wrong = sum(wrong_time) / len_wrong
        total = len_right + len_wrong
        context =\
        {'right_time':ave_right,'ave_wrong':ave_wrong,'total_attempted':total}
        return context



#------------------------------------------Student Ends


class Teach:
    def __init__(self, user):
        self.profile = user.teacher
        self.institution = self.profile.school.category


    def my_classes_objects(self, klass_name=None):
        if klass_name is None:
            kl = klass.objects.filter(school=self.profile.school)
        else:
            kl = klass.objects.get(school=self.profile.school,name=klass_name)
        return kl
        #if klass_name:
        #    subs = self.profile.subject_set.all()
        #    if subs:
        #        klasses = []
        #        for sub in subs:
        #            if sub.student.klass.name == klass_name:
        #                klasses.append(sub.student.klass)
        #        return klasses[0]
        #    else:
        #        return None

        #subs = self.profile.subject_set.all()
        #if subs:
        #    klasses = []
        #    for sub in subs:
        #        klasses.append(sub.student.klass)
        #    return klasses
        #else:
        #    return None

    def my_classes_names(self):
        subs = self.profile.subject_set.all()
        if subs:
            klasses = []
            for sub in subs:
                klasses.append(sub.student.klass.name)
            klasses = list(unique_everseen(klasses))
            return klasses
        else:
            return None
    def my_classes_names_cache(self):
        klass = TeacherClasses.objects.filter(teacher = self.profile)
        klasses = []
        for kl in klass:
            klasses.append(kl.klass)
        return list(unique_everseen(klasses))

    def my_subjects_names(self):
        subs = self.profile.subject_set.all()
        subjects = []
        for i in subs:
            subjects.append(i.name)
        subjects = list(unique_everseen(subjects))
        return subjects

    def my_school(self):
        school = self.profile.school
        return school

    def listofStudents(self, klass):
        listofstudents = []
        subject_list = self.profile.subject_set.filter(student__klass__name=klass)
        for i in subject_list:
            listofstudents.append(i.student)
        return listofstudents

    def listofStudentsMarks(self, which_class):
        marks_class_test1 = []
        marks_class_test2 = []
        marks_class_test3 = []
        marks_class_predictedHy = []
        sub_class = self.profile.subject_set.filter(student__klass__name=which_class)
        if not sub_class:
            pass
        else:
            for i in sub_class:
                if i.test1:
                    marks_class_test1.append(i.test1)
                if i.test2:
                    marks_class_test2.append(i.test2)
                if i.test3:
                    marks_class_test3.append(i.test3)
                if i.predicted_hy:
                    marks_class_predictedHy.append(i.predicted_hy)
        return marks_class_test1, marks_class_test2, marks_class_test3, marks_class_predictedHy

    def teacher_get_testmarks_classwise(req, klass_dict):
        klass_test1_dict = {}  # dictionary to hold test1 marks of different classes
        klass_test2_dict = {}
        klass_test3_dict = {}

        # fill out the above dictionaries

        for i in klass_dict.values():
            kk = i
            klasstest1 = []
            klasstest2 = []
            klasstest3 = []

            for j in kk:
                klasstest1.append(j.test1)
                klasstest2.append(j.test2)
                klasstest3.append(j.test3)
                testm1 = {str(j.student.klass): klasstest1}
                testm2 = {str(j.student.klass): klasstest2}
                testm3 = {str(j.student.klass): klasstest3}
            klass_test1_dict.update(testm1)
            klass_test2_dict.update(testm2)
            klass_test3_dict.update(testm3)
        return klass_test1_dict, klass_test2_dict, klass_test2_dict

    def find_frequency_grades(self, test1, test2=None, test3=None):
        t1_fg_a = 0
        t1_fg_b = 0
        t1_fg_c = 0
        t1_fg_d = 0
        t1_fg_e = 0
        t1_fg_f = 0
        t1_fg_s = 0

        t2_fg_a = 0
        t2_fg_b = 0
        t2_fg_c = 0
        t2_fg_d = 0
        t2_fg_f = 0
        t2_fg_e = 0
        t2_fg_s = 0

        t3_fg_a = 0
        t3_fg_b = 0
        t3_fg_c = 0
        t3_fg_d = 0
        t3_fg_e = 0
        t3_fg_f = 0
        t3_fg_s = 0
        if test2 is None:

            for i in test1:
                if i == 'E':
                    t1_fg_e = t1_fg_e + 1
                elif i == 'F':
                    t1_fg_f = t1_fg_f + 1
                elif i == 'A':
                    t1_fg_a = t1_fg_a + 1
                elif i == 'B':
                    t1_fg_b = t1_fg_b + 1
                elif i == 'C':
                    t1_fg_c = t1_fg_c + 1
                elif i == 'D':
                    t1_fg_d = t1_fg_d + 1
                elif i == 'S':
                    t1_fg_s = t1_fg_s + 1
            return t1_fg_a, t1_fg_b, t1_fg_c, t1_fg_d, t1_fg_e, t1_fg_f, t1_fg_s

        elif test3 is None:
            for i in test1:
                if i == 'E':
                    t1_fg_e = t1_fg_e + 1
                elif i == 'F':
                    t1_fg_f = t1_fg_f + 1
                elif i == 'A':
                    t1_fg_a = t1_fg_a + 1
                elif i == 'B':
                    t1_fg_b = t1_fg_b + 1
                elif i == 'C':
                    t1_fg_c = t1_fg_c + 1
                elif i == 'D':
                    t1_fg_d = t1_fg_d + 1
                elif i == 'S':
                    t1_fg_s = t1_fg_s + 1

            for i in test2:
                if i == 'E':
                    t2_fg_e = t2_fg_e + 1
                elif i == 'F':
                    t2_fg_f = t2_fg_f + 1
                elif i == 'A':
                    t2_fg_a = t2_fg_a + 1
                elif i == 'B':
                    t2_fg_b = t2_fg_b + 1
                elif i == 'C':
                    t2_fg_c = t2_fg_c + 1
                elif i == 'D':
                    t2_fg_d = t2_fg_d + 1
                elif i == 'S':
                    t2_fg_s = t2_fg_s + 1

            return t1_fg_a, t1_fg_b, t1_fg_c, t1_fg_d, t1_fg_e, t1_fg_f, t1_fg_s, \
                   t2_fg_a, t2_fg_b, t2_fg_c, t2_fg_d, t2_fg_e, t2_fg_f, t2_fg_s
        else:
            for i in test1:
                if i == 'E':
                    t1_fg_e = t1_fg_e + 1
                elif i == 'F':
                    t1_fg_f = t1_fg_f + 1
                elif i == 'A':
                    t1_fg_a = t1_fg_a + 1
                elif i == 'B':
                    t1_fg_b = t1_fg_b + 1
                elif i == 'C':
                    t1_fg_c = t1_fg_c + 1
                elif i == 'D':
                    t1_fg_d = t1_fg_d + 1
                elif i == 'S':
                    t1_fg_s = t1_fg_s + 1

            for i in test2:
                if i == 'E':
                    t2_fg_e = t2_fg_e + 1
                elif i == 'F':
                    t2_fg_f = t2_fg_f + 1
                elif i == 'A':
                    t2_fg_a = t2_fg_a + 1
                elif i == 'B':
                    t2_fg_b = t2_fg_b + 1
                elif i == 'C':
                    t2_fg_c = t2_fg_c + 1
                elif i == 'D':
                    t2_fg_d = t2_fg_d + 1
                elif i == 'S':
                    t2_fg_s = t2_fg_s + 1
            for i in test3:
                if i == 'E':
                    t3_fg_e = t3_fg_e + 1
                elif i == 'F':
                    t3_fg_f = t3_fg_f + 1
                elif i == 'A':
                    t3_fg_a = t3_fg_a + 1
                elif i == 'B':
                    t3_fg_b = t3_fg_b + 1
                elif i == 'C':
                    t3_fg_c = t3_fg_c + 1
                elif i == 'D':
                    t3_fg_d = t3_fg_d + 1
                elif i == 'S':
                    t3_fg_s = t3_fg_s + 1
            return t1_fg_a, t1_fg_b, t1_fg_c, t1_fg_d, t1_fg_e, t1_fg_f, t1_fg_s, \
                   t2_fg_a, t2_fg_b, t2_fg_c, t2_fg_d, t2_fg_e, t2_fg_f, t2_fg_s, \
                   t3_fg_a, t3_fg_b, t3_fg_c, t3_fg_d, t3_fg_e, t3_fg_f, t3_fg_s

    def find_grade_from_marks(self, test1, test2=None, test3=None):
        test1_grade = []
        test2_grade = []
        test3_grade = []
        test1 = np.array(test1)
        if test2 is None:
            for i, n in enumerate(test1):
                if n < 4:
                    test1_grade.append('F')
                if 4 <= n < 5:
                    test1_grade.append('E')
                if 5 <= n < 6:
                    test1_grade.append('D')
                if 6 <= n < 7:
                    test1_grade.append('C')
                if 7 <= n < 8:
                    test1_grade.append('B')
                if 8 <= n < 9:
                    test1_grade.append('A')
                if 9 <= n <= 10:
                    test1_grade.append('S')
            return test1_grade
        elif test3 is None:

            test2 = np.array(test2)

            for i, n in enumerate(test1):
                if n < 4:
                    test1_grade.append('F')
                if 4 <= n < 5:
                    test1_grade.append('E')
                if 5 <= n < 6:
                    test1_grade.append('D')
                if 6 <= n < 7:
                    test1_grade.append('C')
                if 7 <= n < 8:
                    test1_grade.append('B')
                if 8 <= n < 9:
                    test1_grade.append('A')
                if 9 <= n <= 10:
                    test1_grade.append('S')

            for i, n in enumerate(test2):
                if n < 4:
                    test2_grade.append('F')
                if 4 <= n < 5:
                    test2_grade.append('E')
                if 5 <= n < 6:
                    test2_grade.append('D')
                if 6 <= n < 7:
                    test2_grade.append('C')
                if 7 <= n < 8:
                    test2_grade.append('B')
                if 8 <= n < 9:
                    test2_grade.append('A')
                if 9 <= n <= 10:
                    test2_grade.append('S')
            return test1_grade, test2_grade
        else:
            test2 = np.array(test2)
            test3 = np.array(test3)
            for i, n in enumerate(test1):
                if n < 4:
                    test1_grade.append('F')
                if 4 <= n < 5:
                    test1_grade.append('E')
                if 5 <= n < 6:
                    test1_grade.append('D')
                if 6 <= n < 7:
                    test1_grade.append('C')
                if 7 <= n < 8:
                    test1_grade.append('B')
                if 8 <= n < 9:
                    test1_grade.append('A')
                if 9 <= n <= 10: test1_grade.append('S')

            for i, n in enumerate(test2):
                if n < 4:
                    test2_grade.append('F')
                if 4 <= n < 5:
                    test2_grade.append('E')
                if 5 <= n < 6:
                    test2_grade.append('D')
                if 6 <= n < 7:
                    test2_grade.append('C')
                if 7 <= n < 8:
                    test2_grade.append('B')
                if 8 <= n < 9:
                    test2_grade.append('A')
                if 9 <= n < 11:
                    test2_grade.append('S')
            for i, n in enumerate(test3):
                if n < 4:
                    test3_grade.append('F')
                if 4 <= n < 5:
                    test3_grade.append('E')
                if 5 <= n < 6:
                    test3_grade.append('D')
                if 6 <= n < 7:
                    test3_grade.append('C')
                if 7 <= n < 8:
                    test3_grade.append('B')
                if 8 <= n < 9:
                    test3_grade.append('A')
                if 9 <= n <= 10:
                    test3_grade.append('S')
            return test1_grade, test2_grade, test3_grade

    def averageoftest(self, test, test2=None, test3=None):
        if test2 is None and test3 is None:
            testmarks = np.array(test)
            return np.mean(testmarks)
        elif test3 is None:
            testmarks = np.array(test)
            testmarks2 = np.array(test2)
            return np.mean(testmarks), np.mean(testmarks2)
        else:
            testmarks = np.array(test)
            testmarks2 = np.array(test2)
            testmarks3 = np.array(test3)
            return np.mean(testmarks), np.mean(testmarks2), np.mean(testmarks3)

    def school_test_analysis(self, test):
        average_test = self.averageoftest(test)
        g1 = self.find_grade_from_marks(test)
        t1_fg_a, t1_fg_b, t1_fg_c, t1_fg_d, t1_fg_e, t1_fg_f, t1_fg_s = \
            self.find_frequency_grades(g1)
        context = \
            {'testav': average_test, 't1_fg_a': t1_fg_a, 't1_fg_b': t1_fg_b,
             't1_fg_c': t1_fg_c, 't1_fg_d': t1_fg_d, 't1_fg_e': t1_fg_e, 't1_fg_f': t1_fg_f,
             't1_fg_s': t1_fg_s}
        return context
    def online_findAverageofTest(self, test_id, percent=None):
        if self.institution == 'School':
            if percent:
                test = OnlineMarks.objects.filter(test__id=test_id)
                all_marks = []
                all_marks_percent = []
                for te in test:
                    all_marks.append(int(te.marks))
                    all_marks_percent.append((te.marks / te.test.max_marks) * 100)
                average = np.mean(all_marks)
                percent_average = np.mean(all_marks_percent)
                return average, percent_average
            else:
                test = OnlineMarks.objects.filter(test__id=test_id)
                all_marks = []
                for te in test:
                    all_marks.append(int(te.marks))
                average = np.mean(all_marks)

                return average
        elif self.institution == 'SSC':
            if percent:
                test = SSCOnlineMarks.objects.filter(test__id=test_id)
                all_marks = []
                all_marks_percent = []
                for te in test:
                    all_marks.append(int(te.marks))
                    all_marks_percent.append((te.marks / te.test.max_marks) * 100)
                average = np.mean(all_marks)
                percent_average = np.mean(all_marks_percent)
                return average, percent_average
            else:
                test = SSCOnlineMarks.objects.filter(test__id=test_id)
                all_marks = []
                for te in test:
                    all_marks.append(int(te.marks))
                average = np.mean(all_marks)
                return average


    def offline_findAverageofTest(self, test_id, percent=None):
        if self.institution == 'School':
            if percent:
                test = OnlineMarks.objects.filter(test__id=test_id)
                all_marks = []
                all_marks_percent = []
                for te in test:
                    all_marks.append(int(te.marks))
                    all_marks_percent.append((te.marks / te.test.max_marks) * 100)
                average = np.mean(all_marks)
                percent_average = np.mean(all_marks_percent)
                return average, percent_average
            else:
                test = OnlineMarks.objects.filter(test__id=test_id)
                all_marks = []
                for te in test:
                    all_marks.append(int(te.marks))
                average = np.mean(all_marks)

                return average
        elif self.institution == 'SSC':
            if percent:
                test = SSCOfflineMarks.objects.filter(test__id=test_id)
                all_marks = []
                all_marks_percent = []
                for te in test:
                    all_marks.append(int(te.marks))
                    all_marks_percent.append((te.marks / te.test.max_marks) * 100)
                average = np.mean(all_marks)
                percent_average = np.mean(all_marks_percent)
                return average, percent_average
            else:
                test = SSCOfflineMarks.objects.filter(test__id=test_id)
                all_marks = []
                for te in test:
                    all_marks.append(int(te.marks))
                average = np.mean(all_marks)
                return average

    def online_freqeucyGrades(self,test_id,mode = None):
        if self.institution == 'School':
            test = OnlineMarks.objects.filter(test__id = test_id)
        elif self.institution == 'SSC':
            if mode =='offline':
                test = SSCOfflineMarks.objects.filter(test__id = test_id)
            else:
                test = SSCOnlineMarks.objects.filter(test__id = test_id)
        all_marks = []
        for i in test:
            all_marks.append((i.marks/i.test.max_marks)*100)
        grade_s = 0
        grade_a = 0
        grade_b = 0
        grade_c = 0
        grade_d = 0
        grade_e = 0
        grade_f = 0
        for marks in all_marks:
            if math.ceil(marks) < 33:
                grade_f +=1
            elif 33 <= math.ceil(marks) < 50:
                grade_e +=1
            elif 50 <= math.ceil(marks) < 60:
                grade_d +=1
            elif 60 <= math.ceil(marks) < 70:
                grade_c +=1
            elif 70 <= math.ceil(marks) < 80:
                grade_b +=1
            elif 80 <= math.ceil(marks) < 90:
                grade_a +=1
            elif 90 <= math.ceil(marks) <= 100:
                grade_s +=1
        return grade_s,grade_a,grade_b,grade_c,grade_d,grade_e,grade_f

    def online_QuestionPercentage(self, test_id):
        if self.institution == 'School':
            online_marks = OnlineMarks.objects.filter(test__id=test_id)
        elif self.institution == 'SSC':
            online_marks = SSCOnlineMarks.objects.filter(test__id=test_id)
        all_answers = []
        for aa in online_marks:
            all_answers.extend(aa.allAnswers)
        unique, counts = np.unique(all_answers, return_counts=True)
        freq = np.asarray((unique, counts)).T
        return freq

    def offline_QuestionPercentage(self, test_id):
        if self.institution == 'School':
            offline_marks = OnlineMarks.objects.filter(test__id=test_id)
        elif self.institution == 'SSC':
            offline_marks = SSCOfflineMarks.objects.filter(test__id=test_id)
        all_answers = []
        for aa in offline_marks:
            all_answers.extend(aa.allAnswers)
        unique, counts = np.unique(all_answers, return_counts=True)
        freq = np.asarray((unique, counts)).T
        return freq





    def online_skippedQuestions(self,test_id,mode=None):
        if self.institution == 'School':
            online_marks = OnlineMarks.objects.filter(test__id=test_id)
        elif self.institution == 'SSC':
            if mode == 'offline':
                online_marks = SSCOfflineMarks.objects.filter(test__id=test_id)
            else:
                online_marks = SSCOnlineMarks.objects.filter(test__id=test_id)
        skipped_questions = []
        for om in online_marks:
            for sq in om.skippedAnswers:
                skipped_questions.append(sq)
        unique, counts = np.unique(skipped_questions, return_counts=True)
        sq = np.asarray((unique, counts)).T
        return sq

    def online_problematicAreasperTest(self,test_id):
        if self.institution == 'School':
            online_marks = OnlineMarks.objects.filter(test__id = test_id)
            wrong_answers = []
            for om in online_marks:
                for wa in om.wrongAnswers:
                    wrong_answers.append(wa)
            wq = []
            for i in wrong_answers:
                qu = Questions.objects.get(choices__id = i)
                quid = qu.id
                wq.append(quid)

            unique, counts = np.unique(wq, return_counts=True)
            waf = np.asarray((unique, counts)).T
            nw_ind = []
            kk = np.sort(waf,0)[::-1]
            for u in kk[:,1]:
                for z,w in waf:
                    if u == w:
                        if z in nw_ind:
                            continue
                        else:
                            nw_ind.append(z)
                            break
            final_freq = np.asarray((nw_ind,kk[:,1])).T
            return final_freq
        elif self.institution == 'SSC':
            online_marks = SSCOnlineMarks.objects.filter(test__id = test_id)
            wrong_answers = []
            for om in online_marks:
                wrong_answers.extend(om.wrongAnswers)
            wq = []
            for i in wrong_answers:
                qu = SSCquestions.objects.get(choices__id = i)
                quid = qu.id
                wq.append(quid)

            unique, counts = np.unique(wq, return_counts=True)
            waf = np.asarray((unique, counts)).T
            nw_ind = []
            kk = np.sort(waf,0)[::-1]
            for u in kk[:,1]:
                for z,w in waf:
                    if u == w:
                        if z in nw_ind:
                            continue
                        else:
                            nw_ind.append(z)
                            break
            final_freq = np.asarray((nw_ind,kk[:,1])).T
            return final_freq
    def offline_problematicAreasperTest(self,test_id):
        if self.institution == 'School':
            online_marks = OnlineMarks.objects.filter(test__id = test_id)
            wrong_answers = []
            for om in online_marks:
                for wa in om.wrongAnswers:
                    wrong_answers.append(wa)
            wq = []
            for i in wrong_answers:
                qu = Questions.objects.get(choices__id = i)
                quid = qu.id
                wq.append(quid)

            unique, counts = np.unique(wq, return_counts=True)
            waf = np.asarray((unique, counts)).T
            nw_ind = []
            kk = np.sort(waf,0)[::-1]
            for u in kk[:,1]:
                for z,w in waf:
                    if u == w:
                        if z in nw_ind:
                            continue
                        else:
                            nw_ind.append(z)
                            break
            final_freq = np.asarray((nw_ind,kk[:,1])).T
            return final_freq
        elif self.institution == 'SSC':
            online_marks = SSCOfflineMarks.objects.filter(test__id = test_id)
            wrong_answers = []
            for om in online_marks:
                for wa in om.wrongAnswers:
                    wrong_answers.append(wa)
            wq = []
            for i in wrong_answers:
                try:
                    qu = SSCquestions.objects.get(choices__id = i)
                except Exception as e:
                    print(str(e))
                    continue
                quid = qu.id
                wq.append(quid)

            unique, counts = np.unique(wq, return_counts=True)
            waf = np.asarray((unique, counts)).T
            nw_ind = []
            kk = np.sort(waf,0)[::-1]
            for u in kk[:,1]:
                for z,w in waf:
                    if u == w:
                        if z in nw_ind:
                            continue
                        else:
                            nw_ind.append(z)
                            break
            final_freq = np.asarray((nw_ind,kk[:,1])).T
            return final_freq
    # problematic areas for non cached tests
    def online_problematicAreasCache(self,user,subject,klass,ids):

        online_marks = []
        for te in ids:
            test = SSCOnlineMarks.objects.filter(test__id = te,test__creator =
                                                 user)
            online_marks.append(test)



        wrong_answers = []
        skipped_answers = []
        if online_marks:
            for om in online_marks:
                for wa in om.wrongAnswers:
                    wrong_answers.append(wa)
                for sp in om.skippedAnswers:
                    skipped_answers.append(sp)

        wq = []
        for i in wrong_answers:
            if self.institution == 'School':
                qu = Questions.objects.get(choices__id = i)
            elif self.institution == 'SSC':
                try:
                    qu = SSCquestions.objects.get(choices__id = i)
                except Exception as e:
                    print(str(e))
                    continue
            if qu.section_category == subject:
                quid = qu.id
                wq.append(quid)
        for i in skipped_answers:
            if self.institution == 'School':
                try:
                    qu = Questions.objects.get(id = i)
                except Exception as e:
                    print(str(e))
                    continue
            elif self.institution == 'SSC':
                try:
                    qu = SSCquestions.objects.get(id = i)
                except Exception as e:
                    print(str(e))
                    continue
            if qu.section_category == subject:
                quid = qu.id
                wq.append(quid)

        unique, counts = np.unique(wq, return_counts=True)
        waf = np.asarray((unique, counts)).T
        nw_ind = []
        kk = np.sort(waf,0)[::-1]
        for u in kk[:,1]:
            for z,w in waf:
                if u == w:
                    if z in nw_ind:
                        continue
                    else:
                        nw_ind.append(z)
                        break
        final_freq = np.asarray((nw_ind,kk[:,1])).T

    def online_problematicAreaswithIntensityCache(self,user,subject,klass,ids):
        arr = self.online_problematicAreasCache(user,subject,klass,ids)
        anal = []
        num = []
        for u,k in arr:
            if self.institution == 'School':
                qu = Questions.objects.get(id = u)
            elif self.institution == 'SSC':
                qu = SSCquestions.objects.get(id = u)
            category = qu.topic_category
            anal.append(category)
            num.append(k)
        analysis = list(zip(anal,num))
        final_analysis = []
        final_num = []
        for u,k in analysis:
            if u in final_analysis:
                ind = final_analysis.index(u)
                temp = final_num[ind]
                final_num[ind] = temp + k
            else:
                final_analysis.append(u)
                final_num.append(k)
        # weak areas frequency
        waf = list(zip(final_analysis,final_num))
        return waf




    def online_problematicAreas(self,user,subject,klass,api=None):
        if self.institution == 'School':
            online_marks = OnlineMarks.objects.filter(test__creator= user,test__sub=
                                                  subject,test__klas__name = klass)
        elif self.institution == 'SSC':
            print('{} subject,{} klass'.format(subject,klass))
            online_marks = SSCOnlineMarks.objects.filter(test__creator= user,test__sub=
                                                  subject,test__klas__name = klass)

            if 'Defence' in klass:
                all_onlineMarks = SSCOnlineMarks.objects.filter(test__creator =
                                                                user,test__sub =
                                                                'Defence-MultipleSubjects',test__klas__name=
                                                                klass)
            else:

                all_onlineMarks = SSCOnlineMarks.objects.filter(test__creator =
                                                                user,test__sub =
                                                                'SSCMultipleSections',test__klas__name=
                                                                klass)
            offline_marks = SSCOfflineMarks.objects.filter(test__creator =
                                                           user,test__sub =
                                                           subject,test__klas__name
                                                           = klass)

            all_offlinemarks = SSCOfflineMarks.objects.filter(test__creator =
                                                               user,test__sub =
                                                               'SSCMultipleSections',test__klas__name
                                                            = klass)

        wrong_answers = []
        skipped_answers = []
        if online_marks:
            for om in online_marks:
                for wa in om.wrongAnswers:
                    wrong_answers.append(wa)
                for sp in om.skippedAnswers:
                    skipped_answers.append(sp)


        if all_onlineMarks:
            for om in all_onlineMarks:
                for wa in om.wrongAnswers:
                    wrong_answers.append(wa)
                for sp in om.skippedAnswers:
                    skipped_answers.append(sp)
        if offline_marks:
            for om in offline_marks:
                for wa in om.wrongAnswers:
                    wrong_answers.append(wa)
                for sp in om.skippedAnswers:
                    skipped_answers.append(sp)
        if all_offlinemarks:
            for om in all_offlinemarks:
                for wa in om.wrongAnswers:
                    wrong_answers.append(wa)
                for sp in om.skippedAnswers:
                    skipped_answers.append(sp)


        wq = []
        for i in wrong_answers:
            if self.institution == 'School':
                qu = Questions.objects.get(choices__id = i)
            elif self.institution == 'SSC':
                try:
                    qu = SSCquestions.objects.get(choices__id = i)
                except Exception as e:
                    print(str(e))
                    continue
            if qu.section_category == subject:
                quid = qu.id
                wq.append(quid)
        for i in skipped_answers:
            if self.institution == 'School':
                try:
                    qu = Questions.objects.get(id = i)
                except Exception as e:
                    print(str(e))
                    continue
            elif self.institution == 'SSC':
                try:
                    qu = SSCquestions.objects.get(id = i)
                except Exception as e:
                    print(str(e))
                    continue
            if qu.section_category == subject:
                quid = qu.id
                wq.append(quid)

        unique, counts = np.unique(wq, return_counts=True)
        waf = np.asarray((unique, counts)).T
        nw_ind = []
        kk = np.sort(waf,0)[::-1]
        for u in kk[:,1]:
            for z,w in waf:
                if u == w:
                    if z in nw_ind:
                        continue
                    else:
                        nw_ind.append(z)
                        break
        final_freq = np.asarray((nw_ind,kk[:,1])).T
        print('%s final freq' %final_freq)
        return final_freq

    def online_problematicAreasNames(self,user,subject,klass):
        arr = self.online_problematicAreas(user.id,subject,klass)

        if self.institution == 'School':
            how_many = 0
            areas = []
            for u,k in arr:
                if how_many == 3:
                    break
                qu = Questions.objects.get(id = u)
                cat = qu.topic_category
                areas.append(cat)
                how_many += 1
            areas = list(unique_everseen(areas))
            area_names=  self.change_topicNumbersNames(arr,subject)
            return areas
        elif self.institution == 'SSC':
            how_many = 0
            areas = []
            for u,k in arr:
                if how_many == 3:
                    break
                qu = SSCquestions.objects.get(id = u)
                cat = qu.topic_category
                areas.append(cat)
                how_many += 1
            areas = list(unique_everseen(areas))
            area_names=  self.change_topicNumbersNames(areas,subject)
            area_names = np.array(area_names)
            print('%s area names' %area_names)
            return area_names[:,0]

    def online_problematicAreaswithIntensity(self,user,subject,klass):
        arr = self.online_problematicAreas(user,subject,klass)
        anal = []
        num = []
        for u,k in arr:
            if self.institution == 'School':
                qu = Questions.objects.get(id = u)
            elif self.institution == 'SSC':
                qu = SSCquestions.objects.get(id = u)
            category = qu.topic_category
            anal.append(category)
            num.append(k)
        analysis = list(zip(anal,num))
        final_analysis = []
        final_num = []
        for u,k in analysis:
            if u in final_analysis:
                ind = final_analysis.index(u)
                temp = final_num[ind]
                final_num[ind] = temp + k
            else:
                final_analysis.append(u)
                final_num.append(k)
        # weak areas frequency
        waf = list(zip(final_analysis,final_num))
        return waf


    def online_problematicAreaswithIntensityAverage(self,user,subject,klass):
        if self.institution  == 'School':
            pass
        elif self.institution == 'SSC':
#1. Look for cache of weak areas for subject and class, get all the
# that have been taken at-least once. If sum of all tests is equal
# to all tests in cache, then just send back the data from cache.
#2. If number of tests taken by students has increased then
# calculate the weak areas for only new tests and then calculate
# the overall weak areas then save it into cache
#3. Weak areas is running for the first time, calculate all the
# weak areas and create a cache in the database.
            try:
                weak_cache = TeacherWeakAreasDetailCache.objects.get(teacher =
                                                                     self.profile,subject=subject,klass=klass)
                average_tests = weak_cache.subjectTests
                defence_tests = weak_cache.defenceTests
# total_tests is the number of tests the data is based on in
# the cache
                total_ssc_marks = len(weak_cache.testids)
# get the total_arr and all_total_arr to count total number of
# new tests
                total_arr = SSCOnlineMarks.objects.filter(test__creator =
                                                          user,test__sub =
                                                          subject,test__klas__name
                                                         = klass)
                if 'Defence' in subject:
                    all_total_arr = SSCOnlineMarks.objects.filter(test__creator =
                                                                  user,test__sub=
                                                                  'Defence-MultipleSubjects',test__klas__name
                                                             = klass)
                else:
                    all_total_arr = SSCOnlineMarks.objects.filter(test__creator =
                                                                  user,test__sub=
                                                                  'SSCMultipleSections',test__klas__name
                                                             = klass)
                new_test_ids = []
# put test ids into a list from SSCOnline marks queries to
# compare number of tests
                for i in total_arr:
                    new_test_ids.append(i.id)
                for i in all_total_arr:
                    new_test_ids.append(i.id)
                #new_test_ids = list(unique_everseen(new_test_ids))
                new_total_tests_num = len(total_arr) + len(all_total_arr)
# compare number of new tests to number of tests in cache and
# if they are equal then show data from cache
                if total_ssc_marks == len(new_test_ids):
                    categories = weak_cache.categories
                    accuracy = weak_cache.accuracies
                    return list(zip(categories,accuracy))
                else:
# if not equal then only calulate weak areas for new tests
                    new_ids = []
                    old_ids = []
                    test_ids = weak_cache.testids
                    for te in new_test_ids:
                        if te not in test_ids:
                            new_ids.append(te)
                        else:
                            old_ids.append(te)
# get the new weak areas with intensity by sending only the ids
# of new tests
                    arr =\
                    self.online_problematicAreaswithIntensityCache(user,subject,klass,new_ids)
                    quest_categories = helper_weakIntesityAverage(arr)
                    unique, counts = np.unique(quest_categories, return_counts=True)
                    waf = np.asarray((unique, counts)).T
                    arr = np.array(arr)
                    average_cat = []
                    average_percent = []
                    wrong_total = []
                    total_cat = []
# below is calculation of new weak areas saved into overall
# list
                    for i,j in waf:
                        if i in arr[:,0]:
                            ind = np.where(arr==i)
                            now_arr = arr[ind[0],1]
                            average =(int(now_arr[0])/int(j)*100)
                            wrong_total.append(now_arr[0])
                            total_cat.append(j)
                            average_cat.append(i)
                            average_percent.append(average)
                    overall =\
                    list(zip(average_cat,average_percent,wrong_total,total_cat))

# get list of cached data
                    old_cat = weak_cache.categories
                    old_acc = weak_cache.accuracies
                    old_wrong = weak_cache.wrong_total
                    old_total = weak_cache.total_total
                    old_overall =\
                    list(zip(old_cat,old_acc,old_wrong,old_total))

                    new_cat = []
                    new_accuracy = []
                    new_total_wrong = []
                    new_total_total = []
# update the old weak areas by adding in the new weak areas
                    for i,j,k,l in old_overall:
                        for l,m,n,o in overall:
                            if i == l:
                                new_wrong = k + n
                                new_total = l + o
                                average =((new_wrong)/int(new_total)*100)
                                new_cat.append(i)
                                new_accuracy.append(100-average)
                                new_total_wrong.append(new_wrong)
                                new_total_total.append(new_total)
# update the old weak areas by adding categories that were
# not originally in the cached weak areas
                    for l,m,n,o in overall:
                        if l not in old_overall[:,0]:
                            new_cat.append(l)
                            new_accuracy.append(m)
                            new_total_wrong.append(n)
                            new_total_total.append(o)
                    weak_cache.categories = new_cat
                    weak_cache.accuracies = new_accuracy
                    weak_cache.wrong_total = new_total_wrong
                    weak_cache.total_total = new_total_total
                    weak_cache.testids = old_ids + new_ids
                    weak_cache.save()
                    return list(zip(new_cat,new_accuracy))

# this is the normal function when no caching has already been
# done. this doesnot include offline tests.
            except Exception as e:
                print(str(e))
                arr = self.online_problematicAreaswithIntensity(user,subject,klass)
                total_arr = SSCOnlineMarks.objects.filter(test__creator =
                                                          user,test__sub =
                                                          subject,test__klas__name
                                                         = klass)
                if 'Defence' in subject:
                    all_total_arr = SSCOnlineMarks.objects.filter(test__creator =
                                                                  user,test__sub=
                                                                  'Defence-MultipleSubjects',test__klas__name
                                                             = klass)
                else:
                    all_total_arr = SSCOnlineMarks.objects.filter(test__creator =
                                                                  user,test__sub=
                                                                  'SSCMultipleSections',test__klas__name
                                                             = klass)
                #offline_total_arr = SSCOfflineMarks.objects.filter(test__creator =
                #                                                   user,test__sub =
                #                                                   subject,test__klas__name
                #                                                   = klass)
                #all_offline_total_arr =\
                #SSCOfflineMarks.objects.filter(test__creator = user,test__sub =
                #                               'SSCMultipleSections',test__klas__name
                #                               = klass)
                overall = [total_arr ,all_total_arr ]
                overall_ids = []
                for i in overall:
                    for j in i:
                        overall_ids.append(j.id)
                #te_ids = []
                #for i in overall:
                #    for j in i:
                #        te_ids.append(j.test.id)
                #te_ids = list(unique_everseen(te_ids))
                quest_categories = helper_weakIntesityAverage(overall)


                unique, counts = np.unique(quest_categories, return_counts=True)
                waf = np.asarray((unique, counts)).T
                arr = np.array(arr)
                average_cat = []
                average_percent = []
                wrong_total = []
                total_cat = []
                new_weak_areas_cache = TeacherWeakAreasDetailCache()
                for i,j in waf:
                    if i in arr[:,0]:
                        ind = np.where(arr==i)
                        now_arr = arr[ind[0],1]
                        average =(int(now_arr[0])/int(j)*100)
                        wrong_total.append(now_arr[0])
                        total_cat.append(j)
                        average_cat.append(i)
                        average_percent.append(100-average)
                new_weak_areas_cache.teacher = self.profile
                new_weak_areas_cache.klass = klass
                new_weak_areas_cache.subject = subject
                new_weak_areas_cache.categories = average_cat
                new_weak_areas_cache.accuracies = average_percent
                new_weak_areas_cache.wrong_total = wrong_total
                new_weak_areas_cache.total_total = total_cat
                new_weak_areas_cache.subjectTests = len(total_arr)
                new_weak_areas_cache.defenceTests = len(all_total_arr)
                new_weak_areas_cache.testids = overall_ids
                new_weak_areas_cache.save()



                weak_average = list(zip(average_cat,average_percent))
                return weak_average

    def weakAreas_timing(self,user,subject,klass):
        all_questions = []
        all_timing = []
        if self.institution == 'School':
            marks = OnlineMarks.objects.filter(test__sub =
                                               subject,test__creator =
                                            user)
            for om in marks:
                for aq in om.sscansweredquestion_set.all():
                    all_questions.append(aq.quest.topic_category)
                    all_timing.append(aq.time)

        elif self.institution == 'SSC':
            try:
                weak_cache =\
                TeacherWeakAreasTimingCache.objects.get(teacher=self.profile,klass
                                                        = klass,subject =
                                                        subject)
                total_old_tests = len(weak_cache.testids)

                marks = SSCOnlineMarks.objects.filter(test__sub = subject,
                                                      test__creator =
                                                      user)
                if 'Defence' in subject:
                    every_marks = SSCOnlineMarks.objects.filter(test__sub =
                                                            'Defence-MultipleSubjects',test__creator
                                                            = user)
                else:
                    every_marks = SSCOnlineMarks.objects.filter(test__sub =
                                                                'SSCMultipleSections',test__creator
                                                                = user)
                len_marks = len(marks)
                len_every = len(every_marks)
                total_new_tests = len_marks + len_every
                if total_old_tests == total_new_tests:
                    print('old cache')
                    cat = weak_cache.categories
                    time = weak_cache.averagetiming
                    freq = weak_cache.totalFreq

                    return list(zip(cat,time)),list(zip(cat,freq))
                else:
                    print('new cache')
                    new_ids = []
                    for te_id in marks.test.id:
                        if te_id not in old_tests:
                            new_ids.append(te_id)
                    for te_id in every_marks.test.id:
                        if te_id not in old_tests:
                            new_ids.append(te_id)
                all_ids = []
                for ids in marks:
                    all_ids.append(ids.id)
                for ids in every_marks:
                    all_ids.append(ids.id)


                new_marks =[]
                for te_id in new_ids:
                    every_marks = SSCOnlineMarks.objects.filter(test_id =
                                                                te_id)
                    new_marks.append(every_marks)


                for nm in new_marks:
                    for om in nm:
                        for al in om.sscansweredquestion_set.all():
                            if al.quest.section_category == subject:
                                all_questions.append(al.quest.topic_category)
                                all_timing.append(al.time)

                areawise_timing = list(zip(all_questions,all_timing))
                dim1 = list(unique_everseen(all_questions))
                dim3 = []
                dim4 = []
                freq = []
                category =weak_cache.categories
                total_timing = weak_cache.totalTiming
                total_freq = weak_cache.totalFreq
                overall = list(zip(category,total_timing,total_freq))
                final_total_time = []
                final_total_freq = []
                final_total_cat = []
                final_average = []
                for j in dim1:
                    k_val = 0
                    n = 0
                    for x,y in areawise_timing:
                        if j == x and y != -1:
                            k_val += y
                            n += 1
                    for cat,tt,tf in overall:
                        if cat == j:
                            totalTime = tt + k_val
                            tfreq = tf + n
                            final_total_time.append(totalTime)
                            final_total_freq.append(tfreq)
                            final_average.append(float(totalTime/tfreq))
                            final_total_cat.append(cat)



                    dim3.append(j)
                    try:
                        average_time = float(k_val/n)
                        dim4.append(average_time)
                        freq.append(n)
                    except:
                        pass
                timing = list(zip(dim3,dim4))
                freq_list = list(zip(dim3,freq))
                weak_cache.categories = final_total_cat
                weak_cache.averagetiming = final_average
                weak_cache.totalTiming = final_total_time
                weak_cache.totalFreq = final_total_freq
                weak_cache.testids = all_ids
                weak_cache.save()
                return\
            list(zip(final_total_cat,final_average)),list(zip(final_total_cat,final_total_freq))





            except Exception as e:
                print(str(e))
                marks = SSCOnlineMarks.objects.filter(test__sub = subject,
                                                      test__creator =
                                                      user)
                if 'Defence' in subject:
                    every_marks = SSCOnlineMarks.objects.filter(test__sub =
                                                            'Defence-MultipleSubjects',test__creator
                                                            = user)
                else:
                    every_marks = SSCOnlineMarks.objects.filter(test__sub =
                                                                'SSCMultipleSections',test__creator
                                                                = user)
                for om in marks:
                    for aq in om.sscansweredquestion_set.all():
                        all_questions.append(aq.quest.topic_category)
                        all_timing.append(aq.time)
                if every_marks:
                    for om in every_marks:
                        for al in om.sscansweredquestion_set.all():
                            if al.quest.section_category == subject:
                                all_questions.append(al.quest.topic_category)
                                all_timing.append(al.time)
                all_ids = []
                for ids in marks:
                    all_ids.append(ids.id)
                for ids in every_marks:
                    all_ids.append(ids.id)

                areawise_timing = list(zip(all_questions,all_timing))
                dim1 = list(unique_everseen(all_questions))
                dim3 = []
                dim4 = []
                freq = []
                total_cat = []
                total_freq = []
                total_time = []
                for j in dim1:
                    k_val = 0
                    n = 0
                    for x,y in areawise_timing:
                        if j == x and y != -1:
                            k_val += y
                            n += 1
                    total_freq.append(n)
                    total_time.append(k_val)
                    dim3.append(j)
                    try:
                        average_time = float(k_val/n)
                        dim4.append(average_time)
                        freq.append(n)
                    except:
                        pass
                timing = list(zip(dim3,dim4))
                freq_list = list(zip(dim3,freq))
                time_cache = TeacherWeakAreasTimingCache()
                time_cache.averagetiming = dim4
                time_cache.categories = dim3
                time_cache.totalTiming = total_time
                time_cache.totalFreq = total_freq
                time_cache.teacher = self.profile
                time_cache.klass = klass
                time_cache.testids = all_ids
                time_cache.subject = subject
                time_cache.save()
                return timing,freq_list

    def find_classRank(self,li):
        array = np.array(li)
        temp = array.argsort()
        ranks = np.empty(len(array), int)
        ranks[temp] = np.arange(len(array))
        final_rank = []
        for j in ranks:
            final_rank.append(((len(li)-j)))
        return final_rank


    def generate_rankTable(self,test_id,mode=None):
        if mode:
            all_marks = SSCOfflineMarks.objects.filter(test__id = test_id)
        else:
            all_marks = SSCOnlineMarks.objects.filter(test__id = test_id)
        names = []
        totalMarks = []
        scores = []
        percentage = []
        numCorrect = []
        numIncorrect = []
        numSkipped = []
        # get total marks and put in a list
        for i in all_marks:
            names.append(i.student.name)
            totalMarks.append(i.test.max_marks)
            scores.append(i.marks)
            percentage.append((i.marks/i.test.max_marks)*100)
            numCorrect.append(len(i.rightAnswers))
            numIncorrect.append(len(i.wrongAnswers))
            numSkipped.append(len(i.skippedAnswers))
            #right_answers = 0
            #wrong_answers = 0
            #skipped_answers = 0
        # counts number of right,wrong and skipped answers

        rank = self.find_classRank(scores)
        result =\
        list(zip(names,totalMarks,scores,rank,percentage,numCorrect,numIncorrect,numSkipped))
    # save it to database
        rank_table = TestRankTable()
        rank_table.teacher = self.profile
        rank_table.test = SSCKlassTest.objects.get(id = test_id)
        rank_table.names = names
        rank_table.totalMarks = totalMarks
        rank_table.scores = scores
        rank_table.percentage = percentage
        rank_table.numCorrect = numCorrect
        rank_table.numIncorrect = numIncorrect
        rank_table.numSkipped = numSkipped
        rank_table.rank = rank
        rank_table.save()

    def combine_rankTable(self,result):
        names = result.names
        totalMarks = result.totalMarks
        scores = result.scores
        rank = [i for i in result.rank]
        percentage = result.percentage
        numCorrect = result.numCorrect
        numIncorrect = result.numIncorrect
        numSkipped = result.numSkipped
        result =\
        list(zip(names,totalMarks,scores,rank,percentage,numCorrect,numIncorrect,numSkipped))
        result = np.array(result)
        try:
            result = result[result[:,3].argsort()]
        except:
            result = None
        return result

    def combine_rankTableDict(self,result):
        names = result.names
        totalMarks = result.totalMarks
        scores = result.scores
        rank = [i for i in result.rank]
        percentage = result.percentage
        numCorrect = result.numCorrect
        numIncorrect = result.numIncorrect
        numSkipped = result.numSkipped
        result =\
        list(zip(names,totalMarks,scores,rank,percentage,numCorrect,numIncorrect,numSkipped))
        result_dict =\
        {'names':names,'totalMarks':totalMarks,'scores':scores,'rank':rank,'percentage':percentage,'numCorrect':numCorrect,'numIncorrect':numIncorrect,'numSkipped':numSkipped}
        return result_dict
        #result = np.array(result)
        #try:
        #    result = result[result[:,3].argsort()]
        #except:
        #    result = None
        #return result





    def test_taken_subjects(self,user):
        tests = SSCKlassTest.objects.filter(creator=user)
        subs = []
        for te in tests:
            if te.sub != '':
                subs.append(te.sub)
        return list(unique_everseen(subs))

    def pattern_test_taken_subjects(self):
        tests = SSCKlassTest.objects.filter(patternTestCreators = self.profile)
        print(len(tests))
        subs = []
        for te in tests:
            if te.sub != '':
                subs.append(te.sub)
        return list(unique_everseen(subs))





    def change_topicNumbersNames(self,arr,subject):
        names = []
        numbers = []
        if subject == 'English':
            for i in arr:
                if i == '1.1':
                    names.append('Antonym')
                    numbers.append(i)
                elif i == '1.2':
                    names.append('Synonym')
                    numbers.append(i)
                elif i == '1.3':
                    names.append('One word substitution')
                    numbers.append(i)
                elif i == '1.4':
                    names.append('Idioms & Phrases')
                    numbers.append(i)
                elif i == '1.5':
                    names.append('Phrasal Verbs')
                    numbers.append(i)
                elif i == '1.6':
                    names.append('Use of some verbs with particular nouns')
                    numbers.append(i)
                elif i == '1.7':
                    names.append('Tense')
                    numbers.append(i)
                elif i == '2.1':
                    names.append('Noun')
                    numbers.append(i)
                elif i == '2.2':
                    names.append('Pronoun')
                    numbers.append(i)
                elif i == '2.3':
                    names.append('Adjective')
                    numbers.append(i)
                elif i == '2.4':
                    names.append('Articles')
                    numbers.append(i)
                elif i == '2.5':
                    names.append('Verb')
                    numbers.append(i)
                elif i == '2.6':
                    names.append('Adverb')
                    numbers.append(i)
                elif i == '2.7':
                    names.append('Time & Tense')
                    numbers.append(i)
                elif i == '2.8':
                    names.append('Voice')
                    numbers.append(i)
                elif i == '2.9':
                    names.append('Non-Finites')
                    numbers.append(i)
                elif i == '3.1':
                    names.append('Narration')
                    numbers.append(i)
                elif i == '3.2':
                    names.append('Preposition')
                    numbers.append(i)
                elif i == '3.3':
                    names.append('Conjunction')
                    numbers.append(i)
                elif i == '3.4':
                    names.append('Subject verb agreement')
                    numbers.append(i)
                elif i == '3.5':
                    names.append('Common Errors')
                    numbers.append(i)
                elif i == '3.6':
                    names.append('Superfluous Expressions & Slang')
                    numbers.append(i)


            changed = list(zip(names,numbers))
            return changed
        if subject == 'General-Intelligence':
            for i in arr:
                if i == '1.1':
                    names.append('Paper cutting and Folding')
                    numbers.append(i)
                elif i == '1.2':
                    names.append('Mirror and Water Image')
                    numbers.append(i)
                elif i == '1.3':
                    names.append('Embedded Figures')
                    numbers.append(i)
                elif i == '1.4':
                    names.append('Figure Completion')
                    numbers.append(i)
                elif i == '1.5':
                    names.append('Counting of embedded figures')
                    numbers.append(i)
                elif i == '1.6':
                    names.append('Counting of figures')
                    numbers.append(i)
                elif i == '2.1':
                    names.append('Analogy')
                    numbers.append(i)
                elif i == '2.2':
                    names.append('Multiple Analogy')
                    numbers.append(i)
                elif i == '2.3':
                    names.append('Choosing the analogous pair')
                    numbers.append(i)
                elif i == '2.4':
                    names.append('Number analogy (series pattern)')
                    numbers.append(i)
                elif i =='2.5':
                    names.append('Number analogy (missing)')
                    numbers.append(i)
                elif i == '2.6':
                    names.append('Alphabet based analogy')
                    numbers.append(i)
                elif i == '2.7':
                    names.append('Mixed analogy')
                    numbers.append(i)
                elif i == '3.1':
                    names.append('Series Completion (Diagram)')
                    numbers.append(i)
                elif i == '3.2':
                    names.append('Analogy (Diagram)')
                    numbers.append(i)
                elif i == '3.3':
                    names.append('Classification (Diagram)')
                    numbers.append(i)
                elif i == '3.4':
                    names.append('Dice & Boxes')
                    numbers.append(i)
                elif i == '2.8':
                    names.append('Ruled based analogy')
                    numbers.append(i)
                elif i == '2.9':
                    names.append('Alphabet Test')
                    numbers.append(i)
                elif i == '4.1':
                    names.append('Ranking')
                    numbers.append(i)
                elif i == '5.1':
                    names.append('Matrix')
                    numbers.append(i)
                elif i == '6.1':
                    names.append('Word Creation')
                    numbers.append(i)
                elif i == '7.1':
                    names.append('Odd one out')
                    numbers.append(i)
                elif i == '8.1':
                    names.append('Height')
                    numbers.append(i)
                elif i == '9.1':
                    names.append('Direction')
                    numbers.append(i)
                elif i =='10.1':
                    names.append('Statement & Conclusion')
                    numbers.append(i)
                elif i == '11.1':
                    names.append('Venn Diagram')
                    numbers.append(i)
                elif i == '12.1':
                    names.append('Missing number')
                    numbers.append(i)
                elif i == '13.1':
                    names.append('Logical Sequence of words')
                    numbers.append(i)
                elif i == '14.1':
                    names.append('Clock/Time')
                    numbers.append(i)
                elif i == '15.1':
                    names.append('Mathematical Operations')
                    numbers.append(i)
                elif i == '16.1':
                    names.append('Coding Decoding')
                    numbers.append(i)
                elif i == '17.1':
                    names.append('Series Test')
                    numbers.append(i)
                elif i == '18.1':
                    names.append('Syllogism')
                    numbers.append(i)
                elif i == '19.1':
                    names.append('Blood Relation')
                    numbers.append(i)
                elif i == '20.1':
                    names.append('Seating Arrangement')
                    numbers.append(i)
                elif i == '22.1':
                    names.append('Calender Test')
                    numbers.append(i)
                elif i == '28.1':
                    names.append('Symbols & Notations')
                    numbers.append(i)

            changed = list(zip(names,numbers))
            return changed


        if subject == 'Quantitative-Analysis':
            for i in arr:

                if i == '1.1':
                    names.append('Age')
                    numbers.append(i)
                elif i == '2.1':
                    names.append('Alligation')
                    numbers.append(i)
                elif i == '3.1':
                    names.append('Area')
                    numbers.append(i)
                elif i == '4.1':
                    names.append('Average')
                    numbers.append(i)
                elif i == '5.1':
                    names.append('Boat & Stream')
                    numbers.append(i)
                elif i == '6.1':
                    names.append('Discount')
                    numbers.append(i)
                elif i == '7.1':
                    names.append('Fraction')
                    numbers.append(i)
                elif i == '8.1':
                    names.append('LCM & LCF')
                    numbers.append(i)
                elif i == '9.1':
                    names.append('Number System')
                    numbers.append(i)
                elif i == '10.1':
                    names.append('Percentage')
                    numbers.append(i)
                elif i == '11.1':
                    names.append('Pipes & Cistern')
                    numbers.append(i)
                elif i == '12.1':
                    names.append('Profit & Loss')
                    numbers.append(i)
                elif i == '13.1':
                    names.append('Ratio')
                    numbers.append(i)
                elif i == '14.1':
                    names.append('Simple Interest')
                    numbers.append(i)
                elif i == '15.1':
                    names.append('Simplification')
                    numbers.append(i)
                elif i == '16.1':
                    names.append('Speed & Distance')
                    numbers.append(i)
                elif i == '17.1':
                    names.append('Square & Cube root')
                    numbers.append(i)
                elif i == '18.1':
                    names.append('Surds & Indices')
                    numbers.append(i)
                elif i == '19.1':
                    names.append('Time & Work')
                    numbers.append(i)
                elif i == '20.1':
                    names.append('Train')
                    numbers.append(i)
                elif i == '21.1':
                    names.append('Volume')
                    numbers.append(i)
                elif i == '22.1':
                    names.append('Trigonometry')
                    numbers.append(i)
                elif i == '23.1':
                    names.append('Partnership')
                    numbers.append(i)
                elif i == '24.1':
                    names.append('Coumpound Interest')
                    numbers.append(i)
                elif i == '25.1':
                    names.append('Decimals')
                    numbers.append(i)


            changed = list(zip(names,numbers))
            return changed


        if subject == 'General-Knowledge':
            for i in arr:
                if i == '1.1':
                    names.append('Inventions & Innovators')
                    numbers.append(i)
                if i == '2.1':
                    names.append('Bird Sanctuary')
                    numbers.append(i)
                if i == '3.1':
                    names.append('Books & Authors')
                    numbers.append(i)
                if i == '4.1':
                    names.append('Countries, Capitals & Currencies')
                    numbers.append(i)
                if i == '5.1':
                    names.append('Current Affairs')
                    numbers.append(i)
                if i == '6.1':
                    names.append('Economics')
                    numbers.append(i)
                if i == '7.1':
                    names.append('General Science')
                    numbers.append(i)
                if i == '8.1':
                    names.append('Biology')
                    numbers.append(i)
                if i == '9.1':
                    names.append('Chemistry')
                    numbers.append(i)
                if i == '10.1':
                    names.append('Science & Technology')
                    numbers.append(i)
                if i == '11.1':
                    names.append('Physics')
                    numbers.append(i)
                if i == '12.1':
                    names.append('Geography')
                    numbers.append(i)
                if i == '13.1':
                    names.append('National Organizations')
                    numbers.append(i)
                if i == '14.1':
                    names.append('History')
                    numbers.append(i)
                if i == '15.1':
                    names.append('Honors & Awards')
                    numbers.append(i)
                if i == '16.1':
                    names.append('Important Dates')
                    numbers.append(i)
                if i == '17.1':
                    names.append('Indian Agriculture')
                    numbers.append(i)
                if i == '18.1':
                    names.append('Indian Constitution')
                    numbers.append(i)
                if i == '19.1':
                    names.append('Indian Culture')
                    numbers.append(i)
                if i == '20.1':
                    names.append('Indian Museums')
                    numbers.append(i)
                if i == '21.1':
                    names.append('Polity (India)')
                    numbers.append(i)
                if i == '22.1':
                    names.append('Sports')
                    numbers.append(i)
                if i == '23.1':
                    names.append('Superlatives(India)')
                    numbers.append(i)
                if i == '24.1':
                    names.append('Symbols of States (India)')
                    numbers.append(i)
                if i == '25.1':
                    names.append('Tiger Reserve')
                    numbers.append(i)
                if i == '26.1':
                    names.append('UNESCO Word Heritage Sites(India)')
                    numbers.append(i)
                if i == '27.1':
                    names.append('World Organizations')
                    numbers.append(i)
                if i == '28.1':
                    names.append('Polity (World)')
                    numbers.append(i)
            changed = list(zip(names,numbers))
            return changed

        if subject == 'General-Science':
            for i in arr:
                if i == '1.1':
                    names.append('गुरूत्व स्थूल पदार्थ के गुण व प्रकाशन')
                    numbers.append(i)

                if i == '2.1':
                    names.append('लेंस व दर्पण')
                    numbers.append(i)
                if i == '3.1':
                    names.append('आधुनिक भौतिकी')
                    numbers.append(i)
                if i == '4.1':
                    names.append('विमिय तथा द्विविमिय')
                    numbers.append(i)
                if i == '5.1':
                    names.append('कॉमन प्रश्नपत्र भौतिक शास्त्र')
                    numbers.append(i)
                if i == '6.1':
                    names.append('दाब घटाव प्रत्यासा')
                    numbers.append(i)
                if i == '7.1':
                    names.append('ध्वनि')
                    numbers.append(i)
                if i == '8.1':
                    names.append('मात्रक विभाएं मापन')
                    numbers.append(i)
                if i == '9.1':
                    names.append('सदिश तथा अदिश')
                    numbers.append(i)
                if i == '10.1':
                    names.append('कार्य,ऊर्जा व शक्ति')
                    numbers.append(i)
                if i == '11.1':
                    names.append('कोशिका विज्ञान')
                    numbers.append(i)
                if i == '12.1':
                    names.append('पादप जगत')
                    numbers.append(i)
                if i == '13.1':
                    names.append('पादप शरीर क्रिया विज्ञान')
                    numbers.append(i)
                if i == '14.1':
                    names.append('आर्थिक वनस्पति विज्ञान')
                    numbers.append(i)
                if i == '15.1':
                    names.append('जन्तु विज्ञान')
                    numbers.append(i)
                if i == '16.1':
                    names.append('जन्तु उत्तक एवं पोषण')
                    numbers.append(i)
                if i == '17.1':
                    names.append('आनुवांशिक')
                    numbers.append(i)
                if i == '18.1':
                    names.append('मानव स्वास्थ्य एवं रोग')
                    numbers.append(i)
                if i == '19.1':
                    names.append('जैव प्रोद्यौगिक')
                    numbers.append(i)
                if i == '20.1':
                    names.append('कम्प्यूटर एवं सूचना प्रोद्यौगिकी')
                    numbers.append(i)

            changed = list(zip(names,numbers))
            return changed


# categories for GroupX

        if subject == 'Defence-English':
            for i in arr:
                if i == '1.1':
                    names.append('Comprehension')
                    numbers.append(i)
                if i == '2.1':
                    names.append('Judge Comprehension')
                    numbers.append(i)
                if i == '3.1':
                    names.append('Inferences')
                    numbers.append(i)
                if i == '4.1':
                    names.append('Vocabulary')
                    numbers.append(i)
                if i == '5.1':
                    names.append('Composition')
                    numbers.append(i)
                if i == '6.1':
                    names.append('Subject and Verb')
                    numbers.append(i)
                if i == '7.1':
                    names.append('Verb and their use')
                    numbers.append(i)
                if i == '8.1':
                    names.append('Sequence of tenses')
                    numbers.append(i)
                if i == '9.1':
                    names.append('Transformation')
                    numbers.append(i)
                if i == '10.1':
                    names.append('Grammer')
                    numbers.append(i)
                if i == '11.1':
                    names.append('Spellings')
                    numbers.append(i)
                if i == '12.1':
                    names.append('Word formation')
                    numbers.append(i)
                if i == '11.1':
                    names.append('Antonyms& Synonyms')
                    numbers.append(i)
                if i == '11.1':
                    names.append('Word Substitution')
                    numbers.append(i)
                if i == '12.1':
                    names.append('Correct use of words')
                    numbers.append(i)
                if i == '13.1':
                    names.append('Confusing words')
                    numbers.append(i)
                if i == '14.1':
                    names.append('Word order')
                    numbers.append(i)
                if i == '15.1':
                    names.append('Correct use of Adverbs')
                    numbers.append(i)
                if i == '16.1':
                    names.append('Idioms and Phrases')
                    numbers.append(i)
                if i == '17.1':
                    names.append('Use of simple idioms')
                    numbers.append(i)
                if i == '18.1':
                    names.append('Use of common proverbs')
                    numbers.append(i)
                if i == '19.1':
                    names.append('Direct/Indirect sentences')
                    numbers.append(i)
                if i == '20.1':
                    names.append('Direct to Indirect form')
                    numbers.append(i)
                if i == '21.1':
                    names.append('Indirect to Direct')
                    numbers.append(i)
                if i == '22.1':
                    names.append('Active and Passive voice')
                    numbers.append(i)
                if i == '23.1':
                    names.append('Active to Passive voice')
                    numbers.append(i)
                if i == '22.1':
                    names.append('Passive to Active voice')
                    numbers.append(i)
                if i == '50.1':
                    names.append('To be categorized')
                    numbers.append(i)

            return list(zip(names,numbers))


        if subject == 'Defence-Physics':
            for i in arr:
                if i == '1.1':
                    names.append('Unit of Dimension')
                    numbers.append(i)
                if i == '2.1':
                    names.append('Scalers&Vectors')
                    numbers.append(i)
                if i == '3.1':
                    names.append('Motion in straight line')
                    numbers.append(i)
                if i == '4.1':
                    names.append('Law of Motion')
                    numbers.append(i)
                if i == '5.1':
                    names.append('Projectile Motion')
                    numbers.append(i)
                if i == '6.1':
                    names.append('Circular Motion')
                    numbers.append(i)
                if i == '7.1':
                    names.append('Friction ')
                    numbers.append(i)
                if i == '8.1':
                    names.append('Work power & Energy')
                    numbers.append(i)
                if i == '9.1':
                    names.append('Collision')
                    numbers.append(i)
                if i == '10.1':
                    names.append('Rotational motion % Moment of Inertia')
                    numbers.append(i)
                if i == '11.1':
                    names.append('Gravitation')
                    numbers.append(i)
                if i == '12.1':
                    names.append('Elasticity')
                    numbers.append(i)
                if i == '13.1':
                    names.append('Fluid Pressure ')
                    numbers.append(i)
                if i == '14.1':
                    names.append('Viscocity& Flow of fluids')
                    numbers.append(i)
                if i == '15.1':
                    names.append('Surface Tension')
                    numbers.append(i)
                if i == '16.1':
                    names.append('Oscillations')
                    numbers.append(i)
                if i == '17.1':
                    names.append('Thermometry')
                    numbers.append(i)
                if i == '18.1':
                    names.append('Thermal Expansion')
                    numbers.append(i)
                if i == '19.1':
                    names.append('Calorimetry')
                    numbers.append(i)
                if i == '20.1':
                    names.append('Transmission of Heat')
                    numbers.append(i)
                if i == '21.1':
                    names.append('Thermodynamics')
                    numbers.append(i)
                if i == '22.1':
                    names.append('Kinetic Theory of gases')
                    numbers.append(i)
                if i == '23.1':
                    names.append('Wave Motion')
                    numbers.append(i)
                if i == '24.1':
                    names.append('Superposition of waves')
                    numbers.append(i)
                if i == '25.1':
                    names.append('Speed of Sound')
                    numbers.append(i)
                if i == '26.1':
                    names.append('Vibrations in air columns')
                    numbers.append(i)
                if i == '27.1':
                    names.append('Vibration of Strings')
                    numbers.append(i)
                if i == '28.1':
                    names.append('Dopplers Effect')
                    numbers.append(i)
                if i == '29.1':
                    names.append('Musical Sound& Ultra sound')
                    numbers.append(i)
                if i == '30.1':
                    names.append('Electric charge & Electric Field')
                    numbers.append(i)
                if i == '31.1':
                    names.append('Gauss Theorem')
                    numbers.append(i)
                if i == '32.1':
                    names.append('Electric Capacitance')
                    numbers.append(i)
                if i == '33.1':
                    names.append('Electric Conduction')
                    numbers.append(i)
                if i == '34.1':
                    names.append('Ohms Law')
                    numbers.append(i)
                if i == '35.1':
                    names.append('Electromotive force & Electric cell')
                    numbers.append(i)
                if i == '36.1':
                    names.append('Kirchoffs law & wheatstone bridge')
                    numbers.append(i)
                if i == '37.1':
                    names.append('Potentiometer')
                    numbers.append(i)
                if i == '38.1':
                    names.append('Heating effect of current')
                    numbers.append(i)
                if i == '39.1':
                    names.append('Chemical effect of current')
                    numbers.append(i)
                if i == '40.1':
                    names.append('Magnetic effect of current')
                    numbers.append(i)
                if i == '41.1':
                    names.append('Electrical Instruments')
                    numbers.append(i)
                if i == '42.1':
                    names.append('Magnetic Field')
                    numbers.append(i)
                if i == '43.1':
                    names.append('Magnetic effects of matter & terrestrial\
                                    magnetism')
                    numbers.append(i)
                if i == '44.1':
                    names.append('Electromagnetic Induction')
                    numbers.append(i)
                if i == '45.1':
                    names.append('Alternating Current')
                    numbers.append(i)
                if i == '46.1':
                    names.append('Reflection of light')
                    numbers.append(i)
                if i == '47.1':
                    names.append('Refraction of light')
                    numbers.append(i)
                if i == '48.1':
                    names.append('Refraction at Spherical surface & by\
                                    lenses')
                    numbers.append(i)
                if i == '49.1':
                    names.append('Prism & scattering of light')
                    numbers.append(i)
                if i == '50.1':
                    names.append('Optical instruments')
                    numbers.append(i)
                if i == '51.1':
                    names.append('Human eye & defects of vision')
                    numbers.append(i)
                if i == '52.1':
                    names.append('Wave theory of light')
                    numbers.append(i)
                if i == '53.1':
                    names.append('Interferance & Deflection of light')
                    numbers.append(i)
                if i == '54.1':
                    names.append('Polarization of light')
                    numbers.append(i)
                if i == '55.1':
                    names.append('Photometry')
                    numbers.append(i)
                if i == '56.1':
                    names.append('Dual nature of radiation & matter')
                    numbers.append(i)
                if i == '57.1':
                    names.append('Electromagnetic waves')
                    numbers.append(i)
                if i == '58.1':
                    names.append('Structure of Atom')
                    numbers.append(i)
                if i == '59.1':
                    names.append('Radioactivity')
                    numbers.append(i)
                if i == '60.1':
                    names.append('Nuclear fission & fusion')
                    numbers.append(i)
                if i == '61.1':
                    names.append('Semi-conductor,diode & Transistors')
                    numbers.append(i)
                if i == '62.1':
                    names.append('Digital electronics & logic gates')
                    numbers.append(i)

            return list(zip(names,numbers))

        if subject == 'Defence-GK-CA':
            for i in arr:
                if i == '1.1':
                    names.append('General Science')
                    numbers.append(i)
                if i == '1.2':
                    names.append('Civics')
                    numbers.append(i)
                if i == '1.3':
                    names.append('Geography')
                    numbers.append(i)
                if i == '1.4':
                    names.append('Current Events')
                    numbers.append(i)
                if i == '1.5':
                    names.append('History')
                    numbers.append(i)
                if i == '1.6':
                    names.append('Basic Computer Operation')
                    numbers.append(i)
                if i == '1.7':
                    names.append('General Knowledge')
                    numbers.append(i)

            return list(zip(names,numbers))






        if subject == 'GroupX-Maths':
            for i in arr:
                if i == '1.1':
                    names.append('Sets-Relations-Functions')
                    numbers.append(i)
                if i == '2.1':
                    names.append('Trigonometric functions')
                    numbers.append(i)
                if i == '3.1':
                    names.append('Inverse Trigonometric functions')
                    numbers.append(i)
                if i == '4.1':
                    names.append('Complex numbers')
                    numbers.append(i)
                if i == '5.1':
                    names.append('Quadratic eqations')
                    numbers.append(i)
                if i == '6.1':
                    names.append('Sequence & Series')
                    numbers.append(i)
                if i == '7.1':
                    names.append('Permutations')
                    numbers.append(i)
                if i == '8.1':
                    names.append('Combination')
                    numbers.append(i)
                if i == '9.1':
                    names.append('Binomial Theorem')
                    numbers.append(i)
                if i == '10.1':
                    names.append('Coordinate Geometry')
                    numbers.append(i)
                if i == '11.1':
                    names.append('Exponential Series')
                    numbers.append(i)
                if i == '12.1':
                    names.append('Logarithmic Series')
                    numbers.append(i)
                if i == '13.1':
                    names.append('Matrices')
                    numbers.append(i)
                if i == '14.1':
                    names.append('Determinants')
                    numbers.append(i)
                if i == '15.1':
                    names.append('Limit & Continuity')
                    numbers.append(i)
                if i == '16.1':
                    names.append('Differentiation')
                    numbers.append(i)
                if i == '17.1':
                    names.append('Application of Differentiation')
                    numbers.append(i)
                if i == '18.1':
                    names.append('Indefinite Integrals')
                    numbers.append(i)
                if i == '19.1':
                    names.append('Definite Integrals')
                    numbers.append(i)
                if i == '20.1':
                    names.append('Application of Integration')
                    numbers.append(i)
                if i == '21.1':
                    names.append('Diferential Equations')
                    numbers.append(i)
                if i == '22.1':
                    names.append('Probability Statistics')
                    numbers.append(i)
                if i == '23.1':
                    names.append('Properties of Triangle')
                    numbers.append(i)
                if i == '24.1':
                    names.append('Height&Distance')
                    numbers.append(i)



            return list(zip(names,numbers))

        if subject == 'MathsIITJEE10':
            for i in arr:
                if i == '1.1':
                    names.append('All Categories')
                    numbers.append(i)

            return list(zip(names,numbers))

        if subject == 'MathsIITJEE11':
            for i in arr:
                if i == '1.1':
                    names.append('All Categories')
                    numbers.append(i)
            return list(zip(names,numbers))

        if subject == 'MathsIITJEE12':
            for i in arr:
                if i == '1.1':
                    names.append('All Categories')
                    numbers.append(i)

            return list(zip(names,numbers))

        if subject == 'PhysicsIITJEE10':
            for i in arr:
                if i == '1.1':
                    names.append('All Categories')
                    numbers.append(i)
            return list(zip(names,numbers))

        if subject == 'PhysicsIITJEE11':
            for i in arr:
                if i == '1.1':
                    names.append('All Categories')
                    numbers.append(i)

            return list(zip(names,numbers))

        if subject == 'PhysicsIITJEE12':
            for i in arr:
                if i == '1.1':
                    names.append('All Categories')
                    numbers.append(i)
            return list(zip(names,numbers))


        if subject == 'ChemistryIITJEE10':
            for i in arr:
                if i == '1.1':
                    names.append('All Categories')
                    numbers.append(i)

            return list(zip(names,numbers))

        if subject == 'ChemistryIITJEE11':
            for i in arr:
                if i == '1.1':
                    names.append('All Categories')
                    numbers.append(i)
            return list(zip(names,numbers))


        if subject == 'ChemistryIITJEE12':
            for i in arr:
                if i == '1.1':
                    names.append('All Categories')
                    numbers.append(i)
            return list(zip(names,numbers))
# for locopilot
        if subject == 'ElectricalLocoPilot':
            for i in arr:
                if i == '1.1':
                    names.append('चालक,अचालक एवं कुचालक')
                    numbers.append(i)
                if i == '2.1':
                    names.append('बेसिक इलेक्ट्रिकल')
                    numbers.append(i)
                if i == '3.1':
                    names.append('विद्युत सेल')
                    numbers.append(i)
                if i == '4.1':
                    names.append('संधारित्र')
                    numbers.append(i)
                if i == '5.1':
                    names.append('चुम्बक')
                    numbers.append(i)
                if i == '6.1':
                    names.append('डी.सी.जनित्र')
                    numbers.append(i)
                if i == '7.1':
                    names.append('डी.सी.मोटर')
                    numbers.append(i)
                if i == '8.1':
                    names.append('ए.सी थ्योरी')
                    numbers.append(i)
                if i == '9.1':
                    names.append('भू-सम्पर्कन')
                    numbers.append(i)
                if i == '10.1':
                    names.append('विद्युय वायरिंग')
                    numbers.append(i)
                if i == '11.1':
                    names.append('विद्युत मापक यंत्र')
                    numbers.append(i)
                if i == '12.1':
                    names.append('ट्रांसफार्मर')
                    numbers.append(i)
                if i == '13.1':
                    names.append('प्रत्यावर्तक')
                    numbers.append(i)
                if i == '14.1':
                    names.append('तुल्यकालिक प्रेरण')
                    numbers.append(i)
                if i == '15.1':
                    names.append('ए.सी. मोटर')
                    numbers.append(i)
                if i == '16.1':
                    names.append('वाइंडिंग')
                    numbers.append(i)
                if i == '17.1':
                    names.append('विद्युत उत्पादन,ट्रांसमिशन एवं वितरण')
                    numbers.append(i)
                if i == '18.1':
                    names.append('प्रदीप्ति')
                    numbers.append(i)
                if i == '19.1':
                    names.append('इलेक्ट्रिक्स')
                    numbers.append(i)
                if i == '20.1':
                    names.append('व्यावसायिक एवं सावधानियां')
                    numbers.append(i)
            return list(zip(names,numbers))
        if subject == 'FitterLocoPilot':
            for i in arr:
                if i == '1.1':
                    names.append('Introduction')
                    numbers.append(i)
                if i == '2.1':
                    names.append('Fitter tools')
                    numbers.append(i)
                if i == '3.1':
                    names.append('Sheet Metal Shop')
                    numbers.append(i)
                if i == '4.1':
                    names.append('Welding Theory')
                    numbers.append(i)
                if i == '5.1':
                    names.append('Soldering And Brazing')
                    numbers.append(i)
                if i == '6.1':
                    names.append('Physical and Mechanical Properties of Metals')
                    numbers.append(i)
                if i == '7.1':
                    names.append('Heat Treatment')
                    numbers.append(i)
                if i == '8.1':
                    names.append('Bearings')
                    numbers.append(i)
                if i == '9.1':
                    names.append('Drilling Machine')
                    numbers.append(i)
                if i == '10.1':
                    names.append('Lathe Machine')
                    numbers.append(i)
                if i == '11.1':
                    names.append('Grinding Machine')
                    numbers.append(i)
                if i == '12.1':
                    names.append('Power Transmission')
                    numbers.append(i)
                if i == '13.1':
                    names.append('Pipe And Pipe Fitting')
                    numbers.append(i)
                if i == '14.1':
                    names.append('Screw Threads')
                    numbers.append(i)
                if i == '15.1':
                    names.append('Gauge')
                    numbers.append(i)
                if i == '16.1':
                    names.append('Limits,Fits And Tolerance')
                    numbers.append(i)
                if i == '17.1':
                    names.append('Other Important Questions')
                    numbers.append(i)
                if i == '18.1':
                    names.append('Previous Year Exams Questions')
                    numbers.append(i)

            return list(zip(names,numbers))
        if subject == 'Civil_Loco_Pilot_Tech':
            for i in arr:
                if i == '2.1':
                    names.append('Land Surveying Basic Principal And Classification')
                    numbers.append(i)
                if i == '2.2':
                    names.append('Chain Surveying')
                    numbers.append(i)
                if i == '2.3':
                    names.append('Compass Surveying')
                    numbers.append(i)
                if i == '2.4':
                    names.append('Levelling')
                    numbers.append(i)
                if i == '2.5':
                    names.append('Minor Instruments')
                    numbers.append(i)
                if i == '2.6':
                    names.append('Computation Of Land')
                    numbers.append(i)
                if i == '2.7':
                    names.append('Plane Table Survey')
                    numbers.append(i)
                if i == '2.8':
                    names.append('Contours And Contouring')
                    numbers.append(i)
                if i == '2.9':
                    names.append('Theodolite Survey')
                    numbers.append(i)
                if i == '50.1':
                    names.append('Curve And Curves Setting')
                    numbers.append(i)
                if i == '12.1':
                    names.append('Bending moment and sheer force')
                    numbers.append(i)
                if i == '12.2':
                    names.append('Bending and sheer stress')
                    numbers.append(i)
                if i == '12.3':
                    names.append('Combined direct and bending stress')
                    numbers.append(i)
                if i == '12.4':
                    names.append('Slope and deflection')
                    numbers.append(i)
                if i == '12.5':
                    names.append('Principal stress and principle planes')
                    numbers.append(i)
                if i == '12.6':
                    names.append('Columns and struts')
                    numbers.append(i)
                if i == '12.7':
                    names.append('Trosion')
                    numbers.append(i)
                if i == '13.1':
                    names.append('Rivet Connection')
                    numbers.append(i)
                if i == '13.2':
                    names.append('Weld Connection')
                    numbers.append(i)
                if i == '13.3':
                    names.append('Tension Members')
                    numbers.append(i)
                if i == '13.4':
                    names.append('Compression Member')
                    numbers.append(i)
                if i == '13.5':
                    names.append('Steel Beams')
                    numbers.append(i)
                if i == '13.6':
                    names.append('Column base and Foundation')
                    numbers.append(i)
                if i == '13.7':
                    names.append('Steel root of trusses')
                    numbers.append(i)


            return list(zip(names,numbers))

        if subject == 'LocoPilot_Diesel':
            for i in arr:
                if i == '1.1':
                    names.append('Introduction to Engine & Development')
                    numbers.append(i)
                if i == '2.1':
                    names.append('Cylinder Head & Valve Assembly')
                    numbers.append(i)
                if i == '3.1':
                    names.append('Piston & Connecting Rod')
                    numbers.append(i)
                if i == '4.1':
                    names.append('Crank Shaft,Cam Shaft Fly Wheel & Bearing')
                    numbers.append(i)
                if i == '5.1':
                    names.append('Gas Turbine Marine & Statonery Engine')
                    numbers.append(i)
                if i == '6.1':
                    names.append('Cooling & Snake System')
                    numbers.append(i)
                if i == '7.1':
                    names.append('Intake & Exhaust System')
                    numbers.append(i)
                if i == '8.1':
                    names.append('Diesel Fuel Supply System')
                    numbers.append(i)
                if i == '9.1':
                    names.append('Emission Charging & Starting System')
                    numbers.append(i)
                if i == '10.1':
                    names.append('Troubleshooting')
                    numbers.append(i)

            return list(zip(names,numbers))


# for knimbus subjects
        if subject == 'Design and analysis of algorithm':
            for i in arr:
                if i == '1.1':
                    names.append('Divide and Conquer')
                    numbers.append(i)
                if i == '2.1':
                    names.append('Dynamic Programming')
                    numbers.append(i)
                if i == '3.1':
                    names.append('Introduction')
                    numbers.append(i)
                if i == '4.1':
                    names.append('Greedy Method')
                    numbers.append(i)
            return list(zip(names,numbers))

        if subject == 'CAT_Quantitative_Aptitude':
            for i in arr:
                if i == '11.1':
                    names.append('Geometry')
                    numbers.append(i)

            return list(zip(names,numbers))



    def change_topicNumbersNamesWeakAreas(self,arr,subject):
        names = []
        numbers = []
        if subject == 'English':
            for i,j in arr:
                if i == '1.1':
                    names.append('Antonym')
                    numbers.append(j)
                elif i == '1.2':
                    names.append('Synonym')
                    numbers.append(j)
                elif i == '1.3':
                    names.append('One word substitution')
                    numbers.append(j)
                elif i == '1.4':
                    names.append('Idioms & Phrases')
                    numbers.append(j)
                elif i == '1.5':
                    names.append('Phrasal Verbs')
                    numbers.append(j)
                elif i == '1.6':
                    names.append('Use of some verbs with particular nouns')
                    numbers.append(j)
                elif i == '1.7':
                    names.append('Tense')
                    numbers.append(j)
                elif i == '2.1':
                    names.append('Noun')
                    numbers.append(j)
                elif i == '2.2':
                    names.append('Pronoun')
                    numbers.append(j)
                elif i == '2.3':
                    names.append('Adjective')
                    numbers.append(j)
                elif i == '2.4':
                    names.append('Articles')
                    numbers.append(j)
                elif i == '2.5':
                    names.append('Verb')
                    numbers.append(j)
                elif i == '2.6':
                    names.append('Adverb')
                    numbers.append(j)
                elif i == '2.7':
                    names.append('Time & Tense')
                    numbers.append(j)
                elif i == '2.8':
                    names.append('Voice')
                    numbers.append(j)
                elif i == '2.9':
                    names.append('Non-Finites')
                    numbers.append(j)
                elif i == '3.1':
                    names.append('Narration')
                    numbers.append(j)
                elif i == '3.2':
                    names.append('Preposition')
                    numbers.append(j)
                elif i == '3.3':
                    names.append('Conjunction')
                    numbers.append(j)
                elif i == '3.4':
                    names.append('Subject verb agreement')
                    numbers.append(j)
                elif i == '3.5':
                    names.append('Common Errors')
                    numbers.append(j)
                elif i == '3.6':
                    names.append('Superfluous Expressions & Slang')
                    numbers.append(j)



            changed = list(zip(names,numbers))
            return changed
        if subject == 'General-Intelligence':
            for i,j in arr:
                if i == '1.1':
                    names.append('Paper cutting and Folding')
                    numbers.append(j)
                elif i == '1.2':
                    names.append('Mirror and Water Image')
                    numbers.append(j)
                elif i == '1.3':
                    names.append('Embedded Figures')
                    numbers.append(j)
                elif i == '1.4':
                    names.append('Figure Completion')
                    numbers.append(j)
                elif i == '1.5':
                    names.append('Counting of embedded figures')
                    numbers.append(j)
                elif i == '1.6':
                    names.append('Counting of figures')
                    numbers.append(j)
                elif i == '2.1':
                    names.append('Analogy')
                    numbers.append(j)
                elif i == '2.2':
                    names.append('Multiple Analogy')
                    numbers.append(j)
                elif i == '2.3':
                    names.append('Choosing the analogous pair')
                    numbers.append(j)
                elif i == '2.4':
                    names.append('Number analogy (series pattern)')
                    numbers.append(j)
                elif i =='2.5':
                    names.append('Number analogy (missing)')
                    numbers.append(j)
                elif i == '2.6':
                    names.append('Alphabet based analogy')
                    numbers.append(j)
                elif i == '2.7':
                    names.append('Mixed analogy')
                    numbers.append(j)
                elif i == '3.1':
                    names.append('Series Completion (Diagram)')
                    numbers.append(j)
                elif i == '3.2':
                    names.append('Analogy (Diagram)')
                    numbers.append(j)
                elif i == '3.3':
                    names.append('Classification (Diagram)')
                    numbers.append(j)
                elif i == '3.4':
                    names.append('Dice & Boxes')
                    numbers.append(j)
                elif i == '2.8':
                    names.append('Ruled based analogy')
                    numbers.append(j)
                elif i == '2.9':
                    names.append('Alphabet Test')
                    numbers.append(j)
                elif i == '4.1':
                    names.append('Ranking')
                    numbers.append(j)
                elif i == '5.1':
                    names.append('Matrix')
                    numbers.append(j)
                elif i == '6.1':
                    names.append('Word Creation')
                    numbers.append(j)
                elif i == '7.1':
                    names.append('Odd one out')
                    numbers.append(j)
                elif i == '8.1':
                    names.append('Height')
                    numbers.append(j)
                elif i == '9.1':
                    names.append('Direction')
                    numbers.append(j)
                elif i =='10.1':
                    names.append('Statement & Conclusion')
                    numbers.append(j)
                elif i == '11.1':
                    names.append('Venn Diagram')
                    numbers.append(j)
                elif i == '12.1':
                    names.append('Missing number')
                    numbers.append(j)
                elif i == '13.1':
                    names.append('Logical Sequence of words')
                    numbers.append(j)
                elif i == '14.1':
                    names.append('Clock/Time')
                    numbers.append(j)
                elif i == '15.1':
                    names.append('Mathematical Operations')
                    numbers.append(j)
                elif i == '16.1':
                    names.append('Coding Decoding')
                    numbers.append(j)
                elif i == '17.1':
                    names.append('Series Test')
                    numbers.append(j)
                elif i == '18.1':
                    names.append('Syllogism')
                    numbers.append(j)
                elif i == '19.1':
                    names.append('Blood Relation')
                    numbers.append(j)
                elif i == '20.1':
                    names.append('Seating Arrangement')
                    numbers.append(j)
                elif i == '22.1':
                    names.append('Calender Test')
                    numbers.append(j)
                elif i == '28.1':
                    names.append('Symbols & Notations')
                    numbers.append(j)




            changed = list(zip(names,numbers))
            return changed
        if subject == 'Quantitative-Analysis':
            for i,j in arr:

                if i == '1.1':
                    names.append('Age')
                    numbers.append(j)
                elif i == '2.1':
                    names.append('Alligation')
                    numbers.append(j)
                elif i == '3.1':
                    names.append('Area')
                    numbers.append(j)
                elif i == '4.1':
                    names.append('Average')
                    numbers.append(j)
                elif i == '5.1':
                    names.append('Boat & Stream')
                    numbers.append(j)
                elif i == '6.1':
                    names.append('Discount')
                    numbers.append(j)
                elif i == '7.1':
                    names.append('Fraction')
                    numbers.append(j)
                elif i == '8.1':
                    names.append('LCM & LCF')
                    numbers.append(j)
                elif i == '9.1':
                    names.append('Number System')
                    numbers.append(j)
                elif i == '10.1':
                    names.append('Percentage')
                    numbers.append(j)
                elif i == '11.1':
                    names.append('Pipes & Cistern')
                    numbers.append(j)
                elif i == '12.1':
                    names.append('Profit & Loss')
                    numbers.append(j)
                elif i == '13.1':
                    names.append('Ratio')
                    numbers.append(j)
                elif i == '14.1':
                    names.append('Simple Interest')
                    numbers.append(j)
                elif i == '15.1':
                    names.append('Simplification')
                    numbers.append(j)
                elif i == '16.1':
                    names.append('Speed & Distance')
                    numbers.append(j)
                elif i == '17.1':
                    names.append('Square & Cube root')
                    numbers.append(j)
                elif i == '18.1':
                    names.append('Surds & Indices')
                    numbers.append(j)
                elif i == '19.1':
                    names.append('Time & Work')
                    numbers.append(j)
                elif i == '20.1':
                    names.append('Train')
                    numbers.append(j)
                elif i == '21.1':
                    names.append('Volume')
                    numbers.append(j)
                elif i == '22.1':
                    names.append('Trigonometry')
                    numbers.append(j)
                elif i == '23.1':
                    names.append('Partnership')
                    numbers.append(j)
                elif i == '24.1':
                    names.append('Compound Interest')
                    numbers.append(j)
                elif i == '25.1':
                    names.append('Decimals')
                    numbers.append(j)


            changed = list(zip(names,numbers))
            return changed
        if subject == 'General-Knowledge':
            for i,j in arr:
                if i == '1.1':
                    names.append('Inventions & Innovators')
                    numbers.append(j)
                if i == '2.1':
                    names.append('Bird Sanctuary')
                    numbers.append(j)
                if i == '3.1':
                    names.append('Books & Authors')
                    numbers.append(j)
                if i == '4.1':
                    names.append('Countries, Capitals & Currencies')
                    numbers.append(j)
                if i == '5.1':
                    names.append('Current Affairs')
                    numbers.append(j)
                if i == '6.1':
                    names.append('Economics')
                    numbers.append(j)
                if i == '7.1':
                    names.append('General Science')
                    numbers.append(j)
                if i == '8.1':
                    names.append('Biology')
                    numbers.append(j)
                if i == '9.1':
                    names.append('Chemistry')
                    numbers.append(j)
                if i == '10.1':
                    names.append('Science & Technology')
                    numbers.append(j)
                if i == '11.1':
                    names.append('Physics')
                    numbers.append(j)
                if i == '12.1':
                    names.append('Geography')
                    numbers.append(j)
                if i == '13.1':
                    names.append('National Organizations')
                    numbers.append(j)
                if i == '14.1':
                    names.append('History')
                    numbers.append(j)
                if i == '15.1':
                    names.append('Honors & Awards')
                    numbers.append(j)
                if i == '16.1':
                    names.append('Important Dates')
                    numbers.append(j)
                if i == '17.1':
                    names.append('Indian Agriculture')
                    numbers.append(j)
                if i == '18.1':
                    names.append('Indian Constitution')
                    numbers.append(j)
                if i == '19.1':
                    names.append('Indian Culture')
                    numbers.append(j)
                if i == '20.1':
                    names.append('Indian Museums')
                    numbers.append(j)
                if i == '21.1':
                    names.append('Polity (India)')
                    numbers.append(j)
                if i == '22.1':
                    names.append('Sports')
                    numbers.append(j)
                if i == '23.1':
                    names.append('Superlatives(India)')
                    numbers.append(j)
                if i == '24.1':
                    names.append('Symbols of States (India)')
                    numbers.append(j)
                if i == '25.1':
                    names.append('Tiger Reserve')
                    numbers.append(j)
                if i == '26.1':
                    names.append('UNESCO Word Heritage Sites(India)')
                    numbers.append(j)
                if i == '27.1':
                    names.append('World Organizations')
                    numbers.append(j)
                if i == '28.1':
                    names.append('Polity (World)')
                    numbers.append(j)
            changed = list(zip(names,numbers))
            return changed


        if subject == 'General-Science':
            for i,j in arr:
                if i == '1.1':
                    names.append('गुरूत्व स्थूल पदार्थ के गुण व प्रकाशन')
                    numbers.append(j)

                if i == '2.1':
                    names.append('लेंस व दर्पण')
                    numbers.append(j)
                if i == '3.1':
                    names.append('आधुनिक भौतिकी')
                    numbers.append(j)
                if i == '4.1':
                    names.append('विमिय तथा द्विविमिय')
                    numbers.append(j)
                if i == '5.1':
                    names.append('कॉमन प्रश्नपत्र भौतिक शास्त्रा')
                    numbers.append(j)
                if i == '6.1':
                    names.append('दाब घटाव प्रत्यासा')
                    numbers.append(j)
                if i == '7.1':
                    names.append('ध्वनि')
                    numbers.append(j)
                if i == '8.1':
                    names.append('मात्रक विभाएं मापन')
                    numbers.append(j)
                if i == '9.1':
                    names.append('सदिश तथा अदिश')
                    numbers.append(j)
                if i == '10.1':
                    names.append('कार्य,ऊर्जा व शक्ति')
                    numbers.append(j)
                if i == '11.1':
                    names.append('कोशिका विज्ञान')
                    numbers.append(j)
                if i == '12.1':
                    names.append('पादप जगत')
                    numbers.append(j)
                if i == '13.1':
                    names.append('पादप शरीर क्रिया विज्ञान')
                    numbers.append(j)
                if i == '14.1':
                    names.append('आर्थिक वनस्पति विज्ञान')
                    numbers.append(j)
                if i == '15.1':
                    names.append('जन्तु विज्ञान')
                    numbers.append(j)
                if i == '16.1':
                    names.append('जन्तु उत्तक एवं पोषण')
                    numbers.append(j)
                if i == '17.1':
                    names.append('आनुवांशिक')
                    numbers.append(j)
                if i == '18.1':
                    names.append('मानव स्वास्थ्य एवं रोग')
                    numbers.append(j)
                if i == '19.1':
                    names.append('जैव प्रोद्यौगिक')
                    numbers.append(j)
                if i == '20.1':
                    names.append('कम्प्यूटर एवं सूचना प्रोद्यौगिकी')
                    numbers.append(j)

            changed = list(zip(names,numbers))
            return changed


# categories for GroupX

        if subject == 'Defence-English':
            for i,j in arr:
                if i == '1.1':
                    names.append('Comprehension')
                    numbers.append(j)
                if i == '2.1':
                    names.append('Judge Comprehension')
                    numbers.append(j)
                if i == '3.1':
                    names.append('Inferences')
                    numbers.append(j)
                if i == '4.1':
                    names.append('Vocabulary')
                    numbers.append(j)
                if i == '5.1':
                    names.append('Composition')
                    numbers.append(j)
                if i == '6.1':
                    names.append('Subject and Verb')
                    numbers.append(j)
                if i == '7.1':
                    names.append('Verb and their use')
                    numbers.append(j)
                if i == '8.1':
                    names.append('Sequence of tenses')
                    numbers.append(j)
                if i == '9.1':
                    names.append('Transformation')
                    numbers.append(j)
                if i == '10.1':
                    names.append('Grammer')
                    numbers.append(j)
                if i == '11.1':
                    names.append('Spellings')
                    numbers.append(j)
                if i == '12.1':
                    names.append('Word formation')
                    numbers.append(j)
                if i == '11.1':
                    names.append('Antonyms& Synonyms')
                    numbers.append(j)
                if i == '11.1':
                    names.append('Word Substitution')
                    numbers.append(j)
                if i == '12.1':
                    names.append('Correct use of words')
                    numbers.append(j)
                if i == '13.1':
                    names.append('Confusing words')
                    numbers.append(j)
                if i == '14.1':
                    names.append('Word order')
                    numbers.append(j)
                if i == '15.1':
                    names.append('Correct use of Adverbs')
                    numbers.append(j)
                if i == '16.1':
                    names.append('Idioms and Phrases')
                    numbers.append(j)
                if i == '17.1':
                    names.append('Use of simple idioms')
                    numbers.append(j)
                if i == '18.1':
                    names.append('Use of common proverbs')
                    numbers.append(j)
                if i == '19.1':
                    names.append('Direct/Indirect sentences')
                    numbers.append(j)
                if i == '20.1':
                    names.append('Direct to Indirect form')
                    numbers.append(j)
                if i == '21.1':
                    names.append('Indirect to Direct')
                    numbers.append(j)
                if i == '22.1':
                    names.append('Active and Passive voice')
                    numbers.append(j)
                if i == '23.1':
                    names.append('Active to Passive voice')
                    numbers.append(j)
                if i == '22.1':
                    names.append('Passive to Active voice')
                    numbers.append(j)
                if i == '50.1':
                    names.append('To be categorized')
                    numbers.append(j)

            changed = list(zip(names,numbers))
            return changed

        if subject == 'Defence-Physics':
            for i,j in arr:
                if i == '1.1':
                    names.append('Unit of Dimension')
                    numbers.append(j)
                if i == '2.1':
                    names.append('Scalers&Vectors')
                    numbers.append(j)
                if i == '3.1':
                    namedarr.append('Motion in straight line')
                    numbers.append(j)
                if i == '4.1':
                    names.append('Law of Motion')
                    numbers.append(j)
                if i == '5.1':
                    names.append('Projectile Motion')
                    numbers.append(j)
                if i == '6.1':
                    names.append('Circular Motion')
                    numbers.append(j)
                if i == '7.1':
                    names.append('Friction ')
                    numbers.append(j)
                if i == '8.1':
                    names.append('Work power & Energy')
                    numbers.append(j)
                if i == '9.1':
                    names.append('Collision')
                    numbers.append(j)
                if i == '10.1':
                    names.append('Rotational motion % Moment of Inertia')
                    numbers.append(j)
                if i == '11.1':
                    names.append('Gravitation')
                    numbers.append(j)
                if i == '12.1':
                    names.append('Elasticity')
                    numbers.append(j)
                if i == '13.1':
                    names.append('Fluid Pressure ')
                    numbers.append(j)
                if i == '14.1':
                    names.append('Viscocity& Flow of fluids')
                    numbers.append(j)
                if i == '15.1':
                    names.append('Surface Tension')
                    numbers.append(j)
                if i == '16.1':
                    names.append('Oscillations')
                    numbers.append(j)
                if i == '17.1':
                    names.append('Thermometry')
                    numbers.append(j)
                if i == '18.1':
                    names.append('Thermal Expansion')
                    numbers.append(j)
                if i == '19.1':
                    names.append('Calorimetry')
                    numbers.append(j)
                if i == '20.1':
                    names.append('Transmission of Heat')
                    numbers.append(j)
                if i == '21.1':
                    names.append('Thermodynamics')
                    numbers.append(j)
                if i == '22.1':
                    names.append('Kinetic Theory of gases')
                    numbers.append(j)
                if i == '23.1':
                    names.append('Wave Motion')
                    numbers.append(j)
                if i == '24.1':
                    names.append('Superposition of waves')
                    numbers.append(j)
                if i == '25.1':
                    names.append('Speed of Sound')
                    numbers.append(j)
                if i == '26.1':
                    names.append('Vibrations in air columns')
                    numbers.append(j)
                if i == '27.1':
                    names.append('Vibration of Strings')
                    numbers.append(j)
                if i == '28.1':
                    names.append('Dopplers Effect')
                    numbers.append(j)
                if i == '29.1':
                    names.append('Musical Sound& Ultra sound')
                    numbers.append(j)
                if i == '30.1':
                    names.append('Electric charge & Electric Field')
                    numbers.append(j)
                if i == '31.1':
                    names.append('Gauss Theorem')
                    numbers.append(j)
                if i == '32.1':
                    names.append('Electric Capacitance')
                    numbers.append(j)
                if i == '33.1':
                    names.append('Electric Conduction')
                    numbers.append(j)
                if i == '34.1':
                    names.append('Ohms Law')
                    numbers.append(j)
                if i == '35.1':
                    names.append('Electromotive force & Electric cell')
                    numbers.append(j)
                if i == '36.1':
                    names.append('Kirchoffs law & wheatstone bridge')
                    numbers.append(j)
                if i == '37.1':
                    names.append('Potentiometer')
                    numbers.append(j)
                if i == '38.1':
                    names.append('Heating effect of current')
                    numbers.append(j)
                if i == '39.1':
                    names.append('Chemical effect of current')
                    numbers.append(j)
                if i == '40.1':
                    names.append('Magnetic effect of current')
                    numbers.append(j)
                if i == '41.1':
                    names.append('Electrical Instruments')
                    numbers.append(j)
                if i == '42.1':
                    names.append('Magnetic Field')
                    numbers.append(j)
                if i == '43.1':
                    names.append('Magnetic effects of matter & terrestrial\
                                    magnetism')
                    numbers.append(j)
                if i == '44.1':
                    names.append('Electromagnetic Induction')
                    numbers.append(j)
                if i == '45.1':
                    names.append('Alternating Current')
                    numbers.append(j)
                if i == '46.1':
                    names.append('Reflection of light')
                    numbers.append(j)
                if i == '47.1':
                    names.append('Refraction of light')
                    numbers.append(j)
                if i == '48.1':
                    names.append('Refraction at Spherical surface & by\
                                    lenses')
                    numbers.append(j)
                if i == '49.1':
                    names.append('Prism & scattering of light')
                    numbers.append(j)
                if i == '50.1':
                    names.append('Optical instruments')
                    numbers.append(j)
                if i == '51.1':
                    names.append('Human eye & defects of vision')
                    numbers.append(j)
                if i == '52.1':
                    names.append('Wave theory of light')
                    numbers.append(j)
                if i == '53.1':
                    names.append('Interferance & Deflection of light')
                    numbers.append(j)
                if i == '54.1':
                    names.append('Polarization of light')
                    numbers.append(j)
                if i == '55.1':
                    names.append('Photometry')
                    numbers.append(j)
                if i == '56.1':
                    names.append('Dual nature of radiation & matter')
                    numbers.append(j)
                if i == '57.1':
                    names.append('Electromagnetic waves')
                    numbers.append(j)
                if i == '58.1':
                    names.append('Structure of Atom')
                    numbers.append(j)
                if i == '59.1':
                    names.append('Radioactivity')
                    numbers.append(j)
                if i == '60.1':
                    names.append('Nuclear fission & fusion')
                    numbers.append(j)
                if i == '61.1':
                    names.append('Semi-conductor,diode & Transistors')
                    numbers.append(j)
                if i == '62.1':
                    names.append('Digital electronics & logic gates')
                    numbers.append(j)

            return list(zip(names,numbers))
        if subject == 'Defence-GK-CA':
            for i,j in arr:
                if i == '1.1':
                    names.append('General Science')
                    numbers.append(j)
                if i == '1.2':
                    names.append('Civics')
                    numbers.append(j)
                if i == '1.3':
                    names.append('Geography')
                    numbers.append(j)
                if i == '1.4':
                    names.append('Current Events')
                    numbers.append(j)
                if i == '1.5':
                    names.append('History')
                    numbers.append(j)
                if i == '1.6':
                    names.append('Basic Computer Operation')
                    numbers.append(j)
                if i == '1.7':
                    names.append('General Knowledge')
                    numbers.append(j)

            return list(zip(names,numbers))






        if subject == 'GroupX-Maths':
            for i,j in arr:
                if i == '1.1':
                    names.append('Sets-Relations-Functions')
                    numbers.append(j)
                if i == '2.1':
                    names.append('Trigonometric functions')
                    numbers.append(j)
                if i == '3.1':
                    names.append('Inverse Trigonometric functions')
                    numbers.append(j)
                if i == '4.1':
                    names.append('Complex numbers')
                    numbers.append(j)
                if i == '5.1':
                    names.append('Quadratic eqations')
                    numbers.append(j)
                if i == '6.1':
                    names.append('Sequence & Series')
                    numbers.append(j)
                if i == '7.1':
                    names.append('Permutations')
                    numbers.append(j)
                if i == '8.1':
                    names.append('Combination')
                    numbers.append(j)
                if i == '9.1':
                    names.append('Binomial Theorem')
                    numbers.append(j)
                if i == '10.1':
                    names.append('Coordinate Geometry')
                    numbers.append(j)
                if i == '11.1':
                    names.append('Exponential Series')
                    numbers.append(j)
                if i == '12.1':
                    names.append('Logarithmic Series')
                    numbers.append(j)
                if i == '13.1':
                    names.append('Matrices')
                    numbers.append(j)
                if i == '14.1':
                    names.append('Determinants')
                    numbers.append(j)
                if i == '15.1':
                    names.append('Limit & Continuity')
                    numbers.append(j)
                if i == '16.1':
                    names.append('Differentiation')
                    numbers.append(j)
                if i == '17.1':
                    names.append('Application of Differentiation')
                    numbers.append(j)
                if i == '18.1':
                    names.append('Indefinite Integrals')
                    numbers.append(j)
                if i == '19.1':
                    names.append('Definite Integrals')
                    numbers.append(j)
                if i == '20.1':
                    names.append('Application of Integration')
                    numbers.append(j)
                if i == '21.1':
                    names.append('Diferential Equations')
                    numbers.append(j)
                if i == '22.1':
                    names.append('Probability Statistics')
                    numbers.append(j)
                if i == '23.1':
                    names.append('Properties of Triangle')
                    numbers.append(j)
                if i == '24.1':
                    names.append('Height&Distance')
                    numbers.append(j)

            changed = list(zip(names,numbers))
            return changed

        if subject == 'MathsIITJEE10':
            for i,j in arr:
                if i == '1.1':
                    names.append('All Categories')
                    numbers.append(j)

            return list(zip(names,numbers))
        if subject == 'MathsIITJEE11':
            for i,j in arr:
                if i == '1.1':
                    names.append('All Categories')
                    numbers.append(j)
            return list(zip(names,numbers))

        if subject == 'MathsIITJEE12':
            for i,j in arr:
                if i == '1.1':
                    names.append('All Categories')
                    numbers.append(j)

            return list(zip(names,numbers))
        if subject == 'PhysicsIITJEE10':
            for i,j in arr:
                if i == '1.1':
                    names.append('All Categories')
                    numbers.append(j)
            return list(zip(names,numbers))

        if subject == 'PhysicsIITJEE11':
            for i,j in arr:
                if i == '1.1':
                    names.append('All Categories')
                    numbers.append(j)

            return list(zip(names,numbers))
        if subject == 'PhysicsIITJEE12':
            for i in arr:
                if i == '1.1':
                    names.append('All Categories')
                    numbers.append(i)
            return list(zip(names,numbers))

        if subject == 'ChemistryIITJEE10':
            for i in arr:
                if i == '1.1':
                    names.append('All Categories')
                    numbers.append(i)

            return list(zip(names,numbers))
        if subject == 'ChemistryIITJEE11':
            for i in arr:
                if i == '1.1':
                    names.append('All Categories')
                    numbers.append(i)
            return list(zip(names,numbers))

        if subject == 'ChemistryIITJEE12':
            for i in arr:
                if i == '1.1':
                    names.append('All Categories')
                    numbers.append(i)
            return list(zip(names,numbers))

# for locopilot subjects
        if subject == 'ElectricalLocoPilot':
            for i,j in arr:
                if i == '1.1':
                    names.append('चालक,अचालक एवं कुचालक')
                    numbers.append(j)
                if i == '2.1':
                    names.append('बेसिक इलेक्ट्रिकल')
                    numbers.append(j)
                if i == '3.1':
                    names.append('विद्युत सेल')
                    numbers.append(j)
                if i == '4.1':
                    names.append('संधारित्र')
                    numbers.append(j)
                if i == '5.1':
                    names.append('चुम्बक')
                    numbers.append(j)
                if i == '6.1':
                    names.append('डी.सी.जनित्र')
                    numbers.append(j)
                if i == '7.1':
                    names.append('डी.सी.मोटर')
                    numbers.append(j)
                if i == '8.1':
                    names.append('ए.सी थ्योरी')
                    numbers.append(j)
                if i == '9.1':
                    names.append('भू-सम्पर्कन')
                    numbers.append(j)
                if i == '10.1':
                    names.append('विद्युय वायरिंग')
                    numbers.append(j)
                if i == '11.1':
                    names.append('विद्युत मापक यंत्र')
                    numbers.append(j)
                if i == '12.1':
                    names.append('ट्रांसफार्मर')
                    numbers.append(j)
                if i == '13.1':
                    names.append('प्रत्यावर्तक')
                    numbers.append(j)
                if i == '14.1':
                    names.append('तुल्यकालिक प्रेरण')
                    numbers.append(j)
                if i == '15.1':
                    names.append('ए.सी. मोटर')
                    numbers.append(j)
                if i == '16.1':
                    names.append('वाइंडिंग')
                    numbers.append(j)
                if i == '17.1':
                    names.append('विद्युत उत्पादन,ट्रांसमिशन एवं वितरण')
                    numbers.append(j)
                if i == '18.1':
                    names.append('प्रदीप्ति')
                    numbers.append(j)
                if i == '19.1':
                    names.append('इलेक्ट्रिक्स')
                    numbers.append(j)
                if i == '20.1':
                    names.append('व्यावसायिक एवं सावधानियां')
                    numbers.append(j)

            return list(zip(names,numbers))

        if subject == 'FitterLocoPilot':
            for i,j in arr:
                if i == '1.1':
                    names.append('Introduction')
                    numbers.append(j)
                if i == '2.1':
                    names.append('Fitter tools')
                    numbers.append(j)
                if i == '3.1':
                    names.append('Sheet Metal Shop')
                    numbers.append(j)
                if i == '4.1':
                    names.append('Welding Theory')
                    numbers.append(j)
                if i == '5.1':
                    names.append('Soldering And Brazing')
                    numbers.append(j)
                if i == '6.1':
                    names.append('Physical and Mechanical Properties of Metals')
                    numbers.append(j)
                if i == '7.1':
                    names.append('Heat Treatment')
                    numbers.append(j)
                if i == '8.1':
                    names.append('Bearings')
                    numbers.append(j)
                if i == '9.1':
                    names.append('Drilling Machine')
                    numbers.append(j)
                if i == '10.1':
                    names.append('Lathe Machine')
                    numbers.append(j)
                if i == '11.1':
                    names.append('Grinding Machine')
                    numbers.append(j)
                if i == '12.1':
                    names.append('Power Transmission')
                    numbers.append(j)
                if i == '13.1':
                    names.append('Pipe And Pipe Fitting')
                    numbers.append(j)
                if i == '14.1':
                    names.append('Screw Threads')
                    numbers.append(j)
                if i == '15.1':
                    names.append('Gauge')
                    numbers.append(j)
                if i == '16.1':
                    names.append('Limits,Fits And Tolerance')
                    numbers.append(j)
                if i == '17.1':
                    names.append('Other Important Questions')
                    numbers.append(j)
                if i == '18.1':
                    names.append('Previous Year Exams Questions')
                    numbers.append(j)

            return list(zip(names,numbers))

        if subject == 'Civil_Loco_Pilot_Tech':
            for i, j in arr:
                if i == '2.1':
                    names.append('Land Surveying Basic Principal And Classification')
                    numbers.append(j)
                if i == '2.2':
                    names.append('Chain Surveying')
                    numbers.append(j)
                if i == '2.3':
                    names.append('Compass Surveying')
                    numbers.append(j)
                if i == '2.4':
                    names.append('Levelling')
                    numbers.append(j)
                if i == '2.5':
                    names.append('Minor Instruments')
                    numbers.append(j)
                if i == '2.6':
                    names.append('Computation Of Land')
                    numbers.append(j)
                if i == '2.7':
                    names.append('Plane Table Survey')
                    numbers.append(j)
                if i == '2.8':
                    names.append('Contours And Contouring')
                    numbers.append(j)
                if i == '2.9':
                    names.append('Theodolite Survey')
                    numbers.append(j)
                if i == '50.1':
                    names.append('Curve And Curves Setting')
                    numbers.append(j)
                if i == '12.1':
                    names.append('Bending moment and sheer force')
                    numbers.append(j)
                if i == '12.2':
                    names.append('Bending and sheer stress')
                    numbers.append(j)
                if i == '12.3':
                    names.append('Combined direct and bending stress')
                    numbers.append(j)
                if i == '12.4':
                    names.append('Slope and deflection')
                    numbers.append(j)
                if i == '12.5':
                    names.append('Principal stress and principle planes')
                    numbers.append(j)
                if i == '12.6':
                    names.append('Columns and struts')
                    numbers.append(j)
                if i == '12.7':
                    names.append('Trosion')
                    numbers.append(j)
                if i == '13.1':
                    names.append('Rivet Connection')
                    numbers.append(j)
                if i == '13.2':
                    names.append('Weld Connection')
                    numbers.append(j)
                if i == '13.3':
                    names.append('Tension Members')
                    numbers.append(j)
                if i == '13.4':
                    names.append('Compression Member')
                    numbers.append(j)
                if i == '13.5':
                    names.append('Steel Beams')
                    numbers.append(j)
                if i == '13.6':
                    names.append('Column base and Foundation')
                    numbers.append(j)
                if i == '13.7':
                    names.append('Steel root of trusses')
                    numbers.append(j)


            return list(zip(names,numbers))



        if subject == 'LocoPilot_Diesel':
            for i,j in arr:
                if i == '1.1':
                    names.append('Introduction to Engine & Development')
                    numbers.append(j)
                if i == '2.1':
                    names.append('Cylinder Head & Valve Assembly')
                    numbers.append(j)
                if i == '3.1':
                    names.append('Piston & Connecting Rod')
                    numbers.append(j)
                if i == '4.1':
                    names.append('Crank Shaft,Cam Shaft Fly Wheel & Bearing')
                    numbers.append(j)
                if i == '5.1':
                    names.append('Gas Turbine Marine & Statonery Engine')
                    numbers.append(j)
                if i == '6.1':
                    names.append('Cooling & Snake System')
                    numbers.append(j)
                if i == '7.1':
                    names.append('Intake & Exhaust System')
                    numbers.append(j)
                if i == '8.1':
                    names.append('Diesel Fuel Supply System')
                    numbers.append(j)
                if i == '9.1':
                    names.append('Emission Charging & Starting System')
                    numbers.append(j)
                if i == '10.1':
                    names.append('Troubleshooting')
                    numbers.append(j)

            return list(zip(names,numbers))

# for knimbus subjects
        if subject == 'Design and analysis of algorithm':
            for i,j in arr:
                if i == '1.1':
                    names.append('Divide and Conquer')
                    numbers.append(j)
                if i == '2.1':
                    names.append('Dynamic Programming')
                    numbers.append(j)
                if i == '3.1':
                    names.append('Introduction')
                    numbers.append(j)
                if i == '4.1':
                    names.append('Greedy Method')
                    numbers.append(j)
                return list(zip(names,numbers))


        if subject == 'CAT_Quantitative_Aptitude':
            for i,j in arr:
                if i == '11.1':
                    names.append('Geometry')
                    numbers.append(i)

            return list(zip(names,numbers))




    def change_topicNamesNumber(self,arr,subject):
        numbers = []
        if subject == 'English':
            for i in arr:
                if i == 'Antonym':
                    numbers.append('1.1')
                elif i == 'Synonym':
                    numbers.append('1.2')
                elif i == 'One word substitution':
                    numbers.append('1.3')
                elif i == 'Idioms & Phrases':
                    numbers.append('1.4')
                elif i == 'Phrasal Verbs':
                    numbers.append('1.5')
                elif i == 'Use of some verbs with particular nouns':
                    numbers.append('1.6')
                elif i == 'Tense':
                    numbers.append('1.7')
                elif i == 'Noun':
                    numbers.append('2.1')
                elif i == 'Pronoun':
                    numbers.append('2.2')
                elif i == 'Adjective':
                    numbers.append('2.3')
                elif i == 'Articles':
                    numbers.append('2.4')
                elif i == 'Verb':
                    numbers.append('2.5')
                elif i == 'Adverb':
                    numbers.append('2.6')
                elif i == 'Time & Tense':
                    numbers.append('2.7')
                elif i == 'Voice':
                    numbers.append('2.8')
                elif i == 'Non-Finites':
                    numbers.append('2.9')
                elif i == 'Narration':
                    numbers.append('3.1')
                elif i == 'Preposition':
                    numbers.append('3.2')
                elif i == 'Conjunction':
                    numbers.append('3.3')
                elif i == 'Subject verb agreement':
                    numbers.append('3.4')
                elif i == 'Common Errors':
                    numbers.append('3.5')
                elif i == 'Superfluous Expressions & Slang':
                    numbers.append('3.6')


            return numbers
        if subject == 'General-Intelligence':
            for i in arr:
                if i == 'Paper cutting and Folding':
                    numbers.append('1.1')
                elif i == 'Mirror and Water Image':
                    numbers.append('1.2')
                elif i == 'Embedded Figures':
                    numbers.append('1.3')
                elif i == 'Figure Completion':
                    numbers.append('1.4')
                elif i == 'Counting of embedded figures':
                    numbers.append('1.5')
                elif i == 'Counting of figures':
                    numbers.append('1.6')
                elif i == 'Analogy':
                    numbers.append('2.1')
                elif i == 'Multiple Analogy':
                    numbers.append('2.2')
                elif i == 'Choosing the analogous pair':
                    numbers.append('2.3')
                elif i == 'Number analogy (series pattern)':
                    numbers.append('2.4')
                elif i =='Number analogy (missing)':
                    numbers.append('2.5')
                elif i == 'Alphabet based analogy':
                    numbers.append('2.6')
                elif i == 'Mixed analogy':
                    numbers.append('2.7')
                elif i == 'Series Completion (Diagram)':
                    numbers.append('3.1')
                elif i == 'Analogy (Diagram)':
                    numbers.append('3.2')
                elif i == 'Classification (Diagram)':
                    numbers.append('3.3')
                elif i == 'Dice & Boxes':
                    numbers.append('3.4')
                elif i == 'Ruled based analogy':
                    numbers.append('2.8')
                elif i == 'Alphabet Test':
                    numbers.append('2.9')
                elif i == 'Ranking':
                    numbers.append('4.1')
                elif i == 'Matrix':
                    numbers.append('5.1')
                elif i == 'Word Creation':
                    numbers.append('6.1')
                elif i == 'Odd one out':
                    numbers.append('7.1')
                elif i == 'Height':
                    numbers.append('8.1')
                elif i == 'Direction':
                    numbers.append('9.1')
                elif i =='Statement & Conclusion':
                    numbers.append('10.1')
                elif i == 'Venn Diagram':
                    numbers.append('11.1')
                elif i == 'Missing number':
                    numbers.append('12.1')
                elif i == 'Logical Sequence of words':
                    numbers.append('13.1')
                elif i == 'Clock/Time':
                    numbers.append('14.1')
                elif i == 'Mathematical Operations':
                    numbers.append('15.1')
                elif i == 'Coding Decoding':
                    numbers.append('16.1')
                elif i == 'Series Test':
                    numbers.append('17.1')
                elif i == 'Syllogism':
                    numbers.append('18.1')
                elif i == 'Blood Relation':
                    numbers.append('19.1')
                elif i == 'Seating Arrangement':
                    numbers.append('20.1')
                elif i == 'Calender Test':
                    numbers.append('22.1')
                elif i == 'Symbols & Notations':
                    numbers.append('28.1')



            return numbers
        if subject == 'Quantitative-Analysis':
            for i in arr:
                if i == 'Age':
                    numbers.append('1.1')
                elif i == 'Alligation':
                    numbers.append('2.1')
                elif i == 'Area':
                    numbers.append('3.1')
                elif i == 'Average':
                    numbers.append('4.1')
                elif i == 'Boat & Stream':
                    numbers.append('5.1')
                elif i == 'Discount':
                    numbers.append('6.1')
                elif i == 'Fraction':
                    numbers.append('7.1')
                elif i == 'LCM & LCF':
                    numbers.append('8.1')
                elif i == 'Number System':
                    numbers.append('9.1')
                elif i == 'Percentage':
                    numbers.append('10.1')
                elif i == 'Pipes & Cistern':
                    numbers.append('11.1')
                elif i == 'Profit & Loss':
                    numbers.append('12.1')
                elif i == 'Ratio':
                    numbers.append('13.1')
                elif i == 'Simple Interest':
                    numbers.append('14.1')
                elif i == 'Simplification':
                    numbers.append('15.1')
                elif i == 'Speed & Distance':
                    numbers.append('16.1')
                elif i == 'Square & Cube root':
                    numbers.append('17.1')
                elif i == 'Surds & Indices':
                    numbers.append('18.1')
                elif i == 'Time & Work':
                    numbers.append('19.1')
                elif i == 'Train':
                    numbers.append('20.1')
                elif i == 'Volume':
                    numbers.append('21.1')
                elif i == 'Trigonometry':
                    numbers.append('22.1')
                elif i == 'Partnership':
                    numbers.append('23.1')
                elif i == '24.1':
                    numbers.append('Coumpound Interest')
                elif i == '25.1':
                    numbers.append('Decimals')


            return numbers
        if subject == 'General-Knowledge':
            for i in arr:
                if i == 'Inventions & Innovators':
                    numbers.append('1.1')
                if i == 'Bird Sanctuary':
                    numbers.append('2.1')
                if i == 'Books & Authors':
                    numbers.append('3.1')
                if i == 'Countries, Capitals & Currencies':
                    numbers.append('4.1')
                if i == 'Current Affairs':
                    numbers.append('5.1')
                if i == 'Economics':
                    numbers.append('6.1')
                if i == 'General Science':
                    numbers.append('7.1')
                if i == 'Biology':
                    numbers.append('8.1')
                if i == 'Chemistry':
                    numbers.append('9.1')
                if i == 'Science & Technology':
                    numbers.append('10.1')
                if i == 'Physics':
                    numbers.append('11.1')
                if i == 'Geography':
                    numbers.append('12.1')
                if i == 'National Organizations':
                    numbers.append('13.1')
                if i == 'History':
                    numbers.append('14.1')
                if i == 'Honors & Awards':
                    numbers.append('15.1')
                if i == 'Important Dates':
                    numbers.append('16.1')
                if i == 'Indian Agriculture':
                    numbers.append('17.1')
                if i == 'Indian Constitution':
                    numbers.append('18.1')
                if i == 'Indian Culture':
                    numbers.append('19.1')
                if i == 'Indian Museums':
                    numbers.append('20.1')
                if i == 'Polity (India)':
                    numbers.append('21.1')
                if i == 'Sports':
                    numbers.append('22.1')
                if i == 'Superlatives(India)':
                    numbers.append('23.1')
                if i == 'Symbols of States (India)':
                    numbers.append('24.1')
                if i == 'Tiger Reserve':
                    numbers.append('25.1')
                if i == 'UNESCO Word Heritage Sites(India)':
                    numbers.append('26.1')
                if i == 'World Organizations':
                    numbers.append('27.1')
                if i == 'Polity (World)':
                    numbers.append('28.1')
            return numbers

        if subject == 'General-Science':
            for i in arr:
                if i == 'गुरूत्व स्थूल पदार्थ के गुण व प्रकाशन':
                    numbers.append('1.1')
                if i == 'लेंस व दर्पण':
                    numbers.append('2.1')
                if i == 'आधुनिक भौतिकी':
                    numbers.append('3.1')
                if i == 'विमिय तथा द्विविमिय':
                    numbers.append('4.1')
                if i == 'कॉमन प्रश्नपत्र भौतिक शास्त्रा':
                    numbers.append('5.1')
                if i == 'दाब घटाव प्रत्यासा':
                    numbers.append('6.1')
                if i == 'ध्वन':
                    numbers.append('7.1')
                if i == 'मात्रक विभाएं मापन':
                    numbers.append('8.1')
                if i == 'सदिश तथा अदिश':
                    numbers.append('9.1')
                if i == 'कार्य,ऊर्जा व शक्ति':
                    numbers.append('10.1')
                if i == 'कोशिका विज्ञान':
                    numbers.append('11.1')
                if i == 'पादप जगत':
                    numbers.append('12.1')
                if i == 'पादप शरीर क्रिया विज्ञान':
                    numbers.append('13.1')
                if i == 'आर्थिक वनस्पति विज्ञान':
                    numbers.append('14.1')
                if i == 'जन्तु विज्ञान':
                    numbers.append('15.1')
                if i == 'जन्तु उत्तक एवं पोषण':
                    numbers.append('16.1')
                if i == 'आनुवांशिक':
                    numbers.append('17.1')
                if i == 'मानव स्वास्थ्य एवं रोग':
                    numbers.append('18.1')
                if i == 'जैव प्रोद्यौगिक':
                    numbers.append('19.1')
                if i == 'कम्प्यूटर एवं सूचना प्रोद्यौगिकी':
                    numbers.append('20.1')


            return numbers


# categories for GroupX

        if subject == 'Defence-English':
            for i in arr:
                if i == 'Comprehension':
                    numbers.append('1.1')
                if i == 'Judge Comprehension':
                    numbers.append('2.1')
                if i == 'Inferences':
                    numbers.append('3.1')
                if i == 'Vocabulary':
                    numbers.append('4.1')
                if i == 'Composition':
                    numbers.append('5.1')
                if i == 'Subject and Verb':
                    numbers.append('6.1')
                if i == 'Verb and their use':
                    numbers.append('7.1')
                if i == 'Sequence of tenses':
                    numbers.append('8.1')
                if i == 'Transformation':
                    numbers.append('9.1')
                if i == 'Grammer':
                    numbers.append('10.1')
                if i == 'Spellings':
                    numbers.append('11.1')
                if i == 'Word formation':
                    numbers.append('12.1')
                if i == 'Antonyms& Synonyms':
                    numbers.append('13.1')
                if i == 'Word Substitution':
                    numbers.append('14.1')
                if i == 'Correct use of words':
                    numbers.append('15.1')
                if i == 'Confusing words':
                    numbers.append('16.1')
                if i == 'Word order':
                    numbers.append('17.1')
                if i == 'Correct use of Adverbs':
                    numbers.append('18.1')
                if i == 'Idioms and Phrases':
                    numbers.append('19.1')
                if i == 'Use of simple idioms':
                    numbers.append('20.1')
                if i == 'Use of common proverbs':
                    numbers.append('21.1')
                if i == 'Direct/Indirect sentences':
                    numbers.append('22.1')
                if i == 'Direct to Indirect form':
                    numbers.append('23.1')
                if i == 'Indirect to Direct':
                    numbers.append('24.1')
                if i == 'Active and Passive voice':
                    numbers.append('25.1')
                if i == 'Active to Passive voice':
                    numbers.append('26.1')
                if i == 'Passive to Active voice':
                    numbers.append('27.1')
                if i == 'To be categorized':
                    numbers.append('50.1')

            return numbers

        if subject == 'Defence-Physics':
            for i in arr:
                if i == 'Unit of Dimension':
                    numbers.append('1.1')
                if i == 'Scalers&Vectors':
                    numbers.append('2.1')
                if i == 'Motion in straight line':
                    numbers.append('3.1')
                if i == 'Law of Motion':
                    numbers.append('4.1')
                if i == 'Projectile Motion':
                    numbers.append('5.1')
                if i == 'Circular Motion':
                    numbers.append('6.1')
                if i == 'Friction':
                    numbers.append('7.1')
                if i == 'Work power & Energy':
                    numbers.append('8.1')
                if i == 'Collision':
                    numbers.append('9.1')
                if i == 'Rotational motion % Moment of Inertia':
                    numbers.append('10.1')
                if i == 'Gravitation':
                    numbers.append('11.1')
                if i == 'Elasticity':
                    numbers.append('12.1')
                if i == 'Fluid Pressure ':
                    numbers.append('13.1')
                if i == 'Viscocity& Flow of fluids':
                    numbers.append('14.1')
                if i == 'Surface Tension':
                    numbers.append('15.1')
                if i == 'Oscillations':
                    numbers.append('16.1')
                if i == 'Thermometry':
                    numbers.append('17.1')
                if i == 'Thermal Expansion':
                    numbers.append('18.1')
                if i == 'Calorimetry':
                    numbers.append('19.1')
                if i == 'Transmission of Heat':
                    numbers.append('20.1')
                if i == 'Thermodynamics':
                    numbers.append('21.1')
                if i == 'Kinetic Theory of gases':
                    numbers.append('22.1')
                if i == 'Wave Motion':
                    numbers.append('23.1')
                if i == 'Superposition of waves':
                    numbers.append('24.1')
                if i == 'Speed of Sound':
                    numbers.append('25.1')
                if i == 'Vibrations in air columns':
                    numbers.append('26.1')
                if i == 'Vibration of Strings':
                    numbers.append('27.1')
                if i == 'Dopplers Effect':
                    numbers.append('28.1')
                if i == 'Musical Sound& Ultra sound':
                    numbers.append('29.1')
                if i == 'Electric charge & Electric Field':
                    numbers.append('30.1')
                if i == 'Gauss Theorem':
                    numbers.append('31.1')
                if i == 'Electric Capacitance':
                    numbers.append('32.1')
                if i == 'Electric Conduction':
                    numbers.append('33.1')
                if i == 'Ohms Law':
                    numbers.append('34.1')
                if i == 'Electromotive force & Electric cell':
                    numbers.append('35.1')
                if i == 'Kirchoffs law & wheatstone bridge':
                    numbers.append('36.1')
                if i == 'Potentiometer':
                    numbers.append('37.1')
                if i == 'Heating effect of current':
                    numbers.append('38.1')
                if i == 'Chemical effect of current':
                    numbers.append('39.1')
                if i == 'Magnetic effect of current':
                    numbers.append('40.1')
                if i == 'Electrical Instruments':
                    numbers.append('41.1')
                if i == 'Magnetic Field':
                    numbers.append('42.1')
                if i == 'Magnetic effects of matter & terrestrial\
                   magnetism':
                    numbers.append('43.1')
                if i == 'Electromagnetic Induction':
                    numbers.append('44.1')
                if i == 'Alternating Current':
                    numbers.append('45.1')
                if i == 'Reflection of light':
                    numbers.append('46.1')
                if i == 'Refraction of light':
                    numbers.append('47.1')
                if i == 'Refraction at Spherical surface & by\
                                    lenses':
                    numbers.append('48.1')
                if i == 'Prism & scattering of light':
                    numbers.append('49.1')
                if i == 'Optical instruments':
                    numbers.append('50.1')
                if i == 'Human eye & defects of vision':
                    numbers.append('51.1')
                if i == 'Wave theory of light':
                    numbers.append('52.1')
                if i == 'Interferance & Deflection of light':
                    numbers.append('53.1')
                if i == 'Polarization of light':
                    numbers.append('54.1')
                if i == 'Photometry':
                    numbers.append('55.1')
                if i == 'Dual nature of radiation & matter':
                    numbers.append('56.1')
                if i == 'Electromagnetic waves':
                    numbers.append('57.1')
                if i == 'Structure of Atom':
                    numbers.append('58.1')
                if i == 'Radioactivity':
                    numbers.append('59.1')
                if i == 'Nuclear fission & fusion':
                    numbers.append('60.1')
                if i == 'Semi-conductor,diode & Transistors':
                    numbers.append('61.1')
                if i == 'Digital electronics & logic gates':
                    numbers.append('62.1')

            return numbers

        if subject == 'Defence-GK-CA':
            for i in arr:
                if i == 'General Science':
                    numbers.append('1.1')
                if i == 'Civics':
                    numbers.append('1.2')
                if i == 'Geography':
                    numbers.append('1.3')
                if i == 'Current Events':
                    numbers.append('1.4')
                if i == 'History':
                    numbers.append('1.5')
                if i == 'Basic Computer Operation':
                    names.append('1.6')
                if i == 'General Knowledge':
                    names.append('1.7')

            return numbers





        if subject == 'GroupX-Maths':
            for i in arr:
                if i == 'Sets-Relations-Functions':
                    numbers.append('1.1')
                if i == 'Trigonometric functions':
                    numbers.append('2.1')
                if i == 'Inverse Trigonometric functions':
                    numbers.append('3.1')
                if i == 'Complex numbers':
                    numbers.append('4.1')
                if i == 'Quadratic eqations':
                    numbers.append('5.1')
                if i == 'Sequence & Series':
                    numbers.append('6.1')
                if i == 'Permutations':
                    numbers.append('7.1')
                if i == 'Combination':
                    numbers.append('8.1')
                if i == 'Binomial Theorem':
                    numbers.append('9.1')
                if i == 'Coordinate Geometry':
                    numbers.append('10.1')
                if i == 'Exponential Series':
                    numbers.append('11.1')
                if i == 'Logarithmic Series':
                    numbers.append('12.1')
                if i == 'Matrices':
                    numbers.append('13.1')
                if i == 'Determinants':
                    numbers.append('14.1')
                if i == 'Limit & Continuity':
                    numbers.append('15.1')
                if i == 'Differentiation':
                    numbers.append('16.1')
                if i == 'Application of Differentiation':
                    numbers.append('17.1')
                if i == 'Indefinite Integrals':
                    numbers.append('18.1')
                if i == 'Definite Integrals':
                    numbers.append('19.1')
                if i == 'Application of Integration':
                    numbers.append('20.1')
                if i == 'Diferential Equations':
                    numbers.append('21.1')
                if i == 'Probability Statistics':
                    numbers.append('22.1')
                if i == 'Properties of Triangle':
                    numbers.append('23.1')
                if i == 'Height&Distance':
                    numbers.append('24.1')

            return numbers
        if subject == 'MathsIITJEE10':
            for i in arr:
                if i == 'All Categories':
                    numbers.append('1.1')
            return numbers
        if subject == 'MathsIITJEE11':
            for i in arr:
                if i == 'All Categories':
                    numbers.append('1.1')
            return numbers

        if subject == 'MathsIITJEE12':
            for i in arr:
                if i == 'All Categories':
                    numbers.append('1.1')
            return numbers
        if subject == 'PhysicsIITJEE10':
            for i in arr:
                if i == 'All Categories':
                    numbers.append('1.1')
            return numbers

        if subject == 'PhysicsIITJEE11':
            for i in arr:
                if i == 'All Categories':
                    numbers.append('1.1')
            return numbers
        if subject == 'PhysicsIITJEE12':
            for i in arr:
                if i == 'All Categories':
                    numbers.append('1.1')
            return numbers
        if subject == 'ChemistryIITJEE10':
            for i in arr:
                if i == 'All Categories':
                    numbers.append('1.1')
            return numbers
        if subject == 'ChemistryIITJEE11':
            for i in arr:
                if i == 'All Categories':
                    numbers.append('1.1')
            return numbers

        if subject == 'ChemistryIITJEE12':
            for i in arr:
                if i == 'All Categories':
                    numbers.append('1.1')
            return numbers

        if subject == 'ElectricalLocoPilot':
            for i in arr:
                if i == 'चालक,अचालक एवं कुचालक':
                    numbers.append('1.1')
                if i == 'बेसिक इलेक्ट्रिकल':
                    numbers.append('2.1')
                if i == 'विद्युत सेल':
                    numbers.append('3.1')

                if i == 'संधारित्र':
                    numbers.append('4.1')

                if i == 'चुम्बक':
                    numbers.append('5.1')

                if i == 'डी.सी.जनित्र':
                    numbers.append('6.1')

                if i == 'डी.सी.मोटर':
                    numbers.append('7.1')

                if i == 'ए.सी थ्योरी':
                    numbers.append('8.1')

                if i == 'भू-सम्पर्कन':
                    numbers.append('9.1')

                if i == 'विद्युय वायरिंग':
                    numbers.append('10.1')

                if i == 'विद्युत मापक यंत्र':
                    numbers.append('11.1')

                if i == 'ट्रांसफार्मर':
                    numbers.append('12.1')

                if i == 'प्रत्यावर्तक':
                    numbers.append('13.1')

                if i == 'तुल्यकालिक प्रेरण':
                    numbers.append('14.1')

                if i == 'ए.सी. मोटर':
                    numbers.append('15.1')

                if i == 'वाइंडिंग':
                    numbers.append('16.1')

                if i == 'विद्युत उत्पादन,ट्रांसमिशन एवं वितरण':
                    numbers.append('17.1')

                if i == 'प्रदीप्ति':
                    numbers.append('18.1')

                if i == 'इलेक्ट्रिक्स':
                    numbers.append('19.1')

                if i == 'व्यावसायिक एवं सावधानियां':
                    numbers.append('20.1')


            return numbers

        if subject == 'FitterLocoPilot':
            for i in arr:
                if i == 'Introduction':
                    numbers.append('1.1')
                if i == 'Fitter tools':
                    numbers.append('2.1')
                if i == 'Sheet Metal Shop':
                    numbers.append('3.1')
                if i == 'Welding Theory':
                    numbers.append('4.1')
                if i == 'Soldering And Brazing':
                    numbers.append('5.1')
                if i == 'Physical and Mechanical Properties of Metals':
                    numbers.append('6.1')
                if i == 'Heat Treatment':
                    numbers.append('7.1')
                if i == 'Bearings':
                    numbers.append('8.1')
                if i == 'Drilling Machine':
                    numbers.append('9.1')
                if i == 'Lathe Machine':
                    numbers.append('10.1')
                if i == 'Grinding Machine':
                    numbers.append('11.1')
                if i == 'Power Transmission':
                    numbers.append('12.1')
                if i == 'Pipe And Pipe Fitting':
                    numbers.append('13.1')
                if i == 'Screw Threads':
                    numbers.append('14.1')
                if i == 'Gauge':
                    numbers.append('15.1')
                if i == 'Limits,Fits And Tolerance':
                    numbers.append('16.1')
                if i == 'Other Important Questions':
                    numbers.append('17.1')
                if i == 'Previous Year Exams Questions':
                    numbers.append('18.1')

            return numbers

        if subject == 'Civil_Loco_Pilot_Tech':
            for i in arr:
                if i == 'Land Surveying Basic Principal And Classification':
                    numbers.append('2.1')
                if i == 'Chain Surveying':
                    numbers.append('2.2')
                if i == 'Compass Surveying':
                    numbers.append('2.3')
                if i == 'Levelling':
                    numbers.append('2.4')
                if i == 'Minor Instruments':
                    numbers.append('2.5')
                if i == 'Computation Of Land':
                    numbers.append('2.6')
                if i == 'Plane Table Survey':
                    numbers.append('2.7')
                if i == 'Contours And Contouring':
                    numbers.append('2.8')
                if i == 'Theodolite Survey':
                    numbers.append('2.9')
                if i == 'Curve And Curves Setting':
                    numbers.append('50.1')
                if i == 'Bending moment and sheer force':
                    numbers.append('12.1')
                if i == 'Bending and sheer stress':
                    numbers.append('12.2')
                if i == 'Combined direct and bending stress':
                    numbers.append('12.3')
                if i == 'Slope and deflection':
                    numbers.append('12.4')
                if i == 'Principal stress and principle planes':
                    numbers.append('12.5')
                if i == 'Columns and struts':
                    numbers.append('12.6')
                if i == 'Trosion':
                    numbers.append('12.7')
                if i == 'Rivet Connection':
                    numbers.append('13.1')
                if i == 'Weld Connection':
                    numbers.append('13.2')
                if i == 'Tension Members':
                    numbers.append('13.3')
                if i == 'Compression Member':
                    numbers.append('13.4')
                if i == 'Steel Beams':
                    numbers.append('13.5')
                if i == 'Column base and Foundation':
                    numbers.append('13.6')
                if i == 'Steel root of trusses':
                    numbers.append('13.7')

 
            return numbers

        if subject == 'LocoPilot_Diesel':
            for i in arr:
                if i == 'Introduction to Engine & Development':
                    numbers.append('1.1')
                if i == 'Cylinder Head & Valve Assembly':
                    numbers.append('2.1')
                if i == 'Piston & Connecting Rod':
                    numbers.append('3.1')
                if i == 'Crank Shaft,Cam Shaft Fly Wheel & Bearing':
                    numbers.append('4.1')
                if i == 'Gas Turbine Marine & Statonery Engine':
                    numbers.append('5.1')
                if i == 'Cooling & Snake System':
                    numbers.append('6.1')
                if i == 'Intake & Exhaust System':
                    numbers.append('7.1')
                if i == 'Diesel Fuel Supply System':
                    numbers.append('8.1')
                if i == 'Emission Charging & Starting System':
                    numbers.append('9.1')
                if i == 'Troubleshooting':
                    numbers.append('10.1')

            return numbers

# for knimbus subjects
        if subject == 'Design and analysis of algorithm':
            for i in arr:
                if i == 'Divide and Conquer':
                    numbers.append('1.1')
                if i == 'Dynamic Programming':
                    numbers.append('2.1')
                if i == 'Introduction':
                    numbers.append('3.1')
                if i == 'Greedy Method':
                    numbers.append('4.1')
                return numbers

        if subject == 'CAT_Quantitative_Aptitude':
            for i in arr:
                if i == 'Geometry':
                    numbers.append('11.1')

            return numbers





    def return_TopicNames(self,subject):
        if subject == 'Defence-GK-CA':
            sub_list = ['1.1','1.2','1.3','1.4','1.5','1.6','1.7']
            return sub_list
        if subject == 'GroupX-Maths':
            sub_list =\
            ['1.1','2.1','3.1','4.1','5.1','6.1','7.1','8.1','9.1','10.1','11.1','12.1','13.1','14.1','15.1','16.1','17.1','18.1','19.1','20.1','21.1','22.1','23.1','24.1']
            return sub_list
        if subject == 'Defence-Physics':
            topic_choice = []
            for ch in range(1,63):
                topic_choice.append(str(ch)+'.'+str(1))
            return topic_choice
        if subject == 'Defence-English':
            topic_choice = []
            for ch in range(1,28):
                topic_choice.append(str(ch)+'.'+str(1))
            topic_choice.append('50.1')
            return topic_choice



def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    #pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),result)
    pdf =\
    pisa.pisaDocument(BytesIO(html.encode("utf-8-sig")),result,encoding='utf-8')
    if not pdf.err:
        return  HttpResponse(result.getvalue(),content_type='application/pdf')
    return None



def visible_tests(test_id):
    test = SSCKlassTest.objects.get(id = test_id)
    test_date = test.due_date
    print(test_date)
    today_date = datetime.now().date()
    print(today_date)
    if test_date == today_date:
        return test

    else:
        return test

# ---------------------------
# changing names without using a student or teacher class
def change_topicNumbersNames(arr,subject):
    names = []
    numbers = []
    if subject == 'English':
        for i in arr:
            if i == '1.1':
                names.append('Antonym')
                numbers.append(i)
            elif i == '1.2':
                names.append('Synonym')
                numbers.append(i)
            elif i == '1.3':
                names.append('One word substitution')
                numbers.append(i)
            elif i == '1.4':
                names.append('Idioms & Phrases')
                numbers.append(i)
            elif i == '1.5':
                names.append('Phrasal Verbs')
                numbers.append(i)
            elif i == '1.6':
                names.append('Use of some verbs with particular nouns')
                numbers.append(i)
            elif i == '1.7':
                names.append('Tense')
                numbers.append(i)
            elif i == '2.1':
                names.append('Noun')
                numbers.append(i)
            elif i == '2.2':
                names.append('Pronoun')
                numbers.append(i)
            elif i == '2.3':
                names.append('Adjective')
                numbers.append(i)
            elif i == '2.4':
                names.append('Articles')
                numbers.append(i)
            elif i == '2.5':
                names.append('Verb')
                numbers.append(i)
            elif i == '2.6':
                names.append('Adverb')
                numbers.append(i)
            elif i == '2.7':
                names.append('Time & Tense')
                numbers.append(i)
            elif i == '2.8':
                names.append('Voice')
                numbers.append(i)
            elif i == '2.9':
                names.append('Non-Finites')
                numbers.append(i)
            elif i == '3.1':
                names.append('Narration')
                numbers.append(i)
            elif i == '3.2':
                names.append('Preposition')
                numbers.append(i)
            elif i == '3.3':
                names.append('Conjunction')
                numbers.append(i)
            elif i == '3.4':
                names.append('Subject verb agreement')
                numbers.append(i)
            elif i == '3.5':
                names.append('Common Errors')
                numbers.append(i)
            elif i == '3.6':
                names.append('Superfluous Expressions & Slang')
                numbers.append(i)


        changed = list(zip(names,numbers))
        return changed
    if subject == 'General-Intelligence':
        for i in arr:
            if i == '1.1':
                names.append('Paper cutting and Folding')
                numbers.append(i)
            elif i == '1.2':
                names.append('Mirror and Water Image')
                numbers.append(i)
            elif i == '1.3':
                names.append('Embedded Figures')
                numbers.append(i)
            elif i == '1.4':
                names.append('Figure Completion')
                numbers.append(i)
            elif i == '1.5':
                names.append('Counting of embedded figures')
                numbers.append(i)
            elif i == '1.6':
                names.append('Counting of figures')
                numbers.append(i)
            elif i == '2.1':
                names.append('Analogy')
                numbers.append(i)
            elif i == '2.2':
                names.append('Multiple Analogy')
                numbers.append(i)
            elif i == '2.3':
                names.append('Choosing the analogous pair')
                numbers.append(i)
            elif i == '2.4':
                names.append('Number analogy (series pattern)')
                numbers.append(i)
            elif i =='2.5':
                names.append('Number analogy (missing)')
                numbers.append(i)
            elif i == '2.6':
                names.append('Alphabet based analogy')
                numbers.append(i)
            elif i == '2.7':
                names.append('Mixed analogy')
                numbers.append(i)
            elif i == '3.1':
                names.append('Series Completion (Diagram)')
                numbers.append(i)
            elif i == '3.2':
                names.append('Analogy (Diagram)')
                numbers.append(i)
            elif i == '3.3':
                names.append('Classification (Diagram)')
                numbers.append(i)
            elif i == '3.4':
                names.append('Dice & Boxes')
                numbers.append(i)
            elif i == '2.8':
                names.append('Ruled based analogy')
                numbers.append(i)
            elif i == '2.9':
                names.append('Alphabet Test')
                numbers.append(i)
            elif i == '4.1':
                names.append('Ranking')
                numbers.append(i)
            elif i == '5.1':
                names.append('Matrix')
                numbers.append(i)
            elif i == '6.1':
                names.append('Word Creation')
                numbers.append(i)
            elif i == '7.1':
                names.append('Odd one out')
                numbers.append(i)
            elif i == '8.1':
                names.append('Height')
                numbers.append(i)
            elif i == '9.1':
                names.append('Direction')
                numbers.append(i)
            elif i =='10.1':
                names.append('Statement & Conclusion')
                numbers.append(i)
            elif i == '11.1':
                names.append('Venn Diagram')
                numbers.append(i)
            elif i == '12.1':
                names.append('Missing number')
                numbers.append(i)
            elif i == '13.1':
                names.append('Logical Sequence of words')
                numbers.append(i)
            elif i == '14.1':
                names.append('Clock/Time')
                numbers.append(i)
            elif i == '15.1':
                names.append('Mathematical Operations')
                numbers.append(i)
            elif i == '16.1':
                names.append('Coding Decoding')
                numbers.append(i)
            elif i == '17.1':
                names.append('Series Test')
                numbers.append(i)
            elif i == '18.1':
                names.append('Syllogism')
                numbers.append(i)
            elif i == '19.1':
                names.append('Blood Relation')
                numbers.append(i)
            elif i == '20.1':
                names.append('Seating Arrangement')
                numbers.append(i)
            elif i == '22.1':
                names.append('Calender Test')
                numbers.append(i)
            elif i == '28.1':
                names.append('Symbols & Notations')
                numbers.append(i)

        changed = list(zip(names,numbers))
        return changed
    if subject == 'Quantitative-Analysis':
        for i in arr:
            if i == '1.1':
                names.append('Age')
                numbers.append(i)
            elif i == '2.1':
                names.append('Alligation')
                numbers.append(i)
            elif i == '3.1':
                names.append('Area')
                numbers.append(i)
            elif i == '4.1':
                names.append('Average')
                numbers.append(i)
            elif i == '5.1':
                names.append('Boat & Stream')
                numbers.append(i)
            elif i == '6.1':
                names.append('Discount')
                numbers.append(i)
            elif i == '7.1':
                names.append('Fraction')
                numbers.append(i)
            elif i == '8.1':
                names.append('LCM & LCF')
                numbers.append(i)
            elif i == '9.1':
                names.append('Number System')
                numbers.append(i)
            elif i == '10.1':
                names.append('Percentage')
                numbers.append(i)
            elif i == '11.1':
                names.append('Pipes & Cistern')
                numbers.append(i)
            elif i == '12.1':
                names.append('Profit & Loss')
                numbers.append(i)
            elif i == '13.1':
                names.append('Ratio')
                numbers.append(i)
            elif i == '14.1':
                names.append('Simple Interest')
                numbers.append(i)
            elif i == '15.1':
                names.append('Simplification')
                numbers.append(i)
            elif i == '16.1':
                names.append('Speed & Distance')
                numbers.append(i)
            elif i == '17.1':
                names.append('Square & Cube root')
                numbers.append(i)
            elif i == '18.1':
                names.append('Surds & Indices')
                numbers.append(i)
            elif i == '19.1':
                names.append('Time & Work')
                numbers.append(i)
            elif i == '20.1':
                names.append('Train')
                numbers.append(i)
            elif i == '21.1':
                names.append('Volume')
                numbers.append(i)
            elif i == '22.1':
                names.append('Trigonometry')
                numbers.append(i)
            elif i == '23.1':
                names.append('Partnership')
                numbers.append(i)
            elif i == '24.1':
                names.append('Coumpound Interest')
                numbers.append(i)
            elif i == '25.1':
                names.append('Decimals')
                numbers.append(i)



        changed = list(zip(names,numbers))
        return changed
    if subject == 'General-Knowledge':
        for i in arr:
            if i == '1.1':
                names.append('Inventions & Innovators')
                numbers.append(i)
            if i == '2.1':
                names.append('Bird Sanctuary')
                numbers.append(i)
            if i == '3.1':
                names.append('Books & Authors')
                numbers.append(i)
            if i == '4.1':
                names.append('Countries, Capitals & Currencies')
                numbers.append(i)
            if i == '5.1':
                names.append('Current Affairs')
                numbers.append(i)
            if i == '6.1':
                names.append('Economics')
                numbers.append(i)
            if i == '7.1':
                names.append('General Science')
                numbers.append(i)
            if i == '8.1':
                names.append('Biology')
                numbers.append(i)
            if i == '9.1':
                names.append('Chemistry')
                numbers.append(i)
            if i == '10.1':
                names.append('Science & Technology')
                numbers.append(i)
            if i == '11.1':
                names.append('Physics')
                numbers.append(i)
            if i == '12.1':
                names.append('Geography')
                numbers.append(i)
            if i == '13.1':
                names.append('National Organizations')
                numbers.append(i)
            if i == '14.1':
                names.append('History')
                numbers.append(i)
            if i == '15.1':
                names.append('Honors & Awards')
                numbers.append(i)
            if i == '16.1':
                names.append('Important Dates')
                numbers.append(i)
            if i == '17.1':
                names.append('Indian Agriculture')
                numbers.append(i)
            if i == '18.1':
                names.append('Indian Constitution')
                numbers.append(i)
            if i == '19.1':
                names.append('Indian Culture')
                numbers.append(i)
            if i == '20.1':
                names.append('Indian Museums')
                numbers.append(i)
            if i == '21.1':
                names.append('Polity (India)')
                numbers.append(i)
            if i == '22.1':
                names.append('Sports')
                numbers.append(i)
            if i == '23.1':
                names.append('Superlatives(India)')
                numbers.append(i)
            if i == '24.1':
                names.append('Symbols of States (India)')
                numbers.append(i)
            if i == '25.1':
                names.append('Tiger Reserve')
                numbers.append(i)
            if i == '26.1':
                names.append('UNESCO Word Heritage Sites(India)')
                numbers.append(i)
            if i == '27.1':
                names.append('World Organizations')
                numbers.append(i)
            if i == '28.1':
                names.append('Polity (World)')
                numbers.append(i)
        changed = list(zip(names,numbers))
        return changed
# categories for GroupX

    if subject == 'Defence-English':
        for i in arr:
            if i == '1.1':
                names.append('Comprehension')
                numbers.append(i)
            if i == '2.1':
                names.append('Judge Comprehension')
                numbers.append(i)
            if i == '3.1':
                names.append('Inferences')
                numbers.append(i)
            if i == '4.1':
                names.append('Vocabulary')
                numbers.append(i)
            if i == '5.1':
                names.append('Composition')
                numbers.append(i)
            if i == '6.1':
                names.append('Subject and Verb')
                numbers.append(i)
            if i == '7.1':
                names.append('Verb and their use')
                numbers.append(i)
            if i == '8.1':
                names.append('Sequence of tenses')
                numbers.append(i)
            if i == '9.1':
                names.append('Transformation')
                numbers.append(i)
            if i == '10.1':
                names.append('Grammer')
                numbers.append(i)
            if i == '11.1':
                names.append('Spellings')
                numbers.append(i)
            if i == '12.1':
                names.append('Word formation')
                numbers.append(i)
            if i == '11.1':
                names.append('Antonyms& Synonyms')
                numbers.append(i)
            if i == '11.1':
                names.append('Word Substitution')
                numbers.append(i)
            if i == '12.1':
                names.append('Correct use of words')
                numbers.append(i)
            if i == '13.1':
                names.append('Confusing words')
                numbers.append(i)
            if i == '14.1':
                names.append('Word order')
                numbers.append(i)
            if i == '15.1':
                names.append('Correct use of Adverbs')
                numbers.append(i)
            if i == '16.1':
                names.append('Idioms and Phrases')
                numbers.append(i)
            if i == '17.1':
                names.append('Use of simple idioms')
                numbers.append(i)
            if i == '18.1':
                names.append('Use of common proverbs')
                numbers.append(i)
            if i == '19.1':
                names.append('Direct/Indirect sentences')
                numbers.append(i)
            if i == '20.1':
                names.append('Direct to Indirect form')
                numbers.append(i)
            if i == '21.1':
                names.append('Indirect to Direct')
                numbers.append(i)
            if i == '22.1':
                names.append('Active and Passive voice')
                numbers.append(i)
            if i == '23.1':
                names.append('Active to Passive voice')
                numbers.append(i)
            if i == '22.1':
                names.append('Passive to Active voice')
                numbers.append(i)
            if i == '50.1':
                names.append('To be categorized')
                numbers.append(i)

        return list(zip(names,numbers))


    if subject == 'Defence-Physics':
        for i in arr:
            if i == '1.1':
                names.append('Unit of Dimension')
                numbers.append(i)
            if i == '2.1':
                names.append('Scalers&Vectors')
                numbers.append(i)
            if i == '3.1':
                names.append('Motion in straight line')
                numbers.append(i)
            if i == '4.1':
                names.append('Law of Motion')
                numbers.append(i)
            if i == '5.1':
                names.append('Projectile Motion')
                numbers.append(i)
            if i == '6.1':
                names.append('Circular Motion')
                numbers.append(i)
            if i == '7.1':
                names.append('Friction ')
                numbers.append(i)
            if i == '8.1':
                names.append('Work power & Energy')
                numbers.append(i)
            if i == '9.1':
                names.append('Collision')
                numbers.append(i)
            if i == '10.1':
                names.append('Rotational motion % Moment of Inertia')
                numbers.append(i)
            if i == '11.1':
                names.append('Gravitation')
                numbers.append(i)
            if i == '12.1':
                names.append('Elasticity')
                numbers.append(i)
            if i == '13.1':
                names.append('Fluid Pressure ')
                numbers.append(i)
            if i == '14.1':
                names.append('Viscocity& Flow of fluids')
                numbers.append(i)
            if i == '15.1':
                names.append('Surface Tension')
                numbers.append(i)
            if i == '16.1':
                names.append('Oscillations')
                numbers.append(i)
            if i == '17.1':
                names.append('Thermometry')
                numbers.append(i)
            if i == '18.1':
                names.append('Thermal Expansion')
                numbers.append(i)
            if i == '19.1':
                names.append('Calorimetry')
                numbers.append(i)
            if i == '20.1':
                names.append('Transmission of Heat')
                numbers.append(i)
            if i == '21.1':
                names.append('Thermodynamics')
                numbers.append(i)
            if i == '22.1':
                names.append('Kinetic Theory of gases')
                numbers.append(i)
            if i == '23.1':
                names.append('Wave Motion')
                numbers.append(i)
            if i == '24.1':
                names.append('Superposition of waves')
                numbers.append(i)
            if i == '25.1':
                names.append('Speed of Sound')
                numbers.append(i)
            if i == '26.1':
                names.append('Vibrations in air columns')
                numbers.append(i)
            if i == '27.1':
                names.append('Vibration of Strings')
                numbers.append(i)
            if i == '28.1':
                names.append('Dopplers Effect')
                numbers.append(i)
            if i == '29.1':
                names.append('Musical Sound& Ultra sound')
                numbers.append(i)
            if i == '30.1':
                names.append('Electric charge & Electric Field')
                numbers.append(i)
            if i == '31.1':
                names.append('Gauss Theorem')
                numbers.append(i)
            if i == '32.1':
                names.append('Electric Capacitance')
                numbers.append(i)
            if i == '33.1':
                names.append('Electric Conduction')
                numbers.append(i)
            if i == '34.1':
                names.append('Ohms Law')
                numbers.append(i)
            if i == '35.1':
                names.append('Electromotive force & Electric cell')
                numbers.append(i)
            if i == '36.1':
                names.append('Kirchoffs law & wheatstone bridge')
                numbers.append(i)
            if i == '37.1':
                names.append('Potentiometer')
                numbers.append(i)
            if i == '38.1':
                names.append('Heating effect of current')
                numbers.append(i)
            if i == '39.1':
                names.append('Chemical effect of current')
                numbers.append(i)
            if i == '40.1':
                names.append('Magnetic effect of current')
                numbers.append(i)
            if i == '41.1':
                names.append('Electrical Instruments')
                numbers.append(i)
            if i == '42.1':
                names.append('Magnetic Field')
                numbers.append(i)
            if i == '43.1':
                names.append('Magnetic effects of matter & terrestrial\
                                magnetism')
                numbers.append(i)
            if i == '44.1':
                names.append('Electromagnetic Induction')
                numbers.append(i)
            if i == '45.1':
                names.append('Alternating Current')
                numbers.append(i)
            if i == '46.1':
                names.append('Reflection of light')
                numbers.append(i)
            if i == '47.1':
                names.append('Refraction of light')
                numbers.append(i)
            if i == '48.1':
                names.append('Refraction at Spherical surface & by\
                                lenses')
                numbers.append(i)
            if i == '49.1':
                names.append('Prism & scattering of light')
                numbers.append(i)
            if i == '50.1':
                names.append('Optical instruments')
                numbers.append(i)
            if i == '51.1':
                names.append('Human eye & defects of vision')
                numbers.append(i)
            if i == '52.1':
                names.append('Wave theory of light')
                numbers.append(i)
            if i == '53.1':
                names.append('Interferance & Deflection of light')
                numbers.append(i)
            if i == '54.1':
                names.append('Polarization of light')
                numbers.append(i)
            if i == '55.1':
                names.append('Photometry')
                numbers.append(i)
            if i == '56.1':
                names.append('Dual nature of radiation & matter')
                numbers.append(i)
            if i == '57.1':
                names.append('Electromagnetic waves')
                numbers.append(i)
            if i == '58.1':
                names.append('Structure of Atom')
                numbers.append(i)
            if i == '59.1':
                names.append('Radioactivity')
                numbers.append(i)
            if i == '60.1':
                names.append('Nuclear fission & fusion')
                numbers.append(i)
            if i == '61.1':
                names.append('Semi-conductor,diode & Transistors')
                numbers.append(i)
            if i == '62.1':
                names.append('Digital electronics & logic gates')
                numbers.append(i)

        return list(zip(names,numbers))

    if subject == 'Defence-GK-CA':
        for i in arr:
            if i == '1.1':
                names.append('General Science')
                numbers.append(i)
            if i == '1.2':
                names.append('Civics')
                numbers.append(i)
            if i == '1.3':
                names.append('Geography')
                numbers.append(i)
            if i == '1.4':
                names.append('Current Events')
                numbers.append(i)
            if i == '1.5':
                names.append('History')
                numbers.append(i)
            if i == '1.6':
                names.append('Basic Computer Operation')
                numbers.append(i)
            if i == '1.7':
                names.append('General Knowledge')
                numbers.append(i)

        return list(zip(names,numbers))






    if subject == 'GroupX-Maths':
        for i in arr:
            if i == '1.1':
                names.append('Sets-Relations-Functions')
                numbers.append(i)
            if i == '2.1':
                names.append('Trigonometric functions')
                numbers.append(i)
            if i == '3.1':
                names.append('Inverse Trigonometric functions')
                numbers.append(i)
            if i == '4.1':
                names.append('Complex numbers')
                numbers.append(i)
            if i == '5.1':
                names.append('Quadratic eqations')
                numbers.append(i)
            if i == '6.1':
                names.append('Sequence & Series')
                numbers.append(i)
            if i == '7.1':
                names.append('Permutations')
                numbers.append(i)
            if i == '8.1':
                names.append('Combination')
                numbers.append(i)
            if i == '9.1':
                names.append('Binomial Theorem')
                numbers.append(i)
            if i == '10.1':
                names.append('Coordinate Geometry')
                numbers.append(i)
            if i == '11.1':
                names.append('Exponential Series')
                numbers.append(i)
            if i == '12.1':
                names.append('Logarithmic Series')
                numbers.append(i)
            if i == '13.1':
                names.append('Matrices')
                numbers.append(i)
            if i == '14.1':
                names.append('Determinants')
                numbers.append(i)
            if i == '15.1':
                names.append('Limit & Continuity')
                numbers.append(i)
            if i == '16.1':
                names.append('Differentiation')
                numbers.append(i)
            if i == '17.1':
                names.append('Application of Differentiation')
                numbers.append(i)
            if i == '18.1':
                names.append('Indefinite Integrals')
                numbers.append(i)
            if i == '19.1':
                names.append('Definite Integrals')
                numbers.append(i)
            if i == '20.1':
                names.append('Application of Integration')
                numbers.append(i)
            if i == '21.1':
                names.append('Diferential Equations')
                numbers.append(i)
            if i == '22.1':
                names.append('Probability Statistics')
                numbers.append(i)
            if i == '23.1':
                names.append('Properties of Triangle')
                numbers.append(i)
            if i == '24.1':
                names.append('Height&Distance')
                numbers.append(i)



        return list(zip(names,numbers))

    if subject == 'MathsIITJEE10':
        for i in arr:
            if i == '1.1':
                names.append('All Categories')
                numbers.append(i)

        return list(zip(names,numbers))

    if subject == 'MathsIITJEE11':
        for i in arr:
            if i == '1.1':
                names.append('All Categories')
                numbers.append(i)
        return list(zip(names,numbers))

    if subject == 'MathsIITJEE12':
        for i in arr:
            if i == '1.1':
                names.append('All Categories')
                numbers.append(i)

        return list(zip(names,numbers))

    if subject == 'PhysicsIITJEE10':
        for i in arr:
            if i == '1.1':
                names.append('All Categories')
                numbers.append(i)
        return list(zip(names,numbers))

    if subject == 'PhysicsIITJEE11':
        for i in arr:
            if i == '1.1':
                names.append('All Categories')
                numbers.append(i)

        return list(zip(names,numbers))

    if subject == 'PhysicsIITJEE12':
        for i in arr:
            if i == '1.1':
                names.append('All Categories')
                numbers.append(i)
        return list(zip(names,numbers))


    if subject == 'ChemistryIITJEE10':
        for i in arr:
            if i == '1.1':
                names.append('All Categories')
                numbers.append(i)

        return list(zip(names,numbers))

    if subject == 'ChemistryIITJEE11':
        for i in arr:
            if i == '1.1':
                names.append('All Categories')
                numbers.append(i)
        return list(zip(names,numbers))


    if subject == 'ChemistryIITJEE12':
        for i in arr:
            if i == '1.1':
                names.append('All Categories')
                numbers.append(i)
        return list(zip(names,numbers))
    # for locopilot

    if subject == 'ElectricalLocoPilot':
        for i in arr:
            if i == '1.1':
                names.append('चालक,अचालक एवं कुचालक')
                numbers.append(i)
            if i == '2.1':
                names.append('बेसिक इलेक्ट्रिकल')
                numbers.append(i)
            if i == '3.1':
                names.append('विद्युत सेल')
                numbers.append(i)
            if i == '4.1':
                names.append('संधारित्र')
                numbers.append(i)
            if i == '5.1':
                names.append('चुम्बक')
                numbers.append(i)
            if i == '6.1':
                names.append('डी.सी.जनित्र')
                numbers.append(i)
            if i == '7.1':
                names.append('डी.सी.मोटर')
                numbers.append(i)
            if i == '8.1':
                names.append('ए.सी थ्योरी')
                numbers.append(i)
            if i == '9.1':
                names.append('भू-सम्पर्कन')
                numbers.append(i)
            if i == '10.1':
                names.append('विद्युय वायरिंग')
                numbers.append(i)
            if i == '11.1':
                names.append('विद्युत मापक यंत्र')
                numbers.append(i)
            if i == '12.1':
                names.append('ट्रांसफार्मर')
                numbers.append(i)
            if i == '13.1':
                names.append('प्रत्यावर्तक')
                numbers.append(i)
            if i == '14.1':
                names.append('तुल्यकालिक प्रेरण')
                numbers.append(i)
            if i == '15.1':
                names.append('ए.सी. मोटर')
                numbers.append(i)
            if i == '16.1':
                names.append('वाइंडिंग')
                numbers.append(i)
            if i == '17.1':
                names.append('विद्युत उत्पादन,ट्रांसमिशन एवं वितरण')
                numbers.append(i)
            if i == '18.1':
                names.append('प्रदीप्ति')
                numbers.append(i)
            if i == '19.1':
                names.append('इलेक्ट्रिक्स')
                numbers.append(i)
            if i == '20.1':
                names.append('व्यावसायिक एवं सावधानियां')
                numbers.append(i)

        return list(zip(names,numbers))

        if subject == 'FitterLocoPilot':
            for i in arr:
                if i == '1.1':
                    names.append('Introduction')
                    numbers.append(i)
                if i == '2.1':
                    names.append('Fitter tools')
                    numbers.append(i)
                if i == '3.1':
                    names.append('Sheet Metal Shop')
                    numbers.append(i)
                if i == '4.1':
                    names.append('Welding Theory')
                    numbers.append(i)
                if i == '5.1':
                    names.append('Soldering And Brazing')
                    numbers.append(i)
                if i == '6.1':
                    names.append('Physical and Mechanical Properties of Metals')
                    numbers.append(i)
                if i == '7.1':
                    names.append('Heat Treatment')
                    numbers.append(i)
                if i == '8.1':
                    names.append('Bearings')
                    numbers.append(i)
                if i == '9.1':
                    names.append('Drilling Machine')
                    numbers.append(i)
                if i == '10.1':
                    names.append('Lathe Machine')
                    numbers.append(i)
                if i == '11.1':
                    names.append('Grinding Machine')
                    numbers.append(i)
                if i == '12.1':
                    names.append('Power Transmission')
                    numbers.append(i)
                if i == '13.1':
                    names.append('Pipe And Pipe Fitting')
                    numbers.append(i)
                if i == '14.1':
                    names.append('Screw Threads')
                    numbers.append(i)
                if i == '15.1':
                    names.append('Gauge')
                    numbers.append(i)
                if i == '16.1':
                    names.append('Limits,Fits And Tolerance')
                    numbers.append(i)
                if i == '17.1':
                    names.append('Other Important Questions')
                    numbers.append(i)
                if i == '18.1':
                    names.append('Previous Year Exams Questions')
                    numbers.append(i)

            return list(zip(names,numbers))

        if subject == 'Civil_Loco_Pilot_Tech':
            for i in arr:
                if i == '2.1':
                    names.append('Land Surveying Basic Principal And Classification')
                    numbers.append(i)
                if i == '2.2':
                    names.append('Chain Surveying')
                    numbers.append(i)
                if i == '2.3':
                    names.append('Compass Surveying')
                    numbers.append(i)
                if i == '2.4':
                    names.append('Levelling')
                    numbers.append(i)
                if i == '2.5':
                    names.append('Minor Instruments')
                    numbers.append(i)
                if i == '2.6':
                    names.append('Computation Of Land')
                    numbers.append(i)
                if i == '2.7':
                    names.append('Plane Table Survey')
                    numbers.append(i)
                if i == '2.8':
                    names.append('Contours And Contouring')
                    numbers.append(i)
                if i == '2.9':
                    names.append('Theodolite Survey')
                    numbers.append(i)
                if i == '50.1':
                    names.append('Curve And Curves Setting')
                    numbers.append(i)
                if i == '12.1':
                    names.append('Bending moment and sheer force')
                    numbers.append(i)
                if i == '12.2':
                    names.append('Bending and sheer stress')
                    numbers.append(i)
                if i == '12.3':
                    names.append('Combined direct and bending stress')
                    numbers.append(i)
                if i == '12.4':
                    names.append('Slope and deflection')
                    numbers.append(i)
                if i == '12.5':
                    names.append('Principal stress and principle planes')
                    numbers.append(i)
                if i == '12.6':
                    names.append('Columns and struts')
                    numbers.append(i)
                if i == '12.7':
                    names.append('Trosion')
                    numbers.append(i)
                if i == '13.1':
                    names.append('Rivet Connection')
                    numbers.append(i)
                if i == '13.2':
                    names.append('Weld Connection')
                    numbers.append(i)
                if i == '13.3':
                    names.append('Tension Members')
                    numbers.append(i)
                if i == '13.4':
                    names.append('Compression Member')
                    numbers.append(i)
                if i == '13.5':
                    names.append('Steel Beams')
                    numbers.append(i)
                if i == '13.6':
                    names.append('Column base and Foundation')
                    numbers.append(i)
                if i == '13.7':
                    names.append('Steel root of trusses')
                    numbers.append(i)


            return list(zip(names,numbers))

        if subject == 'LocoPilot_Diesel':
            for i in arr:
                if i == '1.1':
                    names.append('Introduction to Engine & Development')
                    numbers.append(i)
                if i == '2.1':
                    names.append('Cylinder Head & Valve Assembly')
                    numbers.append(i)
                if i == '3.1':
                    names.append('Piston & Connecting Rod')
                    numbers.append(i)
                if i == '4.1':
                    names.append('Crank Shaft,Cam Shaft Fly Wheel & Bearing')
                    numbers.append(i)
                if i == '5.1':
                    names.append('Gas Turbine Marine & Statonery Engine')
                    numbers.append(i)
                if i == '6.1':
                    names.append('Cooling & Snake System')
                    numbers.append(i)
                if i == '7.1':
                    names.append('Intake & Exhaust System')
                    numbers.append(i)
                if i == '8.1':
                    names.append('Diesel Fuel Supply System')
                    numbers.append(i)
                if i == '9.1':
                    names.append('Emission Charging & Starting System')
                    numbers.append(i)
                if i == '10.1':
                    names.append('Troubleshooting')
                    numbers.append(i)

            return list(zip(names,numbers))


# for knimbus subjects
        if subject == 'Design and analysis of algorithm':
            for i in arr:
                if i == '1.1':
                    names.append('Divide and Conquer')
                    numbers.append(i)
                if i == '2.1':
                    names.append('Dynamic Programming')
                    numbers.append(i)
                if i == '3.1':
                    names.append('Introduction')
                    numbers.append(i)
                if i == '4.1':
                    names.append('Greedy Method')
                    numbers.append(i)

            return list(zip(names,numbers))

        if subject == 'CAT_Quantitative_Aptitude':
            for i in arr:
                if i == '11.1':
                    names.append('Geometry')
                    numbers.append(i)
            return list(zip(names,numbers))



def changeIndividualNames(i,subject):
    if subject == 'English':
        if i == '1.1':
            return 'Antonym'
        elif i == '1.2':
            return 'Synonym'
        elif i == '1.3':
            return 'One word substitution'
        elif i == '1.4':
            return 'Idioms & Phrases'
        elif i == '1.5':
            return 'Phrasal Verbs'
        elif i == '1.6':
            return 'Use of some verbs with particular nouns'
        elif i == '1.7':
            return 'Tense'
        elif i == '2.1':
            return 'Noun'
        elif i == '2.2':
            return 'Pronoun'
        elif i == '2.3':
            return 'Adjective'
        elif i == '2.4':
            return 'Articles'
        elif i == '2.5':
            return 'Verb'
        elif i == '2.6':
            return 'Adverb'
        elif i == '2.7':
            return 'Time & Tense'
        elif i == '2.8':
            return 'Voice'
        elif i == '2.9':
            return 'Non-Finites'
        elif i == '3.1':
            return 'Narration'
        elif i == '3.2':
            return 'Preposition'
        elif i == '3.3':
            return 'Conjunction'
        elif i == '3.4':
            return 'Subject verb agreement'
        elif i == '3.5':
            return 'Common Errors'
        elif i == '3.6':
            return 'Superfluous Expressions & Slang'



    if subject == 'General-Intelligence':
        if i == '1.1':
            return 'Paper Cutting and Folding'
        elif i == '1.2':
            return 'Mirror and Water Image'
        elif i == '1.3':
            return 'Embedded Figures'
        elif i == '1.4':
            return 'Figure Completion'
        elif i == '1.5':
            return 'Counting Embedded Figures'
        elif i == '1.6':
            return 'Counting in figures'
        elif i == '2.1':
            return 'Analogy'
        elif i == '2.2':
            return 'Multiple Analogy'
        elif i == '2.3':
            return 'Choosing the analogous pair'
        elif i == '2.4':
            return 'Number analogy (series pattern)'
        elif i =='2.5':
            return 'Number analogy (missing)'
        elif i == '2.6':
            return 'Alphabet based analogy'
        elif i == '2.7':
            return 'Mixed analogy'
        elif i == '3.1':
            return 'Series Completion (Diagram)'
        elif i == '3.2':
            return 'Analogy (Diagram)'
        elif i == '3.3':
            return 'Classification (Diagram)'
        elif i == '3.4':
            return 'Dice & Boxes'
        elif i == '2.8':
            return 'Ruled based analogy'
        elif i == '2.9':
            return 'Alphabet Test'
        elif i == '4.1':
            return 'Ranking'
        elif i == '5.1':
            return 'Matrix'
        elif i == '6.1':
            return 'Word Creation'
        elif i == '7.1':
            return 'Odd one out'
        elif i == '8.1':
            return 'Height'
        elif i == '9.1':
            return 'Direction'
        elif i =='10.1':
            return 'Statement & Conclusion'
        elif i == '11.1':
            return 'Venn Diagram'
        elif i == '12.1':
            return 'Missing number'
        elif i == '13.1':
            return 'Logical Sequence of words'
        elif i == '14.1':
            return 'Clock/Time'
        elif i == '15.1':
            return 'Mathematical Operations'
        elif i == '16.1':
            return 'Coding Decoding'
        elif i == '17.1':
            return 'Series Test'
        elif i == '18.1':
            return 'Syllogism'
        elif i == '19.1':
            return 'Blood Relation'
        elif i == '20.1':
            return 'Seating Arrangement'
        elif i == '22.1':
            return 'Calender Test'
        elif i == '28.1':
            return 'Symbols & Notations'












    if subject == 'Quantitative-Analysis':
            if i == '1.1':
                return 'Age'
            elif i == '2.1':
                return 'Alligation'
            elif i == '3.1':
                return 'Area'
            elif i == '4.1':
                return 'Average'
            elif i == '5.1':
                return 'Boat & Stream'
            elif i == '6.1':
                return 'Discount'
            elif i == '7.1':
                return 'Fraction'
            elif i == '8.1':
                return 'LCM & LCF'
            elif i == '9.1':
                return 'Number System'
            elif i == '10.1':
                return 'Percentage'
            elif i == '11.1':
                return 'Pipes & Cistern'
            elif i == '12.1':
                return 'Profit & Loss'
            elif i == '13.1':
                return 'Ratio'
            elif i == '14.1':
                return 'Simple Interest'
            elif i == '15.1':
                return 'Simplification'
            elif i == '16.1':
                return 'Speed & Distance'
            elif i == '17.1':
                return 'Square & Cube root'
            elif i == '18.1':
                return 'Surds & Indices'
            elif i == '19.1':
                return 'Time & Work'
            elif i == '20.1':
                return 'Train'
            elif i == '21.1':
                return 'Volume'
            elif i == '22.1':
                return 'Trigonometry'
            elif i == '23.1':
                return 'Partnership'
            elif i == '24.1':
                return 'Coumpound Interest'
            elif i == '25.1':
                return 'Decimals'


    if subject == 'General-Knowledge':
            if i == '1.1':
                return 'Inventions & Innovators'
            if i == '2.1':
               return 'Bird Sanctuary'
            if i == '3.1':
               return 'Books & Authors'
            if i == '4.1':
               return 'Countries, Capitals & Currencies'
            if i == '5.1':
               return 'Current Affairs'
            if i == '6.1':
               return 'Economics'
            if i == '7.1':
               return 'General Science'
            if i == '8.1':
               return 'Biology'
            if i == '9.1':
               return 'Chemistry'
            if i == '10.1':
               return 'Science & Technology'
            if i == '11.1':
               return 'Physics'
            if i == '12.1':
               return 'Geography'
            if i == '13.1':
               return 'National Organizations'
            if i == '14.1':
               return 'History'
            if i == '15.1':
               return 'Honors & Awards'
            if i == '16.1':
               return 'Important Dates'
            if i == '17.1':
               return 'Indian Agriculture'
            if i == '18.1':
               return 'Indian Constitution'
            if i == '19.1':
               return 'Indian Culture'
            if i == '20.1':
               return 'Indian Museums'
            if i == '21.1':
               return 'Polity (India)'
            if i == '22.1':
               return 'Sports'
            if i == '23.1':
               return 'Superlatives(India)'
            if i == '24.1':
               return 'Symbols of States (India)'
            if i == '25.1':
               return 'Tiger Reserve'
            if i == '26.1':
               return 'UNESCO Word Heritage Sites(India)'
            if i == '27.1':
               return 'World Organizations'
            if i == '28.1':
               return 'Polity (World)'

    if subject == 'General-Science':
            if i == '1.1':
                return 'गुरूत्व स्थूल पदार्थ के गुण व प्रकाशन'
            if i == '1.1':
                return 'लेंस व दर्पण'
            if i == '2.1':
                return 'आधुनिक भौतिकी'
            if i == '3.1':
                return 'विमिय तथा द्विविमिय'
            if i == '4.1':
                return 'कॉमन प्रश्नपत्र भौतिक शास्त्रा'
            if i == '5.1':
                return 'दाब घटाव प्रत्यासा'
            if i == '6.1':
                return 'ध्वनि'
            if i == '7.1':
                return 'मात्रक विभाएं मापन'
            if i == '8.1':
                return 'सदिश तथा अदिश'
            if i == '9.1':
                return 'कार्य,ऊर्जा व शक्ति'
            if i == '10.1':
                return 'कोशिका विज्ञान'
            if i == '12.1':
                return 'पादप जगत'
            if i == '13.1':
                return 'पादप शरीर क्रिया विज्ञान'
            if i == '14.1':
                return 'आर्थिक वनस्पति विज्ञान'
            if i == '15.1':
                return 'जन्तु विज्ञान'
            if i == '16.1':
                return 'जन्तु उत्तक एवं पोषण'
            if i == '17.1':
                return 'आनुवांशिक'
            if i == '18.1':
                return 'मानव स्वास्थ्य एवं रोग'
            if i == '19.1':
                return 'जैव प्रोद्यौगिक'
            if i == '20.1':
                return 'कम्प्यूटर एवं सूचना प्रोद्यौगिकी'




# group x subjects

    if subject == 'Defence-English':
            if i == '1.1':
                return 'Comprehension'
            if i == '2.1':
                return 'Judge Comprehension'
            if i == '3.1':
                return 'Inferences'
            if i == '4.1':
                return 'Vocabulary'
            if i == '5.1':
                return 'Composition'
            if i == '6.1':
                return 'Subject and Verb'
            if i == '7.1':
                return 'Verb and their use'
            if i == '8.1':
                return 'Sequence of tenses'
            if i == '9.1':
                return 'Transformation'
            if i == '10.1':
                return 'Grammer'
            if i == '11.1':
                return 'Spellings'
            if i == '12.1':
                return 'Word formation'
            if i == '11.1':
                return 'Antonyms& Synonyms'
            if i == '11.1':
                return 'Word Substitution'
            if i == '12.1':
                return 'Correct use of words'
            if i == '13.1':
                return 'Confusing words'
            if i == '14.1':
                return 'Word order'
            if i == '15.1':
                return 'Correct use of Adverbs'
            if i == '16.1':
                return 'Idioms and Phrases'
            if i == '17.1':
                return 'Use of simple idioms'
            if i == '18.1':
                return 'Use of common proverbs'
            if i == '19.1':
                return 'Direct/Indirect sentences'
            if i == '20.1':
                return 'Direct to Indirect form'
            if i == '21.1':
                return 'Indirect to Direct'
            if i == '22.1':
                return 'Active and Passive voice'
            if i == '23.1':
                return 'Active to Passive voice'
            if i == '22.1':
                return 'Passive to Active voice'
            if i == '50.1':
                return 'To be categorized'


    if subject == 'Defence-Physics':
            if i == '1.1':
                return 'Unit of Dimension'
            if i == '2.1':
                return 'Scalers&Vectors'
            if i == '3.1':
                return 'Motion in straight line'
            if i == '4.1':
                return 'Law of Motion'
            if i == '5.1':
                return 'Projectile Motion'
            if i == '6.1':
                return 'Circular Motion'
            if i == '7.1':
                return 'Friction '
            if i == '8.1':
                return 'Work power & Energy'
            if i == '9.1':
                return 'Collision'
            if i == '10.1':
                return 'Rotational motion % Moment of Inertia'
            if i == '11.1':
                return 'Gravitation'
            if i == '12.1':
                return 'Elasticity'
            if i == '13.1':
                return 'Fluid Pressure '
            if i == '14.1':
                return 'Viscocity& Flow of fluids'
            if i == '15.1':
                return 'Surface Tension'
            if i == '16.1':
                return 'Oscillations'
            if i == '17.1':
                return 'Thermometry'
            if i == '18.1':
                return 'Thermal Expansion'
            if i == '19.1':
                return 'Calorimetry'
            if i == '20.1':
                return 'Transmission of Heat'
            if i == '21.1':
                return 'Thermodynamics'
            if i == '22.1':
                return 'Kinetic Theory of gases'
            if i == '23.1':
                return 'Wave Motion'
            if i == '24.1':
                return 'Superposition of waves'
            if i == '25.1':
                return 'Speed of Sound'
            if i == '26.1':
                return 'Vibrations in air columns'
            if i == '27.1':
                return 'Vibration of Strings'
            if i == '28.1':
                return 'Dopplers Effect'
            if i == '29.1':
                return 'Musical Sound& Ultra sound'
            if i == '30.1':
                return 'Electric charge & Electric Field'
            if i == '31.1':
                return 'Gauss Theorem'
            if i == '32.1':
                return 'Electric Capacitance'
            if i == '33.1':
                return 'Electric Conduction'
            if i == '34.1':
                return 'Ohms Law'
            if i == '35.1':
                return 'Electromotive force & Electric cell'
            if i == '36.1':
                return 'Kirchoffs law & wheatstone bridge'
            if i == '37.1':
                return 'Potentiometer'
            if i == '38.1':
                return 'Heating effect of current'
            if i == '39.1':
                return 'Chemical effect of current'
            if i == '40.1':
                return 'Magnetic effect of current'
            if i == '41.1':
                return 'Electrical Instruments'
            if i == '42.1':
                return 'Magnetic Field'
            if i == '43.1':
                return 'Magnetic effects of matter & terrestrial\
                                magnetism'
            if i == '44.1':
                return 'Electromagnetic Induction'
            if i == '45.1':
                return 'Alternating Current'
            if i == '46.1':
                return 'Reflection of light'
            if i == '47.1':
                return 'Refraction of light'
            if i == '48.1':
                return 'Refraction at Spherical surface & by\
                                lenses'
            if i == '49.1':
                return 'Prism & scattering of light'
            if i == '50.1':
                return 'Optical instruments'
            if i == '51.1':
                return 'Human eye & defects of vision'
            if i == '52.1':
                return 'Wave theory of light'
            if i == '53.1':
                return 'Interferance & Deflection of light'
            if i == '54.1':
                return 'Polarization of light'
            if i == '55.1':
                return 'Photometry'
            if i == '56.1':
                return 'Dual nature of radiation & matter'
            if i == '57.1':
                return 'Electromagnetic waves'
            if i == '58.1':
                return 'Structure of Atom'
            if i == '59.1':
                return 'Radioactivity'
            if i == '60.1':
                return 'Nuclear fission & fusion'
            if i == '61.1':
                return 'Semi-conductor,diode & Transistors'
            if i == '62.1':
                return 'Digital electronics & logic gates'
    if subject == 'Defence-GK-CA':
            if i == '1.1':
                return 'General Science'
            if i == '1.2':
                return 'Civics'
            if i == '1.3':
                return 'Geography'
            if i == '1.4':
                return 'Current Events'
            if i == '1.5':
                return 'History'
            if i == '1.6':
                return 'Basic Computer Operation'
            if i == '1.7':
                return 'General Knowledge'








    if subject == 'GroupX-Maths':
            if i == '1.1':
                return 'Sets-Relations-Functions'
            if i == '2.1':
                return 'Trigonometric functions'
            if i == '3.1':
                return 'Inverse Trigonometric functions'
            if i == '4.1':
                return 'Complex numbers'
            if i == '5.1':
                return 'Quadratic eqations'
            if i == '6.1':
                return 'Sequence & Series'
            if i == '7.1':
                return 'Permutations'
            if i == '8.1':
                return 'Combination'
            if i == '9.1':
                return 'Binomial Theorem'
            if i == '10.1':
                return 'Coordinate Geometry'
            if i == '11.1':
                return 'Exponential Series'
            if i == '12.1':
                return 'Logarithmic Series'
            if i == '13.1':
                return 'Matrices'
            if i == '14.1':
                return 'Determinants'
            if i == '15.1':
                return 'Limit & Continuity'
            if i == '16.1':
                return 'Differentiation'
            if i == '17.1':
                return 'Application of Differentiation'
            if i == '18.1':
                return 'Indefinite Integrals'
            if i == '19.1':
                return 'Definite Integrals'
            if i == '20.1':
                return 'Application of Integration'
            if i == '21.1':
                return 'Diferential Equations'
            if i == '22.1':
                return 'Probability Statistics'
            if i == '23.1':
                return 'Properties of Triangle'
            if i == '24.1':
                return 'Height&Distance'

    if subject == 'MathsIITJEE10':
        if i == '1.1':
            return 'All Categories'


    if subject == 'MathsIITJEE11':
            if i == '1.1':
                return 'All Categories'


    if subject == 'MathsIITJEE12':
        if i == '1.1':
            return 'All Categories'


    if subject == 'PhysicsIITJEE10':
            if i == '1.1':
                return 'All Categories'


    if subject == 'PhysicsIITJEE11':
        if i == '1.1':
            return 'All Categories'

    if subject == 'PhysicsIITJEE12':
            if i == '1.1':
                return 'All Categories'


    if subject == 'ChemistryIITJEE10':
        if i == '1.1':
            return 'All Categories'


    if subject == 'ChemistryIITJEE11':
            if i == '1.1':
                return 'All Categories'

    if subject == 'ChemistryIITJEE12':
            if i == '1.1':
                return 'All Categories'

    # for locopilot
    if subject == 'ElectricalLocoPilot':
            if i == '1.1':
                return 'चालक,अचालक एवं कुचालक'
            if i == '2.1':
                return 'बेसिक इलेक्ट्रिकल'
            if i == '3.1':
                return 'विद्युत सेल'
            if i == '4.1':
                return 'संधारित्र'
            if i == '5.1':
                return 'चुम्बक'
            if i == '6.1':
                return 'डी.सी.जनित्र'
            if i == '7.1':
                return 'डी.सी.मोटर'
            if i == '8.1':
                return 'ए.सी थ्योरी'
            if i == '9.1':
                return 'भू-सम्पर्कन'
            if i == '10.1':
                return 'विद्युय वायरिंग'
            if i == '11.1':
                return 'विद्युत मापक यंत्र'
            if i == '12.1':
                return 'ट्रांसफार्मर'
            if i == '13.1':
                return 'प्रत्यावर्तक'
            if i == '14.1':
                return 'तुल्यकालिक प्रेरण'
            if i == '15.1':
                return 'ए.सी. मोटर'
            if i == '16.1':
                return 'वाइंडिंग'
            if i == '17.1':
                return 'विद्युत उत्पादन,ट्रांसमिशन एवं वितरण'
            if i == '18.1':
                return 'प्रदीप्ति'
            if i == '19.1':
                return 'इलेक्ट्रिक्स'
            if i == '20.1':
                return 'व्यावसायिक एवं सावधानियां'

    if subject == 'FitterLocoPilot':
            if i == '1.1':
                return 'Introduction'
            if i == '2.1':
                return 'Fitter tools'
            if i == '3.1':
                return 'Sheet Metal Shop'
            if i == '4.1':
                return 'Welding Theory'
            if i == '5.1':
                return 'Soldering And Brazing'
            if i == '6.1':
                return 'Physical and Mechanical Properties of Metals'
            if i == '7.1':
                return'Heat Treatment'
            if i == '8.1':
                return 'Bearings'
            if i == '9.1':
                return 'Drilling Machine'
            if i == '10.1':
                return 'Lathe Machine'
            if i == '11.1':
                return 'Grinding Machine'
            if i == '12.1':
                return 'Power Transmission'
            if i == '13.1':
                return 'Pipe And Pipe Fitting'
            if i == '14.1':
                return 'Screw Threads'
            if i == '15.1':
                return 'Gauge'
            if i == '16.1':
                return 'Limits,Fits And Tolerance'
            if i == '17.1':
                return 'Other Important Questions'
            if i == '18.1':
                return 'Previous Year Exams Questions'
        
        
    if subject == 'Civil_Loco_Pilot_Tech':
            if i == '2.1':
                return 'Land Surveying Basic Principal And Classification'
            if i == '2.2':
                return 'Chain Surveying'
            if i == '2.3':
                return 'Compass Surveying'
            if i == '2.4':
                return 'Levelling'
            if i == '2.5':
                return 'Minor Instruments'
            if i == '2.6':
                return 'Computation Of Land'
            if i == '2.7':
                return 'Plane Table Survey'
            if i == '2.8':
                return 'Contours And Contouring'
            if i == '2.9':
                return 'Theodolite Survey'
            if i == '50.1':
                return 'Curve And Curves Setting'
            if i == '12.1':
                return 'Bending moment and sheer force'
            if i == '12.2':
                return 'Bending and sheer stress'
            if i == '12.3':
                return 'Combined direct and bending stress'
            if i == '12.4':
                return 'Slope and deflection'
            if i == '12.5':
                return 'Principal stress and principle planes'
            if i == '12.6':
                return 'Columns and struts'
            if i == '12.7':
                return 'Trosion'
            if i == '13.1':
                return 'Rivet Connection'
            if i == '13.2':
                return 'Weld Connection'
            if i == '13.3':
                return 'Tension Members'
            if i == '13.4':
                return 'Compression Member'
            if i == '13.5':
                return 'Steel Beams'
            if i == '13.6':
                return 'Column base and Foundation'
            if i == '13.7':
                return 'Steel root of trusses'


    if subject == 'LocoPilot_Diesel':
        if i == '1.1':
            return 'Introduction to Engine & Development'
        if i == '2.1':
            return 'Cylinder Head & Valve Assembly'
        if i == '3.1':
            return 'Piston & Connecting Rod'
        if i == '4.1':
            return 'Crank Shaft,Cam Shaft Fly Wheel & Bearing'
        if i == '5.1':
            return 'Gas Turbine Marine & Statonery Engine'
        if i == '6.1':
            return 'Cooling & Snake System'
        if i == '7.1':
            return 'Intake & Exhaust System'
        if i == '8.1':
            return 'Diesel Fuel Supply System'
        if i == '9.1':
            return 'Emission Charging & Starting System'
        if i == '10.1':
            return 'Troubleshooting'


# or knimbus subjects
    if subject == 'Design and analysis of algorithm':
            if i == '1.1':
                return 'Divide and Conquer'
            if i == '2.1':
                return 'Dynamic Programming'
            if i == '3.1':
                return 'Introduction'
            if i == '4.1':
                return 'Greedy Method'

    if subject == 'CAT_Quantitative_Aptitude':
                if i == '11.1':
                    return 'Geometry'







#-------------------------------
#algorithms for question data analytics in QuestionsAndPapers Model


def helper_weakIntesityAverage(total_arr):
    quest_categories = []
    if total_arr:
        for ka in total_arr:
            for ta in ka:
                for al in ta.allAnswers:
                    try:
                        quest = SSCquestions.objects.get(choices__id = al)
                    except Exception as e:
                        print(str(e))
                        continue
                    quest_categories.append(quest.topic_category)
                for sk in ta.skippedAnswers:
                    try:
                        quest = SSCquestions.objects.get(id = sk)
                    except Exception as e:
                        print(str(e))
                        continue
                    quest_categories.append(quest.topic_category)
    return quest_categories


def helper_weakAreas_Intensity(old_ids,subject):

    wrong_Answers = []
    skipped_Answers = []
    # if onetest object is present then adds all the wrong and skipped
    # answers to separate lists
    for test in old_ids:
        for wa in test.wrongAnswers:
            wrong_Answers.append(wa)
        for sa in test.skippedAnswers:
            skipped_Answers.append(sa)
    wq=[]
    for i in wrong_Answers:
        if self.institution == 'School':
            qu = Questions.objects.get(choices__id = i)
        elif self.institution == 'SSC':
        # finds the questions objects of wrong questions
            try:
                qu = SSCquestions.objects.get(choices__id = i)
            except Exception as e:
                print(str(e))
                continue
            if subject == 'SSCMultipleSections' or subject ==\
            'Defence-MultipleSubjects':
                quid = qu.id
                wq.append(quid)
            else:
                if qu.section_category == subject:
                    quid = qu.id
                    wq.append(quid)
    for i in skipped_Answers:
        if self.institution == 'School':
            try:
                qu = Questions.objects.get(id = i)
            except Exception as e:
                print(str(e))
                continue
        elif self.institution == 'SSC':
        # finds the questions objects of skipped questions
            try:
                qu = SSCquestions.objects.get(id = i)
            except Exception as e:
                print(str(e))
                continue
            if subject == 'SSCMultipleSections'or subject ==\
            'Defence-MultipleSubjects':
                quid = qu.id
                wq.append(quid)
            else:
                if qu.section_category == subject:
                    quid = qu.id
                    wq.append(quid)
    # finds unique questions with thier frequency
    unique, counts = np.unique(wq, return_counts=True)
    waf = np.asarray((unique, counts)).T
    nw_ind = []
    # sorts the list
    kk = np.sort(waf,0)[::-1]
    for u in kk[:,1]:
        for z,w in waf:
            if u == w:
                if z in nw_ind:
                    continue
                else:
                    nw_ind.append(z)
                    break
    final_freq = np.asarray((nw_ind,kk[:,1])).T
    arr = final_freq

    catSubject = []
    catCategory = []
    anal = []
    num = []
    for u,k in arr:
        if self.institution == 'School':
            qu = Questions.objects.get(id = u)
        elif self.institution == 'SSC':
            qu = SSCquestions.objects.get(id = u)
        if subject == 'SSCMultipleSections'or subject ==\
            'Defence-MultipleSubjects':
            quest_cat = qu.topic_category
            quest_sub = qu.section_category
            name_cat = self.changeIndividualNames(quest_cat,quest_sub)
            anal.append(name_cat)
            num.append(k)
        else:
            category = qu.topic_category
            anal.append(category)
            num.append(k)
    analysis = list(zip(anal,num))
    final_analysis = []
    final_num = []
    for u,k in analysis:
        if u in final_analysis:
            ind = final_analysis.index(u)
            temp = final_num[ind]
            final_num[ind] = temp + k
        else:
            final_analysis.append(u)
            final_num.append(k)

    waf = list(zip(final_analysis,final_num))
    return waf




#post_save.connect(checking_signals, sender = SSCOnlineMarks)
