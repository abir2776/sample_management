from django.urls import path

from sample_manager.rest.views.buyer import BuyerDetailView, BuyerListCreateView

urlpatterns = [
    path("", BuyerListCreateView.as_view(), name="buyer-list-create"),
    path(
        "<uuid:uid>",
        BuyerDetailView.as_view(),
        name="buyer-details",
    ),
]
