from django.urls import path

from sample_manager.rest.views.sample import (
    SampleDetailView,
    SampleListCreateView,
    SampleListView,
    SampleSearchDetailView,
    SampleUploadView,
)

urlpatterns = [
    path(
        "<uuid:storage_uid>", SampleListCreateView.as_view(), name="sample-list-create"
    ),
    path(
        "<uuid:storage_uid>/<uuid:uid>",
        SampleDetailView.as_view(),
        name="sample-details",
    ),
    path("", SampleListView.as_view(), name="sample-list-create"),
    path(
        "search/<uuid:uid>",
        SampleSearchDetailView.as_view(),
        name="sample-details",
    ),
    path("upload", SampleUploadView.as_view(), name="sample-upload"),
]
