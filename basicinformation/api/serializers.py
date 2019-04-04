from rest_framework import serializers
from basicinformation.models import *
from QuestionsAndPapers.models import *


class SchoolDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = [
            'name',
        ]

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = [
            'id',
            'name',
            'school',
        ]

class BatchSerializer(serializers.ModelSerializer):
    school = SchoolDisplaySerializer()
    class Meta:
        model = klass
        fields = [
            'id',
            'name',
            'school',
        ]

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentLanguage
        fields = [
            'language',
        ]


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCourse
        fields = [
            'course',
        ]




class BatchNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = klass
        fields = [
            'id',
            'name',
        ]
class StudentModelSerializer(serializers.ModelSerializer):
    klass = BatchNameSerializer()
    class Meta:
        model = Student
        fields = [
            'id',
            'name',
            'klass',
        ]

    #def get_user(self,obj):
    #    return str(obj.studentuser.email)
class StudentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',            
            'username',
            'email',
            'first_name'
        ]

class SSCOnlineMarksModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SSCOnlineMarks
        fields = [
            'marks',
            'testTaken'
        ]


class TimeTableModelSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()
    batch = BatchSerializer()
    class Meta:
        model = TimeTable
        fields = [
            'date',
            'timeStart',
            'timeEnd',
            'teacher',
            'batch',
            'sub',
            'note',

        ]


class StudentProfileDetailsSerializer(serializers.ModelSerializer):
    #language = LanguageSerializer()
    course = CourseSerializer()
    class Meta:
        model = StudentDetails
        fields = [
            'id',
            'fullName',
            'photo',
            'phone',
            'address',
            'email',
            'fatherName',
            'parentPhone',
            'language',
            'course',
            'username'

        ]


class StudentTimingChapterwiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAverageTimingDetailCache
        fields = [
            'id',
            'student',
            'subject',
            'chapter',
            'rightAverage',
            'wrongAverage',
            'totalAverage',
            'rightTotalTime',
            'wrongTotalTime',
            'rightTotal',
            'wrongTotal',
            'totalAttempted',

        ]
    def validate(self,validated_data):
        chapter_code = validated_data['chapter']
        print('{} this is the chapter code'.format(chapter_code))
        chapter_name =\
        SubjectChapters.objects.get(subject=validated_data['subject'],code=validated_data['chapter'])
        validated_data['chapter']= chapter_name.name
        print('{} this is the validated data'.format(validated_data))
        return validated_data

