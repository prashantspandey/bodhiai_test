from django.conf.urls import url
from Private_Messages.api import views

urlpatterns = [
        
    url(r'latestMessages/$',views.TeacherLatestInbox.as_view(),name='messageList'),
    # Student send messages
    url(r'student_send_message/$',views.StudentSendMessage.as_view(),name='StudentSendMessage'),
    url(r'student_send_message_sent/$',views.StudentSendMessageFinal.as_view(),name='StudentSendMessageFinal'),
    # Teacher create announcements
    url(r'teacher_create_announcement/$',views.TeacherCreateAnnouncementAPIView.as_view(),name='TeacherCreateAnnouncement'),
    url(r'teacher_create_announcement_final/$',views.TeacherCreateAnnouncemntFinalAPIView.as_view(),name='TeacherCreateAnnouncementFinal'),
    # Student see announcements
    url(r'student_announcements/$',views.StudentShowAnnnouncementAPIView.as_view(),name='StudentAnnouncements'),
    # Student Inbox
    url(r'student_inbox/$',views.StudentInbox.as_view(),name='StudentInbox'),


    
]
