from django.urls import path

from sample_manager.rest.views.storage import (
    StorageDetailView,
    StorageHistoryListView,
    StorageListCreateView,
)

urlpatterns = [
    path("", StorageListCreateView.as_view(), name="storage-list-create"),
    path("<uuid:uid>", StorageDetailView.as_view(), name="storage-detail"),
    path(
        "<uuid:uid>/history/",
        StorageHistoryListView.as_view(),
        name="storage-history",
    ),
]
