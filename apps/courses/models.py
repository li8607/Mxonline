from datetime import datetime

from django.db import models

# Create your models here.
from DjangoUeditor.models import UEditorField
from organization.models import CourseOrg, Teacher


class Course(models.Model):
    DEGREE_CHOICES = (
        ("cj", u"初级"),
        ("zj", u"中级"),
        ("gj", u"高级")
    )
    course_org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name="所属机构", null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="教师")
    name = models.CharField(max_length=50, verbose_name="课程名")
    desc = models.CharField(max_length=300, verbose_name="课程描述")
    detail = UEditorField(width=600, height=300, imagePath='courses/ueditor/', filePath='courses/ueditor/', default='',
                          verbose_name='课程详情')
    is_banner = models.BooleanField(default=False, verbose_name='是否轮播')
    degree = models.CharField(choices=DEGREE_CHOICES, max_length=2, verbose_name='难度')
    learn_times = models.IntegerField(default=0, verbose_name='学习时长(分钟数)')
    students = models.IntegerField(default=0, verbose_name="学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏人数")
    you_need_know = models.CharField(max_length=300, default='一颗勤学的心是本课程必要前提', verbose_name="课程须知")
    teacher_tell = models.CharField(max_length=300, default="什么都可以学到,按时交作业,不然叫家长", verbose_name="老师告诉你")
    image = models.ImageField(upload_to="courses/%Y/%m",
                              verbose_name="封面图",
                              max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    category = models.CharField(max_length=20, verbose_name="课程类别", default='后端开发')
    tag = models.CharField(max_length=15, verbose_name="课程标签", default="")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    name = models.CharField(max_length=100, verbose_name="章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '《{0}》课程的章节 >> {1}'.format(self.course, self.name)


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="章节")
    url = models.CharField(max_length=200, default="http://www.bencheng.xyz", verbose_name="访问地址")
    name = models.CharField(max_length=100, verbose_name="视频名")
    learn_time = models.IntegerField(default=0, verbose_name="学习时长(分钟)")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}章节的视频 >> {1}'.format(self.lesson, self.name)


class CourseResource(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    name = models.CharField(max_length=100, verbose_name="名称")
    download = models.FileField(
        upload_to="course/resource/%Y/%m",
        verbose_name="资源文件",
        max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '《{0}》课程的资源: {1}'.format(self.course, self.name)
