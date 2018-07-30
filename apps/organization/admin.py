from django.contrib import admin

# Register your models here.
from .models import CourseOrg, CityDict, Teacher

admin.site.register(CityDict)
admin.site.register(CourseOrg)
admin.site.register(Teacher)
