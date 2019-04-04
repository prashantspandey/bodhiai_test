from Private_Messages.models import *
from rest_framework import serializers
from basicinformation.api.serializers import *

class PrivateMessageModalSerializer(serializers.ModelSerializer):
    sender = StudentDetailSerializer()
    class Meta:
        model = PrivateMessage
        fields = [
            'sender',
            'receiver',
            'subject',
            'body',
            'sent_date',

        ]

class AnnouncementSerializer(serializers.ModelSerializer):
    announcer = TeacherSerializer()
    listener = StudentModelSerializer()
    class Meta:
        model = Announcement
        fields = [
            'announcer',
            'listener',
            'text',
            'date',
        ]
