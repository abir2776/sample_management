from django.urls import path

from sample_manager.rest.views.drawer import DrawerDetailView, DrawerListCreateView

urlpatterns = [
    path(
        "<uuid:bucket_uid>", DrawerListCreateView.as_view(), name="drawer-list-create"
    ),
    path(
        "<uuid:bucket_uid>/<uuid:uid>",
        DrawerDetailView.as_view(),
        name="drawer-details",
    ),
]
