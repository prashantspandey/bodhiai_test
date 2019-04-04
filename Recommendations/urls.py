from django.conf.urls import url
from basicinformation import views

app_name = 'recommendations'

urlpatterns = [
    url(r'^$', views.home, name='home'),
]
