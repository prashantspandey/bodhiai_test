from django.conf.urls import url
from membership import views as membershipviews

app_name = 'membership'

urlpatterns = [
    url(r'^$', membershipviews.user_login, name='login'),
    # client logins
    url(r'^siel_login/$', membershipviews.siel_user_login, name='SielLogin'),
    url(r'^swami_login/$', membershipviews.srw_user_login, name='SwamiLogin'),
    url(r'^jen_login/$', membershipviews.jen_user_login, name='JENLogin'),
    url(r'^ysm_login/$', membershipviews.jen_user_login, name='YSMLogin'),
    # client logouts
    url(r'^siel_logout/$', membershipviews.siel_logout, name='SielLogout'),
    url(r'^srw_logout/$', membershipviews.srw_logout, name='srwLogout'),
    url(r'^jen_logout/$', membershipviews.jen_logout, name='jenLogout'),
    url(r'^ysm_logout/$', membershipviews.jen_logout, name='ysmLogout'),
    url(r'^register/', membershipviews.user_register, name='register'),
    url(r'^logout/$', membershipviews.user_logout, name='logout'),
    url(r'^change_password/$', membershipviews.user_changePassword,
        name='changePassword'),

]
