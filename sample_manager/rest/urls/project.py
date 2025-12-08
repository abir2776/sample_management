from django.urls import path

from sample_manager.rest.views.project import (
    ProjectDetailView,
    ProjectHistoryListView,
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
    path(
        "<uuid:uid>/history/", ProjectHistoryListView.as_view(), name="project-history"
    ),
]
