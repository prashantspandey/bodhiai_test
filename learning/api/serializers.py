from rest_framework import serializers
from basicinformation.models import *
from QuestionsAndPapers.models import *
from learning.models import *


class SubjectChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectChapters
        fields = [
            'id',
            'name',
            'code',

        ]


