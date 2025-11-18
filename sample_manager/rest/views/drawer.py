from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from common.choices import Status
from sample_manager.models import Drawer
from sample_manager.permissions import (
    IsAdmin,
    IsManager,
    IsMerchandiser,
    IsOwner,
)
from sample_manager.rest.serializers.drawer import DrawerSerializer


class DrawerListCreateView(ListCreateAPIView):
    serializer_class = DrawerSerializer

    def get_queryset(self):
        bucket_uid = self.kwargs.get("bucket_uid")
        organization = self.request.user.get_organization()
        return Drawer.objects.filter(organization=organization, bucket__uid=bucket_uid)

    def get_permissions(self):
        method = self.request.method

        if method == "GET":
            return [IsAuthenticated()]

        if method == "POST":
            return [IsOwner() | IsAdmin() | IsManager() | IsMerchandiser()]

        return [IsAuthenticated()]


class DrawerDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = DrawerSerializer
    lookup_field = "uid"

    def get_permissions(self):
        method = self.request.method

        if method == "GET":
            return [IsAuthenticated()]

        if method in ["PUT", "PATCH"]:
            return [IsOwner() | IsAdmin() | IsManager() | IsMerchandiser()]

        if method == "DELETE":
            return [IsOwner() | IsAdmin()]

        return [IsAuthenticated()]

    def get_queryset(self):
        bucket_uid = self.kwargs.get("bucket_uid")
        organization = self.request.user.get_organization()
        return Drawer.objects.filter(organization=organization, bucket__uid=bucket_uid)

    def delete(self, request, *args, **kwargs):
        drawer = self.get_object()
        drawer.status = Status.REMOVED
        drawer.save()
        return Response(
            {"detail": "Drawer deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )
