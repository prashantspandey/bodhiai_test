from django.contrib.auth.models import User,Group
from django import forms
from django.contrib.auth.forms import UserCreationForm
from basicinformation.models import *
from basicinformation.tasks import *


class LoginForm(forms.ModelForm):
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

class RegisterForm(UserCreationForm):


    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'password1',
            'password2'
        )
    def save(self,commit = True,*args,**kwargs):
        user = super(RegisterForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        try:
            course = kwargs.get('course')
            print('{} this is the real course'.format(course))
            print('found course')
        except:
            course = None
            print('couldnot  found course')
        if commit:
            user.save()
            gr = Group.objects.get(name='Students')
            gr.user_set.add(user)
            print('{} this is the real course'.format(course))
            if course == None:
                print('course is non')
                school = School.objects.get(name='BodhiAI')
                cl = klass.objects.get(school__name='BodhiAI')
                stu = Student(studentuser=user, klass=cl,
                                  name=user.first_name, school= school)
                stu.save()
                bodhi_teacher = Teacher.objects.get(name = 'BodhiAI')
                submaths = Subject(name='Quantitative-Analysis', student=stu,
                                   teacher = bodhi_teacher)
                subgi = Subject(name='General-Intelligence', student=stu,
                                teacher=bodhi_teacher)
                subenglish = Subject(name='English', student=stu, teacher=
                                     bodhi_teacher)
                subgk = Subject(name='General-Knowledge',
                                student=stu, teacher= bodhi_teacher)
                submaths.save()
                subgi.save()
                subenglish.save()
                subgk.save()
                #mail_at = signup_mail.delay(user.email,stu.name)
            elif str(course.lower()) == 'jito':
                if str(course.lower()) == 'jito':
                    return user
                else:
                    print('Course is  none')
            elif str(course).lower() == 'siel':
                return user
            elif str(course).lower() == 'jen':
                print('returning from jen save')
                return user
            else:
                pass
            #else:
            #    print('Indeed i am none')
            #    school = School.objects.get(name='BodhiAI')
            #    print('%s-- school' %school)
            #    cl = klass.objects.get(school__name='BodhiAI')
            #    print('%s -- class' %cl)
            #    stu = Student(studentuser=user, klass=cl,
            #                      name=user.first_name, school= school)
            #    stu.save()
            #    bodhi_teacher = Teacher.objects.get(name = 'BodhiAI')
            #    submaths = Subject(name='Quantitative-Analysis', student=stu,
            #                       teacher = bodhi_teacher)
            #    subgi = Subject(name='General-Intelligence', student=stu,
            #                    teacher=bodhi_teacher)
            #    subenglish = Subject(name='English', student=stu, teacher=
            #                         bodhi_teacher)
            #    subgk = Subject(name='General-Knowledge',
            #                    student=stu, teacher= bodhi_teacher)
            #    submaths.save()
            #    subgi.save()
            #    subenglish.save()
            #    subgk.save()






        return user

class StudentInformationForm(forms.ModelForm):
    #kl = forms.ChoiceField(label='Class',widget=forms.Select())
    class Meta:
        model = StudentCustomProfile
        fields = ['address', 'phone','kl','fatherName','fullName']
        labels = {
                'address':'Address',
                'phone':'Phone',
                'kl': 'Class',
                'fatherName':'Father\'s Name',
                'fullName':'Full Name',
        }

class StudentForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['phone','code']
        labels = {
                'phone':'Phone',
                'code':'Code',
        }




