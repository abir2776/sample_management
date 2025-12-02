from django.urls import path

from organizations.rest.views.users import (
    AdminUserView,
    CompanyUserDetailsView,
    CompanyUserListCreateView,
)

urlpatterns = [
    path("", CompanyUserListCreateView.as_view(), name="company-users"),
    path("admin/user", AdminUserView.as_view(), name="all-users"),
    path(
        "<uuid:uid>",
        CompanyUserDetailsView.as_view(),
        name="company-user-details",
    ),
]
