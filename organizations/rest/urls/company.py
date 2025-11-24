from django.urls import path

from organizations.rest.views.company import (
    MyCompanyListCreate,
    SwitchCompanyAPIView,
    CompanyAddUserView,
)

urlpatterns = [
    path("", MyCompanyListCreate.as_view(), name="my-company-list-create"),
    path("switch", SwitchCompanyAPIView.as_view(), name="company-switch"),
    path("add_user", CompanyAddUserView.as_view(), name="company_add_user"),
]
