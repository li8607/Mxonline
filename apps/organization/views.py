from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View


class OrgView(View):
    def get(self, request):
        return render(request, 'org-list.html')
