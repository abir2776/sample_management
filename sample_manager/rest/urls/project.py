from django.urls import path

from sample_manager.rest.views.project import (
    ProjectDetailView,
    ProjectListCreateView,
)

urlpatterns = [
    path(
        "",
        ProjectListCreateView.as_view(),
        name="project-list-create",
    ),
    path(
        "<uuid:uid>",
        ProjectDetailView.as_view(),
        name="project-details",
    ),
]
