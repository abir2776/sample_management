from django.urls import path

from organizations.rest.views.organizations import (
    MyOrganizationListCreate,
    SwitchOrganizationAPIView,
)

urlpatterns = [
    path("", MyOrganizationListCreate.as_view(), name="my-organization-list-create"),
    path("switch", SwitchOrganizationAPIView.as_view(), name="organization-switch"),
]
