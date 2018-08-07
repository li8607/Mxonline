from django.urls import path, re_path

from users.views import RegisterView, LoginView, LogoutView, UserInfoView, UpdateEmailView, SendEmailCodeView, UpdatePwdView, ForgetPwdView, ModifyPwdView, MyCourseView

app_name = "users"
urlpatterns = [
    path('info/', UserInfoView.as_view(), name='user_info'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('info/', UserInfoView.as_view(), name="user_info"),
    path('update_email/', UpdateEmailView.as_view(), name="update_email"),
    path('sendemail_code/', SendEmailCodeView.as_view(), name="sendemail_code"),
    path('update/pwd/', UpdatePwdView.as_view(), name="update_pwd"),
    path('forget_pwd/', ForgetPwdView.as_view(), name="forget_pwd"),
    path('modify_pwd/', ModifyPwdView.as_view(), name="modify_pwd"),
    path('mycourse/', MyCourseView.as_view(), name="mycourse"),

]
