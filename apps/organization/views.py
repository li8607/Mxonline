from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger

from courses.models import Course
from operation.models import UserFavorite
from organization.forms import UserAskForm
from .models import CityDict, CourseOrg, Teacher


class OrgView(View):

    def get(self, request):
        all_city = CityDict.objects.all()
        all_orgs = CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by("-click_nums")[:3]
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        sort = request.GET.get('sort', '')
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")

        org_nums = all_orgs.count()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 4, request=request)
        orgs = p.page(page)

        return render(request, 'org-list.html', {
            "all_orgs": orgs,
            "all_city": all_city,
            "org_nums": org_nums,
            "city_id": city_id,
            "category": category,
            "sort": sort,
            "hot_orgs": hot_orgs,
        })


class AddUserAskView(View):

    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"您的字段有错误,请检查"}', content_type='application/json')


class OrgHomeView(View):

    def get(self, request, org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        all_courses = course_org.course_set.all()[:4]
        all_teacher = course_org.teacher_set.all()[:3]

        has_org_fav = False
        if request.user.is_authenticated:
            user_fav = UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2)
            if user_fav:
                has_org_fav = True

        return render(request, 'org-detail-homepage.html', {
            "all_courses": all_courses,
            "all_teacher": all_teacher,
            "course_org": course_org,
            "current_page": current_page,
            "has_org_fav": has_org_fav,
        })


class OrgCourseView(View):

    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()
        return render(request, 'org-detail-course.html', {
            "all_courses": all_courses,
            "course_org": course_org,
            "current_page": current_page
        })


class OrgDescView(View):

    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        return render(request, 'org-detail-desc.html', {
            "course_org": course_org,
            "current_page": current_page
        })


class OrgTeacherView(View):

    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teacher = course_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html', {
            "course_org": course_org,
            "current_page": current_page,
            "all_teacher": all_teacher
        })


class TeacherListView(View):

    def get(self, request):
        all_teacher = Teacher.objects.all()
        sort = request.GET.get("sort", "")
        if sort and sort == "hot":
            all_teacher = all_teacher.order_by("-click_nums")

        rank_teacher = all_teacher.order_by("-fav_nums")[:5]
        teacher_nums = all_teacher.count()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teacher, 4, request=request)
        teachers = p.page(page)

        return render(request, 'teachers-list.html', {
            "all_teacher": teachers,
            "teacher_nums": teacher_nums,
            "sort": sort,
            "rank_teacher": rank_teacher
        })


class OrgTeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums += 1
        teacher.save()
        rank_teacher = Teacher.objects.all().order_by("-fav_nums")[:5]
        all_course = teacher.course_set.all()

        has_teacher_fav = False
        has_org_fav = False
        if request.user.is_authenticated:
            user_fav = UserFavorite.objects.filter(user=request.user, fav_id=teacher.id, fav_type=3)
            if user_fav:
                has_teacher_fav = True

            user_org_fav = UserFavorite.objects.filter(user=request.user, fav_id=teacher.org.id, fav_type=2)
            if user_org_fav:
                has_org_fav = True

        return render(request, 'teacher-detail.html', {
            "teacher": teacher,
            "rank_teacher": rank_teacher,
            "all_course": all_course,
            "has_teacher_fav": has_teacher_fav,
            "has_org_fav": has_org_fav,
        })


class AddFavView(View):
    def post(self, request):
        id = request.POST.get('fav_id', 0)
        type = request.POST.get('fav_type', 0)

        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(id), fav_type=int(type))
        if exist_records:
            exist_records.delete()
            if int(type) == 1:
                course = Course.objects.get(id=int(id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif int(type) == 2:
                org = CourseOrg.objects.get(id=int(id))
                org.fav_nums -= 1
                if org.fav_nums < 0:
                    org.fav_nums = 0
                org.save()
            else:
                teacher = Teacher.objects.get(id=int(id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(type) > 0 and int(id) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(id)
                user_fav.fav_type = int(type)
                user_fav.save()

                if int(type) == 1:
                    course = Course.objects.get(id=int(id))
                    course.fav_nums += 1
                    course.save()
                elif int(type) == 2:
                    org = CourseOrg.objects.get(id=int(id))
                    org.fav_nums += 1
                    org.save()
                else:
                    teacher = Teacher.objects.get(id=int(id))
                    teacher.fav_nums += 1
                    teacher.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')
