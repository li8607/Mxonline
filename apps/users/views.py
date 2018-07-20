from django.contrib.auth.hashers import make_password
from django.shortcuts import render
# Create your views here.
from django.views.generic.base import View

from users.forms import RegisterForm, ActiveForm
from users.models import UserProfile, EmailVerifyRecord
from utils.email_send import send_register_eamil


class IndexView(View):

    def get(self, request):
        return render(request, 'index.html')


class UserInfoView(View):

    def get(self, request):
        return render(request, 'usercenter-info.html')


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


class LoginView(View):

    def get(self, request):
        return render(request, 'login.html')


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
                "msg":"您的激活链接无效",
                "active_form": active_form
            })


