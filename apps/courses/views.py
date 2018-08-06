from django.http import HttpResponseRedirect
from django.shortcuts import render
# Create your views here.
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger

from courses.models import Course, Video, CourseResource
from operation.models import UserCourse


class CourseListView(View):

    def get(self, request):
        all_course = Course.objects.all()
        sort = request.GET.get("sort", "")
        hot_course = all_course.order_by("-students")[:3]
        if sort and sort == "hot":
            all_course = all_course.order_by("-click_nums")
        elif sort and sort == "students":
            all_course = all_course.order_by("-students")

        try:
            page = request.GET.get("page", 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_course, 6, request=request)
        courses = p.page(page)
        return render(request, 'course-list.html', {
            "all_course": courses,
            "sort": sort,
            "hot_course": hot_course,
        })


class CourseDetailView(View):

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        tag = course.tag
        if tag:
            course_tag = Course.objects.filter(tag=tag)[1:2]
        else:
            course_tag = []
        return render(request, "course-detail.html ", {
            "course": course,
            "course_tag": course_tag
        })


class CourseInfoView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        return render(request, "course-video.html", {
            "course_id": course_id,
            "course": course
        })


class CourseCommentView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        return render(request, "course-comment.html")


class VideoPlayView(View):
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        return HttpResponseRedirect(video.url)
