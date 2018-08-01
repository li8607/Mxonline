from django.shortcuts import render
# Create your views here.
from django.views.generic.base import View

from courses.models import Course


class CourseListView(View):

    def get(self, request):
        all_course = Course.objects.all()
        sort = request.GET.get("sort", "")
        hot_course = all_course.order_by("-click_nums")[:5]
        if sort and sort == "hot":
            all_course = all_course.order_by("-click_nums")
        elif sort and sort == "students":
            all_course = all_course.order_by("-students")
        else:
            all_course = all_course.order_by("-add_time")

        return render(request, 'course-list.html', {
            "all_course": all_course,
            "sort": sort,
            "hot_course": hot_course,
        })
