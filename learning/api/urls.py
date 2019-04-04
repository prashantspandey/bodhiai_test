from django.conf.urls import url
from learning.api import views

urlpatterns = [
    url(r'learning_subjects/$',views.StudentSubjectsAPIView.as_view(),name='LearningSubjects'),
    url(r'learning_chapters/$',views.StudentGetChaptersAPIView.as_view(),name='GetChapters'),
    url(r'learning_concepts/$',views.StudentGetCoceptsAPIView.as_view(),name='GetConcepts'),
    url(r'concept_content/$',views.StudentGetContentAPIView.as_view(),name='GetContent'),
    url(r'teacher_subjects/$',views.TeacherSubjectsAPIView.as_view(),name='TeacherSubjects'),
    url(r'teacher_chapters/$',views.TeacherGetChaptersAPIView.as_view(),name='TeacherChapters'),
    url(r'teacher_chapters/$',views.TeacherGetChaptersAPIView.as_view(),name='TeacherChapters'),
    url(r'course_subjects/$',views.CourseSubjects.as_view(),name='CourseSubjects'),
]
