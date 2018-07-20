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
