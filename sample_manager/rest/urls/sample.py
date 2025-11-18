from django.urls import path

from sample_manager.rest.views.sample import SampleDetailView, SampleListCreateView

urlpatterns = [
    path(
        "<uuid:bucket_uid>", SampleListCreateView.as_view(), name="sample-list-create"
    ),
    path(
        "<uuid:bucket_uid>/<uuid:uid>",
        SampleDetailView.as_view(),
        name="sample-details",
    ),
]
