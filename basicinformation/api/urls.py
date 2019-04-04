from django.conf.urls import url
from basicinformation.api import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    url(r'^$',views.StudentListAPIView.as_view(),name='studentList'),
    url(r'user_type/$',views.TeacherorStudentAPIView.as_view(),name='UserType'),
    url(r'student_info/$',views.StudentDetailAPIView.as_view(),name='studentInfo'),
    url(r'last_test_performance_teacher/$',views.LastClassTestPerformanceTeacherAPI.as_view(),name='last_performance_teacher'),
    url(r'teacher_weak_areas_brief/$',views.TeacherWeakAreasBrief.as_view(),name='teacher_weak_areas_brief'),
    url(r'teacher_weak_areas_brief_android/$',views.TeacherWeakAreasBriefAndroid.as_view(),name='teacher_weak_areas_brief_Android'),
    url(r'teacher_weak_areas_detail/$',views.TeacherWeakAreasDetailAPIView.as_view(),name='TeacherWeakAreasDetailAPI'), 
    url(r'teacher_tests_overview/$',views.TeacherTestsOverview.as_view(),name='teacher_tests_overview'), 
    url(r'teacher_tests_overview_android/$',views.TeacherTestsOverviewAndroid.as_view(),name='teacher_tests_overview_Android'), 
    url(r'teacher_hard_questions/$',views.TeachersHardQuestionsAPIView.as_view(),name='TeacherHardQuestions'),
    url(r'teacher_hard_questions_latest/$',views.TeachersHardQuestions3TestsAPIView.as_view(),name='TeacherHardQuestionsLatest'),
    url(r'teacher_subjectNames/$',views.TeacherSubjectsAPIView.as_view(),name='TeacherSubjects'),
    url(r'teacher_classNames/$',views.TeacherBatchesAPIView.as_view(),name='TeacherBatches'),
    url(r'teacher_generateRankTable/$',views.GenerateRankTableAPIView.as_view(),name='TeacherGenerateRankTable'),
    url(r'teacher_TestBasicDetails/$',views.TeacherTestBasicDetailsAPIView.as_view(),name='TeacherTestBasicDetails'),
    url(r'teacher_TestQuestionsDetails/$',views.TeacherTestQuestionsAPIView.as_view(),name='TeacherTestQuestionsDetails'),
    url(r'student_previous_performance/$',views.StudentPreviousPerformanceBriefAPIView.as_view(),name='StudentPreviousPerformance'),
    url(r'student_previous_performance_android/$',views.StudentPreviousPerformanceBriefAndroidAPIView.as_view(),name='StudentPreviousPerformanceAndroid'),
    url(r'student_proficiency/$',views.StudentTopicWiseProficiency.as_view(),name='StudentProficiency'),
    url(r'student_proficiency_android/$',views.StudentTopicWiseProficiencyAndroid.as_view(),name='StudentProficiencyAndroid'),
    url(r'student_timing_topicwise/$',views.StudentAverageTimeTopicAPIView.as_view(),name='StudentTimingTopicWise'),
    url(r'student_timing_topicwise_android/$',views.StudentAverageTimeTopicAndroidAPIView.as_view(),name='StudentTimingTopicWiseAndroid'),
    url(r'student_previous_performance_detailed/$',views.StudentTakenTestsDetailsAPIView.as_view(),name='StudentPreviousPerformanceDetailed'),
# Time Table APIs
    url(r'teacher_time_table/$',views.TeacherTimeTableAPIView.as_view(),name='TeacherTimeTable'),
# teacher create Time Table
    url(r'teacher_create_TimeTable/$',views.TeacherCreateTimeTable.as_view(),name='TeacherCreateTimeTable'),
# teacher get batches for Time Table
    url(r'teacher_create_TimeTableBatches/$',views.TeacherTimeTableFirst.as_view(),name='TeacherTimeTableBatches'),
# Student Test Performance Detail
    url(r'student_individual_test_detail/$',views.StudentTestPerformanceDetailedAPIView.as_view(),name='StudentTestPastPerformanceDetail'),
# Custom Registration
    #url(r'custom_registration/$',views.CustomRegistrationAPIView.as_view(),name='CustomRegistration'),
# Student Test Rank
    url(r'student_test_rank/$',views.StudentFindMyRankAPIView.as_view(),name='StudentTestRank'),
# Teacher all Student List
    url(r'teacher_student_list/$',views.TeacherShowAllStudentsAPIView.as_view(),name='TeacherStudentList'),
# Student Show Profile
    url(r'student_profile/$',views.StudentShowDetialsAPIView.as_view(),name='StudentDetailsAPI'),
# Student Write Profile
    url(r'student_edit_profile/$',views.StudentFillDetailsAPIView.as_view(),name='StudentWriteDetails'),
# Student Detailed Average Timings
    url(r'student_averageTiming_detail/$',views.StudentAverageTimingDetailAPIView.as_view(),name='StudentAverageTimingDetailed'),
# Teacher Individual Analysis 
    url(r'teacher_analysis_showTests/$',views.TeacherAnalysisShowTestsAPIView.as_view(),name='TeacherAnalysisShowTests'),
# Teacher Individual Send Students 
    url(r'teacher_analysis_sendStudents/$',views.TeacherAnalysisIndividualSendStudentAPIView.as_view(),name='TeacherAnalysisIndividualSendStudent'),
# Teacher Individual Student Test Analysis 
    url(r'teacher_analysis_student_analysis/$',views.TeacherAnalysisIndividualStudentAPIView.as_view(),name='TeacherAnalysisIndividualStudentFinal'),
# Student Time Table 
    url(r'student_timetables/$',views.StudentShowTimeTableAPIView.as_view(),name='StudentTimeTables'),
# Student My performance Subjects 
    url(r'student_performance_1/$',views.StudentShowPerformanceSubjectsAPIView.as_view(),name='StudentMyPerformanceSubjects'),
# Student My performance Tests 
    url(r'student_performance_2/$',views.StudentShowPerformanceTestsAPIView.as_view(),name='StudentMyPerformanceTests'),
# Teacher edit batch of studnet 
    url(r'edit_batch/$',views.TeacherEditBatches.as_view(),name='TeacherEditBatches'),
# Student Accuracy Brief 
    url(r'student_weak_accuracy_brief/$',views.StudentAccuracyBriefAPIView.as_view(),name='StudentAccuracyBrief'),
# Student Accuracy Detailed 
    url(r'student_weak_accuracy_detail/$',views.StudentAccuracyDetailAPIView.as_view(),name='StudentAccuracyBrief'),
# Teacher batch change send batches 
    url(r'teacher_edit_batch_2/$',views.TeacherEditBatchesSendBatch.as_view(),name='TeacherEditBatch2'),
# Teacher batch change final 
    url(r'teacher_edit_batch_final/$',views.TeacherEditBatchesFinal.as_view(),name='TeacherEditBatchFinal'),
# Teacher create batch 
    url(r'teacher_create_batch1/$',views.CreateBatchAPIView.as_view(),name='TeacherCreateBatch'),
# Teacher create batch  final
    url(r'teacher_create_batch_final/$',views.CreateBatchFinalAPIView.as_view(),name='TeacherCreateBatchFinal'),
# Check Android Version 
    url(r'android_version/$',views.checkAndroidUpdateAPIView.as_view(),name='CheckAndroidUpdate'),
# Delete Bad Tests
    url(r'delete_bad_tests/$',views.DeleteBadTestsAPIView.as_view(),name='DeleteBadTests'),
# Check for user profile filled
    url(r'student_filled_profile/$',views.StudentFilledProfileAPIView.as_view(),name='StudentCheckProfile'),
# Students all subjects
    url(r'student_my_subjects/$',views.StudentSubjectsAPIView.as_view(),name='StudentSubjects'),
# Students average chapterwise timing detail
    url(r'student_chapter_timing/$',views.StudentAverageTimingChapterWiseAPIView.as_view(),name='StudentAverageChapterwiseTiming'),
# Teacher see student profile
    url(r'teacher_studentProfile_detail/$',views.TeacherStudentProfileDetailAPIView.as_view(),name='TeacherStudentProfileDetail'),
# Student Weak Area Subjectwise
    url(r'student_subject_weakAreas/$',views.StudentAllWeakAreasAPIView.as_view(),name='StudentSubjectWeakAreas'),
# Student Progress brief
    url(r'student_progress_brief/$',views.StudentProgressBriefAPIView.as_view(),name='StudentProgressBrief'),
# Student Progress chapterwise detail
    url(r'student_progress_detail/$',views.StudentProgressChapterDetailAPIView.as_view(),name='StudentProgressDetail'),
# Student Progress  detail
    url(r'student_progress_subject/$',views.StudentProgressDetailAPIView.as_view(),name='StudentProgressSubject'),
# Teacher Add question
    url(r'teacher_add_question/$',views.TeacherAddQuestionImageAPIView.as_view(),name='TeacherAddQuestions'),
# Teacher Add text question
    url(r'teacher_add_question_text/$',views.TeacherUploadTextQuestionAPIView.as_view(),name='TeacherAddQuestionText'),
# Get username of user
    url(r'get_username/$',views.get_username.as_view(),name='GetUsername'),
# Preferred Language set
    url(r'preffered_language/$',views.SetPrefferedLanguage.as_view(),name='SetPrefferedLanguage'),
# Edit batch search
    url(r'edit_batch_search/$',views.TeacherEditBatchSearch.as_view(),name='EditBatchSearch'),
# Student Current Batch
    url(r'student_current_batch/$',views.StudentCurrentBatchAPIView.as_view(),name='StudentCurrentBatch'),
# Student track activity
    url(r'student_track_activity/$',views.StudentTrackActivityAPIView.as_view(),name='StudentTrackActivity'),
# Student bookmark question
    url(r'student_bookmark_question/$',views.StudentBookmarkQuestionAPIView.as_view(),name='StudentBookmarkQuestion'),
# Student show bookmarked question
    url(r'student_show_bookmarked_questions/$',views.ShowBookMarksQuestionsAPIView.as_view(),name='ShowBookmarkedQuestion'),
# Student quiz game
    url(r'student_get_quiz_question/$',views.QuizGameAPIView.as_view(),name='StudentQuizGame'),
# Student language
    url(r'student_set_language/$',views.StudentLanguage.as_view(),name='StudentSetLanguage'),
# Student home page subjects
    url(r'home_page_subjects/$',views.HomePageSubjects.as_view(),name='HomePageSubjects'),
# Student change details with language and course (react native and s3 url of
# photo
    url(r'student_change_details/$',views.ChangeStudentDetails.as_view(),name='ChangeStudentDetails'),
# Student get test ranking table
    url(r'test_ranking_table/$',views.getTestRank.as_view(),name='GetStudentTestRank'),
# print test ranks
    url(r'print_testRank/$',views.printTestRank.as_view(),name='testrankPrint'),
# student subject ranks
    url(r'subject_ranking_table/$',views.getSubjectRank.as_view(),name='getSubjectRank'),
# get taken tests ids (student)
    url(r'taken_test_ids/$',views.getTakenTestsIds.as_view(),name='getTakenTestIds'),
# get subject logo
    url(r'subject_logo/$',views.getSubjectLogo.as_view(),name='getSubjectLogo'),
# student chapter ranks
    url(r'chapter_ranking_table/$',views.getChapterRank.as_view(),name='getChapterRank'),
# student see rank details
    url(r'subject_rank_details/$',views.getStudentSubjectRankDetails.as_view(),name='getStudentSubjectRankDetails'),
# student delete profile picture
    url(r'delete_profile_picture/$',views.deleteProfilePicture.as_view(),name='deleteProfilePicture'),
# student all subject rank detail
    url(r'all_rank_details/$',views.getStudentSubjectAllRankDetails.as_view(),name='SubjectRankDetailsAll'),
# teacher test analysis
    url(r'teacher_test_analysis_detail/$',views.TeacherTestAnalysisAPIView.as_view(),name='TeacherTestAnalysis'),
# subject group details
    url(r'subjectwise_group_details/$',views.getSubjectWiseGroupRank.as_view(),name='SubjectwiseGroupRank'),
# rate the test
    url(r'student_rate_test/$',views.RateTestAPIView.as_view(),name='StudentRateTest'),
# get overall rating of test
    url(r'overall_rating_test/$',views.GetTestOverallRating.as_view(),name='TestOverallRating'),
# save or retrieve expo token
    url(r'save_expo_token/$',views.saveExpoToken.as_view(),name='saveExpoToken'),
# get next exam date
    url(r'get_next_examDate/$',views.GetNextExamDate.as_view(),name='getNextExamDate'),
# expo notification
    url(r'send_expo_notification_api/$',views.expoNotification.as_view(),name='sendExpoNotification'),
# teacher go live url 
    url(r'get_teacher_live_url/$',views.TeacherGoLiveAPI.as_view(),name='goLiveAPI'),
# student challenge 
    url(r'challenge_student/$',views.ChallengeStudent.as_view(),name='challengeStudent'),
# see student challenges 
    url(r'see_my_challenges/$',views.GetChallengedStudents.as_view(),name='seeMyChallenges'),
# test performance new 
    url(r'new_test_performance/$',views.StudentTestPerformanceNew.as_view(),name='detailedTestPerformance'),
# get PromoCode
    url(r'get_promo_code/$',views.GetPromoCode.as_view(),name='GetPromoCode'),
# send expo notification testing
    url(r'send_expo_notification2/$',views.expoNotification2.as_view(),name='testExpoNotification'),
# challenge subject rank
    url(r'challenge_get_subjectrank/$',views.ChallengeSubjectRank.as_view(),name='challengeSubjectRank'),
# home page subject rank
    url(r'get_home_page_subjectRank/$',views.getHomePageSubjectRank.as_view(),name='homePageSubjectRank'),
# get subject rank paginated
    url(r'get_subject_ranking_paginated/$',views.getSubjectRankPaginated.as_view(),name='subjectRankPaginated'),
# get chapter rank paginated
    url(r'get_chapter_ranking_paginated/$',views.getChapterRankPaginated.as_view(),name='chapterRankPaginated'),
# get chapter rank paginated
    url(r'get_test_ranking_paginated/$',views.getTestRankPaginated.as_view(),name='testRankPaginated'),
# change course
    url(r'change_course/$',views.changeCourse.as_view(),name='changeCourseAPI'),
# get user data before downloading
    url(r'user_data_before_download/$',views.userBeforeDownloadingData.as_view(),name='getUserDataBeforeDownload'),
# teacher upload content
#    url(r'teacher_upload_content/$',views.teacheruploadimage.as_view(),name='teacherUploadContent'),
















]
