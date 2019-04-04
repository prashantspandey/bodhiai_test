from rest_framework import serializers
from basicinformation.models import *
from QuestionsAndPapers.models import *
from learning.models import *
from Recommendations.models import *
from basicinformation.api.serializers import *
from QuestionsAndPapers.api.serializers import *


class ConceptsBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concepts

        fields = [
            'id',
            'name',
            'subject',
            'chapter',
            'concept_number'

        ]


