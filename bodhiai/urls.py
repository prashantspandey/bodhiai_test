"""bodhiai URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from bodhiai import views

admin.site.site_header = "Bodhi AI Administration"
admin.site.site_title = "Bodhi AI"
admin.site.index_title = "Bodhi AI"

app_name = 'homeBodhi'

urlpatterns = [
    url(r'^$', views.index,name='bodhiHome' ),
    url(r'^bodhi/', include('basicinformation.urls')),
    url(r'^membership/', include('membership.urls')),
    url(r'^questions/',include('QuestionsAndPapers.urls')),
    url(r'^pMessages/',include('Private_Messages.urls')),
    url(r'^recommendations/',include('Recommendations.urls')),
    url(r'^api/basicinformation/',include('basicinformation.api.urls',namespace='basic-api')),
    url(r'^api/messages/',include('Private_Messages.api.urls',namespace='message-api')),
    url(r'^api/papers/',include('QuestionsAndPapers.api.urls',namespace='paper-api')),
    url(r'^api/membership/',include('membership.api.urls',namespace='membership-api')),
    url(r'^api/learning/',include('learning.api.urls',namespace='learning-api')),
    url(r'^api/recommendations/',include('Recommendations.api.urls',namespace='recommendations-api')),
    url(r'^api/chatbox/',include('chatbox.api.urls',namespace='chatbox-api')),
    url(r'^admin/', admin.site.urls),
    url(r'^interested/', views.interested_people,name='InterestedPeople'),
    url(r'^rest-auth/',include('rest_auth.urls')),
    url(r'^accounts/',include('allauth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
]
