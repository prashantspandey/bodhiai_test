from django.conf.urls import url
from basicinformation import views

app_name = 'basic'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'jito/$', views.jitoData, name='jitoHome'),
    url(r'how_it_works/$', views.howitworks, name='howitworks'),
    url(r'courses/$', views.showCourses, name='courses'),
    url(r'student_information/$', views.studentInformation, name='studentInfo'),
    url(r'add_students/$', views.teacher_student_confirmation,
        name='addStudents'),
    url(r'add_students2/$', views.teacher_confirmation,
        name='addStudents2'),

    url(r'^teacher/(?P<grade>\d+)/$', views.current_analysis,
        name='current_analysis'),

    url(r'teach/$',views.teacher_home_page, name= 'teacherHomePage'),

    url(r'teacher/update/$',views.teacher_update_page,name='teacher_update_page'),


    url(r'student_analysis/$',views.student_self_analysis, name= 'studentAnalysis'),

    url(r'student_subject_analysis/$',views.student_subject_analysis, name='studentSubjectAnalysis'),

    url(r'teacher_weakAreasinDetail/$',views.teacher_weakAreasinDetail,
        name='TeacherWeakAreas'),

    url(r'^adminPopulate/$', views.create_entities, name='createEntities'),

    url(r'studentWeakAreas/$',views.student_weakAreasSubject, name= 'studentWeakAreas'),

    url(r'studentWeakAreassub/$',views.student_weakAreas, name=
        'studentWA'),

    url(r'studentImprovement/$',views.student_improvement, name=
        'studentImprovement'),

    url(r'studentImprovement_sub/$',views.student_improvement_sub,
        name='studentImprovementsub'),

    url(r'studentTopicWiseTest/$',views.student_select_topicTest,
        name='studentTopicWiseTest'),

    url(r'downloadResult/$',views.teacher_download_result,name='downloadResult'),

    url(r'all_tests/$',views.student_moreTests,
        name='studentMoreTests'),
    
    url(r'managementInformation/$',views.management_information,name='managementInformation'),
    # click data collection
    url(r'bodhi_play_store/$',views.redirectPlayStore,name='playStoreRedirect'),

]
