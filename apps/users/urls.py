from django.urls import path, re_path

from users.views import RegisterView, LoginView, LogoutView, UserInfoView, UpdateEmailView, SendEmailCodeView, UpdatePwdView

app_name = "users"
urlpatterns = [
    path('info/', UserInfoView.as_view(), name='user_info'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('info/', UserInfoView.as_view(), name="user_info"),
    re_path('update_email/', UpdateEmailView.as_view(), name="update_email"),
    re_path('sendemail_code/', SendEmailCodeView.as_view(), name="sendemail_code"),
    re_path('update/pwd/', UpdatePwdView.as_view(), name="update_pwd"),

]
