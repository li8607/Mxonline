from django.urls import path

from courses.views import CourseListView

app_name = "courses"

urlpatterns = [
    path('list/', CourseListView.as_view(), name='list')
]
