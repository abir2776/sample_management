from django.urls import path

from sample_manager.rest.views.buyer import (
    BuyerDetailView,
    BuyerHistoryListView,
    BuyerListCreateView,
)

urlpatterns = [
    path("", BuyerListCreateView.as_view(), name="buyer-list-create"),
    path(
        "<uuid:uid>",
        BuyerDetailView.as_view(),
        name="buyer-details",
    ),
    path("<uuid:uid>/history/", BuyerHistoryListView.as_view(), name="buyer-history"),
]
