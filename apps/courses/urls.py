from django.urls import path, re_path

from courses.views import CourseListView, CourseDetailView, CourseInfoView, CourseCommentView, VideoPlayView, \
    AddComments

app_name = "courses"

urlpatterns = [
    path('list/', CourseListView.as_view(), name='list'),
    re_path('detail/(?P<course_id>\d+)/', CourseDetailView.as_view(), name="course_detail"),
    re_path('info/(?P<course_id>\d+)/', CourseInfoView.as_view(), name="course_info"),
    re_path('comments/(?P<course_id>\d+)/', CourseCommentView.as_view(), name="course_comments"),
    re_path('video/(?P<video_id>\d+)/', VideoPlayView.as_view(), name="video_play"),
    path('add_comment/', AddComments.as_view(), name="add_comment")
]
