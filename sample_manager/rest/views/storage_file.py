from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import OR, IsAuthenticated
from rest_framework.response import Response

from common.choices import Status
from sample_manager.models import StorageFile
from sample_manager.permissions import (
    IsAdmin,
    IsManager,
    IsMerchandiser,
    IsOwner,
)
from sample_manager.rest.serializers.storage_file import StorageFileSerializer


class StorageFileListCreateView(ListCreateAPIView):
    serializer_class = StorageFileSerializer

    def get_queryset(self):
        storage_uid = self.kwargs.get("storage_uid")
        organization = self.request.user.get_organization()
        return StorageFile.objects.filter(
            organization=organization, storage__uid=storage_uid
        )

    def get_permissions(self):
        method = self.request.method

        if method == "GET":
            return [IsAuthenticated()]

        if method == "POST":
            return [OR(IsOwner(), OR(IsAdmin(), OR(IsManager(), IsMerchandiser())))]

        return [IsAuthenticated()]


class StorageFileDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = StorageFileSerializer
    lookup_field = "uid"

    def get_permissions(self):
        method = self.request.method

        if method == "GET":
            return [IsAuthenticated()]

        if method in ["PUT", "PATCH"]:
            return [OR(IsOwner(), OR(IsAdmin(), OR(IsManager(), IsMerchandiser())))]

        if method == "DELETE":
            return [IsOwner() | IsAdmin()]

        return [IsAuthenticated()]

    def get_queryset(self):
        storage_uid = self.kwargs.get("storage_uid")
        organization = self.request.user.get_organization()
        return StorageFile.objects.filter(
            organization=organization, storage__uid=storage_uid
        )

    def delete(self, request, *args, **kwargs):
        storage_file = self.get_object()
        storage_file.status = Status.REMOVED
        storage_file.save()
        return Response(
            {"detail": "Drawer deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )
