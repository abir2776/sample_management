from django.urls import path

from core.rest.views.users import UserProfileView

urlpatterns = [
    path("", UserProfileView.as_view(), name="user-profile"),
]
