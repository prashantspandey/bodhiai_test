from django.conf.urls import url
from chatbox.api import views


urlpatterns = [
    url(r'^$',views.ChatBoxAPIView.as_view(),name='chatBox'),
    url(r'saveChat/$',views.saveBodhiChatAPIView.as_view(),name='saveChat'),
    url(r'getChat/$',views.getBodhiChatAPIView.as_view(),name='getChat'),
] 
