from django.urls import include, path

urlpatterns = [
    path("users/", include("organizations.rest.urls.users")),
    path("my_organizations/", include("organizations.rest.urls.organizations")),
]
