from captcha.fields import CaptchaField
from django import forms


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})


class ActiveForm(forms.Form):
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})
