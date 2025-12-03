from django.urls import include, path

urlpatterns = [
    path("storage/", include("sample_manager.rest.urls.storage")),
    path("sample/", include("sample_manager.rest.urls.sample")),
    path("storage_file/", include("sample_manager.rest.urls.file")),
    path("buyer/", include("sample_manager.rest.urls.buyer")),
    path("images/", include("sample_manager.rest.urls.image")),
    path("project/", include("sample_manager.rest.urls.project")),
    path("note/", include("sample_manager.rest.urls.note")),
    path("requests/", include("sample_manager.rest.urls.requests")),
]
