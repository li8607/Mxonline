from django.contrib import admin
from .models import Course, Lesson, Video, CourseResource

# Register your models here.
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Video)
admin.site.register(CourseResource)