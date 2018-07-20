from django.urls import path, re_path

from users.views import UserInfoView, RegisterView, LoginView, ActiveUserView

app_name = "users"
urlpatterns = [
    path('info/', UserInfoView.as_view(), name='user_info'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]
