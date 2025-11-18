from django.urls import path

from sample_manager.rest.views.bucket import (
    BucketListCreateView,
    BucketDetailView,
)

urlpatterns = [
    path("", BucketListCreateView.as_view(), name="sample-bucket-list-create"),
    path("<uuid:uid>", BucketDetailView.as_view(), name="sample-bucket-detail"),
]
