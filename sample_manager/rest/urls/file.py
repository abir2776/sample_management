from django.urls import path

from sample_manager.rest.views.file import (
    StorageFileDetailView,
    StorageFileListCreateView,
)

urlpatterns = [
    path(
        "<uuid:storage_uid>",
        StorageFileListCreateView.as_view(),
        name="storage-file-list-create",
    ),
    path(
        "<uuid:storage_uid>/<uuid:uid>",
        StorageFileDetailView.as_view(),
        name="storage-file-details",
    ),
]
