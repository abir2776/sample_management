from django.urls import include, path

urlpatterns = [
    path("activity/", include("core.rest.urls.activitylog")),
    path("send_mail/", include("core.rest.urls.useremail")),
]
