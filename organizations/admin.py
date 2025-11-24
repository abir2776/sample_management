from django.contrib import admin

from .models import (
    Company,
    UserCompany,
)

# Register your models here.
admin.site.register(Company)
admin.site.register(UserCompany)
