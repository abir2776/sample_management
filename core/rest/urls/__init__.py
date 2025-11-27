from django.urls import include, path

urlpatterns = [
    path("", include("core.rest.urls.users")),
    path("activity/", include("core.rest.urls.activitylog")),
]
