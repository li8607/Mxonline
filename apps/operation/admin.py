from django.contrib import admin

from .models import UserAsk, UserCourse

# Register your models here.
admin.site.register(UserAsk)
admin.site.register(UserCourse)
