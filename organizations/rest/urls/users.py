from django.urls import path

from organizations.rest.views.users import (
    OrganizationUserDetailsView,
    OrganizationUserListCreateView,
)

urlpatterns = [
    path("", OrganizationUserListCreateView.as_view(), name="organization-users"),
    path(
        "<uuid:uid>",
        OrganizationUserDetailsView.as_view(),
        name="organization-user-details",
    ),
]
