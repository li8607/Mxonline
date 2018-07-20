from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


class UserProfile(AbstractUser):
    GENDER_CHOICES = (
        ("male", "男"),
        ("female", "女")
    )

    nick_name = models.CharField(max_length=50, verbose_name=u"昵称", default="")
    birthday = models.DateField(verbose_name=u"生日", null=True, blank=True)
    gender = models.CharField(
        max_length=6,
        verbose_name=u"性别",
        choices=GENDER_CHOICES,
        default="female")
    address = models.CharField(max_length=100, verbose_name="地址", default="")
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name="电话")
    image = models.ImageField(upload_to="image/%Y/%m", default="image/default.png", max_length=100, verbose_name="头像")

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    SEND_CHOICES = (("register", "注册"), ("forget", "找回密码"), ("update_email", "修改邮箱"))
    code = models.CharField(max_length=20, verbose_name="验证码")
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    send_type = models.CharField(choices=SEND_CHOICES, max_length=20, verbose_name="验证码类型")
    send_time = models.DateTimeField(default=datetime.now, verbose_name="发送事件")

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)
