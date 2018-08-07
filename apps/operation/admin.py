from django.contrib import admin

from .models import UserAsk, UserCourse, CourseComments, UserFavorite

# Register your models here.
admin.site.register(UserAsk)
admin.site.register(UserCourse)
admin.site.register(CourseComments)
admin.site.register(UserFavorite)
