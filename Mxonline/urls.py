"""Mxonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

from Mxonline.settings import MEDIA_ROOT
from users.views import IndexView, ActiveUserView, ResetPwdView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name="index"),
    path('users/', include('users.urls', namespace='users')),
    path('captcha/', include('captcha.urls')),
    re_path('active/(?P<active_code>.*)/', ActiveUserView.as_view(), name="user_active"),
    re_path('reset/(?P<active_code>.*)/', ResetPwdView.as_view(), name="reset_pwd"),
    path('org/', include('organization.urls', namespace='org')),
    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),
    path('courses/', include('courses.urls', namespace='courses')),
]
