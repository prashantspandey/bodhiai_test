from django.conf.urls import url
from . import views

app_name = 'pms'

urlpatterns = [
    url(r'^inbox/$', views.inbox, name='inbox'),
    url(r'^$', views.every_messages, name='messages'),
    url(r'^send_message/$', views.send_messages, name='sendMessage'),
    url(r'^sent_messages/$', views.view_sent_messages, name='sentMessages'),
    url(r'^seeandcreate_announcements/$', views.home_announcement,
        name='createAnnouncement'),
    url(r'^create_annoucement/$', views.create_annoucement, name='Announce'),
    

    
] 
