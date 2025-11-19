from django.urls import path

from sample_manager.rest.views.storage import (
    StorageDetailView,
    StorageListCreateView,
)

urlpatterns = [
    path("", StorageListCreateView.as_view(), name="storage-list-create"),
    path("<uuid:uid>", StorageDetailView.as_view(), name="storage-detail"),
]
