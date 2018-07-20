from django.shortcuts import render
# Create your views here.
from django.views.generic.base import View

from users.forms import RegisterForm


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
