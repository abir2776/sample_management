from django.urls import path
from sample_manager.rest.views.note import NoteListCreateView, NoteDetailView

urlpatterns = [
    path("", NoteListCreateView.as_view(), name="note-list-create"),
    path("<uuid:uid>", NoteDetailView.as_view(), name="note-details"),
]
