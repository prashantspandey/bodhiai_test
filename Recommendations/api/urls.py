from django.conf.urls import url
from ..api import views

urlpatterns = [
    url(r'chapter_recommendations/$',views.StudentChapterYoutubeRecommendationsAPIView.as_view(),name='ChapterRecommendations'),
    url(r'chapterwise_video/$',views.StudentChapterWiseRecommendationAPIView.as_view(),name='ChapterwiseRecommendation'),
]
