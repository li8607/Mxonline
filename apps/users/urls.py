from django.urls import path

from users.views import RegisterView, LoginView, LogoutView, UserInfoView, UpdateEmailView, SendEmailCodeView, \
    UpdatePwdView, ForgetPwdView, ModifyPwdView, MyCourseView, MyFavOrgView \
    , MyFavTeacherView, MyFavCourseView, UserMessageView

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
    path('myfav/org/', MyFavOrgView.as_view(), name="myfav_org"),
    path('myfav/teacher/', MyFavTeacherView.as_view(), name="myfav_teacher"),
    path('myfav/course/', MyFavCourseView.as_view(), name="myfav_course"),
    path('message/', UserMessageView.as_view(), name="message"),

]
