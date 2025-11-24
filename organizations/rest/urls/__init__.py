from django.urls import include, path

urlpatterns = [
    path("users/", include("organizations.rest.urls.users")),
    path("my_companys/", include("organizations.rest.urls.company")),
]
