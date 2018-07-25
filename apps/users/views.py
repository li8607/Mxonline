import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
# Create your views here.
from django.views.generic.base import View

from users.forms import RegisterForm, ActiveForm, LoginForm, UserInfoForm, ModifyPwdForm, ForgetForm
from users.models import UserProfile, EmailVerifyRecord
from utils.email_send import send_register_eamil


class IndexView(View):

    def get(self, request):
        return render(request, 'index.html')


class RegisterView(View):

    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {
            'register_form': register_form
        })

    def post(self, request):
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            email = request.POST.get('email', '')
            if UserProfile.objects.filter(email=email):
                return render(request, "register.html", {
                    "register_form": register_form,
                    "msg": "用户已存在"
                })

            pass_word = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.email = email
            user_profile.username = email

            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()

            send_register_eamil(email, "register")

            return render(request, "login.html")
        else:
            return render(request, "register.html", {
                "register_form": register_form
            })


class CustomBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")

            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html', {
                        "msg": "用户名未激活! 请前往邮箱进行激活"
                    })
            else:
                return render(request, 'login.html', {
                    "msg": "用户名或密码错误!"
                })
        else:
            return render(request, 'login.html', {
                "login_form": login_form
            })


class ActiveUserView(View):

    def get(self, request, active_code):
        active_form = ActiveForm(request.GET)
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()

            return render(request, 'login.html')
        else:
            return render(request, "register.html", {
                "msg": "您的激活链接无效",
                "active_form": active_form
            })


class LogoutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class UserInfoView(View):

    def get(self, request):
        return render(request, 'usercenter-info.html')

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse(
                '{"status:success"}',
                content_type='application/json'
            )
        else:
            return HttpResponse(
                json.dumps(user_info_form.errors),
                content_type='application/json'
            )


class UpdateEmailView(LoginRequiredMixin, View):

    def post(self, request):
        email = request.POST.get('email', "")
        code = request.POST.get('code', "")
        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code)
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse(
                '{"status":"success"}',
                content_type='application/json')
        else:
            return HttpResponse(
                '{"email":"验证码无效"}',
                content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    def get(self, request):
        email = request.GET.get('email', '')

        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email": "邮箱已经存在"}', content_type='application/json')

        send_register_eamil(email, 'update_email')
        return HttpResponse('{"status": "success"}', content_type='application/json')


class UpdatePwdView(LoginRequiredMixin, View):

    def post(self, request):
        modify_pwd_form = ModifyPwdForm(request.POST)
        if modify_pwd_form.is_valid():
            pwd = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')

            if pwd != pwd2:
                return HttpResponse(
                    '{"status":"fail", "msg":"密码不一致"}',
                    content_type='application/json')
            else:
                user = request.user
                user.password = make_password(pwd)
                user.save()
                return HttpResponse(
                    '{"status":"success"}',
                    content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_pwd_form.errors), content_type='application/json')


class ForgetPwdView(View):

    def get(self, request):
        active_form = ActiveForm(request.POST)
        return render(request, "forgetpwd.html", {'active_form': active_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            send_register_eamil(email, "forget")
            return render(request, 'login.html', {"msg": "重置密码邮件已发送,请注意查收"})
        else:
            return render(request, 'forgetpwd.html', {"forget_from": forget_form})


class ResetPwdView(View):

    def get(self, request, active_code):
        evr = EmailVerifyRecord.objects.get(code=active_code)
        active_form = ActiveForm(request.GET)
        if evr:
            email = evr.email
            return render(request, 'password_reset.html', {
                "email": email
            })
        else:
            return render(request, 'forgetpwd.html', {
                "msg": "您的重置密码链接无效,请重新请求", "active_form": active_form
            })


class ModifyPwdView(View):

    def post(self, request):
        modify_pwd_form = ModifyPwdForm(request.POST)
        if modify_pwd_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {
                    "msg": "密码不一致"
                })

            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return render(request, 'login.html', {
                "msg": "密码修改成功，请登录"
            })
        else:
            return render(request, 'password_reset.html')
