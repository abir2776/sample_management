from django.urls import path

from sample_manager.rest.views.files import FileDetailView, FileListCreateView

urlpatterns = [
    path("", FileListCreateView.as_view(), name="file-list-create"),
    path(
        "<uuid:uid>",
        FileDetailView.as_view(),
        name="file-details",
    ),
]
