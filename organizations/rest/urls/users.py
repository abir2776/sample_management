from django.urls import path

from organizations.rest.views.users import (
    AdminUserDetailView,
    AdminUserView,
    CompanyUserDetailsView,
    CompanyUserListCreateView,
)

urlpatterns = [
    path("", CompanyUserListCreateView.as_view(), name="company-users"),
    path("admin/user", AdminUserView.as_view(), name="all-users"),
    path(
        "admin/user/<int:id>",
        AdminUserDetailView.as_view(),
        name="admin-user-details",
    ),
    path(
        "<uuid:uid>",
        CompanyUserDetailsView.as_view(),
        name="company-user-details",
    ),
]
