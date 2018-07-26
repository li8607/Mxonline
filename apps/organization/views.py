from django.shortcuts import render
# Create your views here.
from django.views.generic.base import View

from .models import CityDict, CourseOrg


class OrgView(View):

    def get(self, request):
        all_city = CityDict.objects.all()
        all_orgs = CourseOrg.objects.all()

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
        return render(request, 'org-list.html', {
            "all_orgs": all_orgs,
            "all_city": all_city,
            "org_nums": org_nums,
            "city_id": city_id,
            "category": category,
            "sort": sort,
        })
