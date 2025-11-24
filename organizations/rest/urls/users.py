from django.urls import path

from organizations.rest.views.users import (
    CompanyUserDetailsView,
    CompanyUserListCreateView,
)

urlpatterns = [
    path("", CompanyUserListCreateView.as_view(), name="company-users"),
    path(
        "<uuid:uid>",
        CompanyUserDetailsView.as_view(),
        name="company-user-details",
    ),
]
