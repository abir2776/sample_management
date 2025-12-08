from django.urls import path

from sample_manager.rest.views.note import (
    NoteDetailView,
    NoteHistoryListView,
    NoteListCreateView,
)

urlpatterns = [
    path("", NoteListCreateView.as_view(), name="note-list-create"),
    path("<uuid:uid>", NoteDetailView.as_view(), name="note-details"),
    path("<uuid:uid>/history/", NoteHistoryListView.as_view(), name="note-history"),
]
