from django.urls import path

from organization.views import OrgView

app_name = 'org'

urlpatterns = [
    path('list/', OrgView.as_view(), name='list')
]
