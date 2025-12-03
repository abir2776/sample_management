from django.urls import path

from sample_manager.rest.views.requests import (
    ModifyRequestListView,
    ModifyRequestRetrieveUpdateView,
)

urlpatterns = [
    path("", ModifyRequestListView.as_view(), name="modify-request-list"),
    path(
        "<str:uid>",
        ModifyRequestRetrieveUpdateView.as_view(),
        name="modify-request-detail",
    ),
]
