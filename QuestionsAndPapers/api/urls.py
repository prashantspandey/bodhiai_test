from django.conf.urls import url
from QuestionsAndPapers.api import views

urlpatterns = [
    url(r'paper_details/$',views.StudentPaperDetailsAPIView.as_view(),name='PaperDetails'),
    url(r'paper_details_android/$',views.StudentPaperDetailsAndroidAPIView.as_view(),name='PaperDetailsAndroid'),
    url(r'paper_details_filter/$',views.StudentPaperDetailsFilter.as_view(),name='PaperDetailsFilter'),
    url(r'paper_details_android_paginated/$',views.StudentPaperDetailsAndroidPaginatedAPIView.as_view(),name='PaperDetailsAndroidPaginated'),
    url(r'all_topics_paper/$',views.StudentShowAllTopicsOfTest.as_view(),name='AllTopics'),
    url(r'individual_test_details/$',views.IndividualTestDetailsAPIView.as_view(),name='IndividualTestDetails'),
    # test taking apis
    url(r'individual_test_first/$',views.ConductTestFirstAPIview.as_view(),name='ConductTestFirst'),
    # Once click test apis
    url(r'teacher_one_click_first/$',views.TeacherOneClickTestOneAPIView.as_view(),name='OneClickOne'),
    url(r'teacher_one_click_subject/$',views.TeacherOneClickTestSubjectsAPIView.as_view(),name='OneClickSubjects'),
    url(r'teacher_one_click_chapters/$',views.TeacherOneClickTestChaptersAPIView.as_view(),name='OneClickChapters'),
    url(r'teacher_one_click_confirm/$',views.TeacherOneClickConfirmAPIView.as_view(),name='OneClickConfirm'),
    url(r'teacher_one_click_final/$',views.TeacherOneClickFinalAPIView.as_view(),name='OneClickFinal'),
    # Normal create test apis
    url(r'teacher_create_test_batches/$',views.CreateTestBatchesAPIView.as_view(),name='CreateTestBatches'),
    url(r'teacher_create_test_subjects/$',views.CreateTestSubjectsAPIView.as_view(),name='CreateTestSubjects'),
    url(r'teacher_create_test_chapters/$',views.CreateTestChaptersAPIView.as_view(),name='CreateTestChapters'),
    url(r'teacher_create_test_questions/$',views.CreateTestQuestionsAPIView.as_view(),name='CreateTestQuestions'),
    url(r'teacher_create_test_final/$',views.CreateTestFinalAPIView.as_view(),name='CreateTestFinal'),
    url(r'teacher_create_test/$',views.CreateTestAPIView.as_view(),name='CreateTestAPI'),
    # Student profile apis
    url(r'student_subjects/$',views.StudentSubjectsAPIView.as_view(),name='StudentSubjects'),
    # Student Take test APIs
    url(r'take_test/$',views.StudentTakeTestAPIView.as_view(),name='StudentTakeTest'),
    # Student evaluate test APIs
    url(r'evaluate_test_android/$',views.StudentEvaluateTestAPIView.as_view(),name='StudentEvaluateTest'),
    # Student smart test api for subjects
    url(r'smart_test_subjects/$',views.StudentSmartTestSubjectAPIView.as_view(),name='StudentSmartTestSubject'),
    # Student smart test creation
    url(r'smart_test_create/$',views.StudentSmartTestCreationAPIView.as_view(),name='StudentSmartTestCreation'),
    # Teacher Debug all questions
    url(r'get_questions/$',views.GetAllQuestions.as_view(),name='DebugQuestions'),
    # ssc questions test json
    url(r'test_json/$',views.test_json.as_view(),name='TestJson'),
    # get subject chapter tests for B2C
    url(r'subject_chapter_tests/$',views.getSubjectChapterTestAPIView.as_view(),name='TestSubjectChapter'),
    # Pattern Test check for pattern
    url(r'pattern_test_exams/$',views.CreatePatternTestCheckExam.as_view(),name='PatternTestCheckPattern'),
    # Pattern Test create test final
    url(r'pattern_test_create/$',views.CreatePatternTestFinal.as_view(),name='CreatePatternTestFinal'),
    # Teacher get subjects
    url(r'teacher_get_subjects/$',views.TeacherGetSubjects.as_view(),name='TeacherGetSubjects'),
    # get my mock tests
    url(r'student_get_mockTest/$',views.GetMockTests.as_view(),name='getMockTests'),
    # get my subject tests
    url(r'student_get_subjectwiseTest/$',views.GetSubjectTests.as_view(),name='getSubjectTests'),




]
