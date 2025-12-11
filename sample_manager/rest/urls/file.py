from django.urls import path

from sample_manager.rest.views.file import (
    FileHistoryListView,
    StorageFileDetailView,
    StorageFileListCreateView,
    StorageFileSearchListView,
    StorageFileSearchDetailView,
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
    path(
        "",
        StorageFileSearchListView.as_view(),
        name="storage-file-search-list",
    ),
    path(
        "<uuid:uid>",
        StorageFileSearchDetailView.as_view(),
        name="storage-file-search-details",
    ),
    path("<uuid:uid>/history/", FileHistoryListView.as_view(), name="file-history"),
]
