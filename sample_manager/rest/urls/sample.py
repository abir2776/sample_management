from django.urls import path

from sample_manager.rest.views.sample import (
    PublicSampleListView,
    PublicSampleSearchDetailView,
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
    path("", SampleListView.as_view(), name="sample-serach-list"),
    path("public", PublicSampleListView.as_view(), name="public-sample-list"),
    path(
        "public/<uuid:uid>",
        PublicSampleSearchDetailView.as_view(),
        name="public-sample-detail",
    ),
    path(
        "search/<uuid:uid>",
        SampleSearchDetailView.as_view(),
        name="sample-serch-details",
    ),
    path("upload", SampleUploadView.as_view(), name="sample-upload"),
]
