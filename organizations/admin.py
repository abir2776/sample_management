from django.contrib import admin

from .models import Company, UserCompany, ActivityLog

# Register your models here.
admin.site.register(Company)
admin.site.register(UserCompany)
admin.site.register(ActivityLog)
