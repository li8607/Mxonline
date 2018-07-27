from django.urls import path

from organization.views import OrgView, AddUserAskView

app_name = 'org'

urlpatterns = [
    path('list/', OrgView.as_view(), name='list'),
    path('add_ask/', AddUserAskView.as_view(), name='add_ask')
]
