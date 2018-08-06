from django.contrib import admin
from users.models import UserProfile, EmailVerifyRecord, Banner
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(EmailVerifyRecord)
admin.site.register(Banner)
