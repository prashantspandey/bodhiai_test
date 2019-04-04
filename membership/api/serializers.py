from rest_framework import serializers
from membership.models import *
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from basicinformation.api.serializers import *
from QuestionsAndPapers.api.serializers import *
from rest_framework import exceptions


class CustomRegistrationSerializer(serializers.ModelSerializer):
   username =\
   serializers.CharField(max_length=30,validators=[UniqueValidator(queryset=User.objects.all(),message=\
   "This username already exists. / यह यूजरनाम पहले से उपस्थित है , कृपया दूसरा यूजरनाम चुने "

                                                                  )])
   password = serializers.CharField(min_length=8,write_only=True)
   first_name = serializers.CharField(max_length=100)

   def create(self,validated_data):
       print(validated_data['username'])
       print(validated_data['password'])
       print(validated_data['first_name'])
       user =\
       User.objects.create_user(username=validated_data['username'],password = validated_data['password'],first_name
                                =validated_data['first_name'])
       return user

   class Meta:
       model = User
       fields = [
           'id',
           'username',
           'first_name',
           'password',

       ]


class StudentConfirmationSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()
    student = StudentDetailSerializer()
    school = SchoolDisplaySerializer()
    batch = BatchNameSerializer()
    class Meta:
       model = StudentConfirmation

       fields = [
           'id',
           'name',
           'student',
           'teacher',
           'batch',
           'school',
           'phone',
           'confirm',
       ]

class CustomLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self,data):
        username = data.get("username","")
        password = data.get("password","")

        if username and password:
            user = authenticate(username=username,password=password)
            if user:
                if user.is_active:
                    data["user"] = user
                else:
                    message = "User is deactivated / आपको डीएक्टिवेट कर दिया गया है "
                    raise exceptions.ValidationError(message)
            else:
                message = "Wrong username or password !! /यूजरनाम या पासवर्ड गलत है .  "
                raise exceptions.ValidationError(message)
            pass
        else:
            message = "Please provide both username and password./\
कृपया उपयोगकर्ता नाम और पासवर्ड दोनों लिखें।"
            raise exceptions.ValidationError(message)
        return data
