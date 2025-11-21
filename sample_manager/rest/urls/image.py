from django.urls import path

from sample_manager.rest.views.image import ImageDetailView, ImageListCreateView

urlpatterns = [
    path("", ImageListCreateView.as_view(), name="image-list-create"),
    path(
        "<uuid:uid>",
        ImageDetailView.as_view(),
        name="image-details",
    ),
]
