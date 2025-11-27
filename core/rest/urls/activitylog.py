from django.urls import path

from core.rest.views.activitylog import ActivityLogListCreateView

urlpatterns = [path("", ActivityLogListCreateView.as_view(), name="user-acitivity")]
