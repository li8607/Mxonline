from django.contrib import admin

# Register your models here.
from .models import CourseOrg,CityDict
admin.site.register(CityDict)
admin.site.register(CourseOrg)