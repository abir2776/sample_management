from django.urls import include, path

urlpatterns = [
    path("bucket/", include("sample_manager.rest.urls.bucket")),
    path("sample/", include("sample_manager.rest.urls.sample")),
    path("drawer/", include("sample_manager.rest.urls.drawer")),
    path("buyer/", include("sample_manager.rest.urls.buyer")),
    path("files/", include("sample_manager.rest.urls.files")),
]
