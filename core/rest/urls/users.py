from django.urls import path

from core.rest.views.users import UserDetailView, UserListCreateView, UserProfileView

urlpatterns = [
    path("", UserListCreateView.as_view(), name="user-list-create"),
    path("<uuid:uid>", UserDetailView.as_view(), name="user-details"),
    path("me", UserProfileView.as_view(), name="user-profile"),
]
