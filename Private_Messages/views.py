from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from django.http import Http404, HttpResponse
from django.contrib.auth.models import User, Group
from django.contrib import messages 
from basicinformation.models import Subject,Teacher,Student
from .models import *
from basicinformation.marksprediction import *
from django.utils import timezone
def inbox(request):
    user = request.user
    if user.is_authenticated:
        messages = PrivateMessage.objects.filter(receiver = user)
        context = {'inbox' : messages}
        return render(request,'Private_Messages/all_messages.html',context)
    else:
        raise Http404('Not allowed')
def every_messages(request):
    user = request.user
    if user.is_authenticated:
        # shows all teachers that a student can send message to 
        if user.groups.filter(name='Students').exists():
            profile = user.student
            sub = profile.subject_set.all()
            my_teachers = []
            for su in sub:
                my_teachers.append(su.teacher)
            # deletes identicle entries
            my_teachers = list(unique_everseen(my_teachers))
            # all messages that student has received(just for counting)
            my_messages = PrivateMessage.objects.filter(receiver= user)
            # count number of messages student has received
            count = 0
            for i in my_messages:
                count = count + 1
            context = {'teachers':my_teachers,'count':count,'isTeacher':False}
            return render(request,'Private_Messages/messages.html',context) 
        # exactly same as the student above
        if user.groups.filter(name='Teachers').exists():
            profile = user.teacher
            sub = profile.subject_set.all()
            my_students = []
            for su in sub:
                my_students.append(su.student)
            my_students = list(unique_everseen(my_students))
            my_messages = PrivateMessage.objects.filter(receiver= user)
            count = 0
            for i in my_messages:
                count = count + 1
            context = {'teachers':my_students,'count':count,'isTeacher':True}
            return render(request,'Private_Messages/messages.html',context) 
        # shows all the teachers and students management can send messages to
        if user.groups.filter(name='Management').exists():
            profile = user.schoolmanagement
            teachers = Teacher.objects.filter(school = profile.school)
            students = Student.objects.filter(school = profile.school)
            all_entities = []
            for i in teachers:
                all_entities.append(i)
            for i in students:
                all_entities.append(i)
            all_entities = list(unique_everseen(all_entities))
            context = {'teachers':all_entities}
            return render(request,'Private_Messages/messages.html',context)


def send_messages(request):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name='Students').exists():
            if 'teacher_name' in request.GET:
                # gets teachername(id) from the get method 
                teacher_name = request.GET['teacher_name']
                teacher_id = int(teacher_name)
                s_id = teacher_id
                teacher = Teacher.objects.get(id = teacher_id)
                # creates a new PrivateMessage in teacher's name and sends to
                # template
                new_Message = PrivateMessage()
                new_Message.sender = user
                new_Message.receiver = teacher.teacheruser
                context = {'message_info':new_Message,'who':'student','sid':s_id}
                return render(request,'Private_Messages/send_message.html',context)
            # fires when student puts in all the fields (subject and body)
            if 'receiver' in request.POST and 'subject' in request.POST and 'body'  in  request.POST:
                profile = user.student
                sub = profile.subject_set.all()
                my_teachers = []
                for su in sub:
                    my_teachers.append(su.teacher)
                my_teachers = list(unique_everseen(my_teachers))
                my_messages = PrivateMessage.objects.filter(receiver= user)
                count = 0
                for i in my_messages:
                    count = count + 1
                subject = request.POST['subject']
                receiver = request.POST['receiver']
                body = request.POST['body']
                teacher = Teacher.objects.get(id = int(receiver))
                post_message = PrivateMessage()
                post_message.sender = user
                post_message.receiver = teacher.teacheruser
                post_message.subject = subject
                # runs when body is empty(creates an error message)
                if body == '':
                    messages.error(request, 'Please fill the Message. ')
                    context ={'messagain':teacher,'teachers':my_teachers,
                              'count':count}
                    return render(request,'Private_Messages/messages.html',context)
                else:
                    post_message.body = body
                    post_message.save()
                    context = {'mess':post_message,'created':True}
                    return render(request,'Private_Messages/successfullySent.html',context)
        if user.groups.filter(name='Teachers').exists():
            # same as above
            if 'teacher_name' in request.GET:
                student_id = request.GET['teacher_name']
                s_id = int(student_id)
                student = Student.objects.get(id = int(student_id))
                new_Message = PrivateMessage()
                new_Message.sender = user
                new_Message.receiver = student.studentuser
                
                context = {'message_info':new_Message,'sid':s_id,
                           }
                return render(request,'Private_Messages/send_message.html',context)
            if 'receiver' in request.POST and 'subject' in request.POST and 'body'  in  request.POST:
                profile = user.teacher
                sub = profile.subject_set.all()
                my_students = []
                for su in sub:
                    my_students.append(su.student)
                my_messages = PrivateMessage.objects.filter(receiver= user)
                count = 0
                for i in my_messages:
                    count = count + 1
                subject = request.POST['subject']
                receiver = request.POST['receiver']
                body = request.POST['body']
                student = Student.objects.get(id = receiver)
                post_message = PrivateMessage()
                post_message.sender = user
                post_message.receiver = student.studentuser
                post_message.subject = subject
                if body == '':
                    messages.error(request, "Message Body can't be empty")
                    context = {'messagain':student,'teachers':my_students,'count':count}
                    return render(request,'Private_Messages/messages.html',context)
                else:
                    post_message.body = body
                    post_message.save()
                    context = {'mess':post_message,'created':True}
                    return render(request,'Private_Messages/successfullySent.html',context)
        if user.groups.filter(name='Management').exists():
            if 'teacher_name' in request.GET:
                entity_id = request.GET['teacher_name']
                entity_id = int(entity_id)
                print('%s entity id' %entity_id)
                new_Message = PrivateMessage()
                new_Message.sender = user

                try:
                    student = Student.objects.get(id = entity_id)
                    new_Message.receiver = student.studentuser
                except:
                    teacher = Teacher.objects.get(id = entity_id)
                    new_Message.receiver = teacher.teacheruser
                
                context = {'message_info':new_Message,'sid':entity_id,
                           }
                return render(request,'Private_Messages/send_message.html',context)
            if 'receiver' in request.POST and 'subject' in request.POST and 'body'  in  request.POST:
                profile = user.schoolmanagement
                teachers = Teacher.objects.filter(school = profile.school)
                students = Student.objects.filter(school = profile.school)
                all_entities = []
                for i in teachers:
                    all_entities.append(i)
                for i in students:
                    all_entities.append(i)

                my_messages = PrivateMessage.objects.filter(receiver= user)
                count = 0
                for i in my_messages:
                    count = count + 1
                subject = request.POST['subject']
                receiver = request.POST['receiver']
                body = request.POST['body']
                post_message = PrivateMessage()
                post_message.sender = user
                try:
                    teacher = Teacher.objects.get(id = int(receiver))
                    post_message.receiver = teacher.teacheruser
                except:
                    student = Student.objects.get(id = int(receiver))
                    post_message.receiver = student.studentuser
                post_message.subject = subject
                if body == '':
                    messages.error(request, 'Please fill the Message. ')
                    try:
                        context ={'messagain':teacher,'teachers':all_entities,
                                'count':count}
                    except:
                        context ={'messagain':student,'teachers':all_entities,
                                'count':count}

                    return render(request,'Private_Messages/messages.html',context)
                else:
                    post_message.body = body
                    post_message.save()
                    context = {'mess':post_message,'created':True}
                    return render(request,'Private_Messages/successfullySent.html',context)


def view_sent_messages(request):
    user = request.user
    if user.is_authenticated:
        sent_messages = PrivateMessage.objects.filter(sender = user)
        context = {'sent_messages':sent_messages}
        return render(request,'Private_Messages/sent_messages.html',context)
    else:
        raise Http404('Please login to see messages')


# functions for Announcement

def home_announcement(request):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name='Teachers').exists():
            me = Teach(user)
            klasses = me.my_classes_names()
            annoucements = Announcement.objects.filter(announcer =
                                                       user.teacher)
            context = {'klasses':klasses,'announcements':annoucements}
            return \
        render(request,'Private_Messages/create_announcement.html',context)
        else:
            raise Http404('Wrong page kid')

def create_annoucement(request):
    user = request.user
    if user.is_authenticated:
        if request.POST:
            kla = request.POST['which_class']
            text = request.POST['announcement']
            print(klass)
            print(text)
            print(user.teacher)
            newAnnouncement = Announcement()
            newAnnouncement.announcer = user.teacher
            newAnnouncement.text = text
            newAnnouncement.date = timezone.now()
            newAnnouncement.save()
            kl = klass.objects.get(name = kla, school =
                                   user.teacher.school)
            students = Student.objects.filter(klass = kl)
            for st in students:
                newAnnouncement.listener.add(st)
            context = {'announcement':newAnnouncement}
            return render(request,'Private_Messages/success_announced.html',context)


















