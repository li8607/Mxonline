# 生成随机字符串
from random import Random

from django.core.mail import EmailMessage

from Mxonline.settings import EMAIL_FROM
from users.models import EmailVerifyRecord


def random_str(random_length=8):
    str = ''
    # 生成字符串的可选字符串
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        str += chars[random.randint(0, length)]
    return str


def send_register_eamil(email, send_type="register"):
    email_record = EmailVerifyRecord()
    if send_type == 'update_email':
        code = random_str(4)
    else:
        code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()
    if send_type == 'register':
        email_title = "bencheng慕课小站 注册激活链接"
        email_body = "欢迎注册bencheng慕课小站:  请点击下面的链接激活你的账号: http://127.0.0.1:8000/active/{0}".format(code)
        msg = EmailMessage(email_title, email_body, EMAIL_FROM, [email])
        msg.send()
    elif send_type == 'update_email':
        email_title = "bencheng慕课小站 修改邮箱验证码"
        email_body = "您好,您的账号正在申请修改密码,下面是您的验证码，请注意查收:{}".format(code)
        msg = EmailMessage(email_title, email_body, EMAIL_FROM, [email])
        msg.send()
    elif send_type == 'forget':
        email_title = "bencheng慕课小站 找回密码链接"
        email_body = "您好,您的账号正在申请找回密码,请点击下面的链接找回你的账号密码: http://127.0.0.1:8000/reset/{0}".format(code)
        msg = EmailMessage(email_title, email_body, EMAIL_FROM, [email])
        msg.send()
