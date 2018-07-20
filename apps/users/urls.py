from django.urls import path

from users.views import UserInfoView,RegisterView

app_name = "users"
urlpatterns = [
    path('info/', UserInfoView.as_view(), name='user_info'),
    path('register/', RegisterView.as_view(), name='register')

]
