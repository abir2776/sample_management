from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import OR, IsAuthenticated
from rest_framework.response import Response

from common.choices import Status
from sample_manager.choices import StorageType
from sample_manager.models import File, Storage
from sample_manager.permissions import (
    IsAdministrator,
    IsSuperAdmin,
)
from sample_manager.rest.serializers.file import StorageFileSerializer


class StorageFileListCreateView(ListCreateAPIView):
    serializer_class = StorageFileSerializer

    def get_queryset(self):
        storage_uid = self.kwargs.get("storage_uid")
        storage = Storage.objects.filter(
            uid=storage_uid, type=StorageType.DRAWER
        ).first()
        if not storage:
            raise APIException("Invalid storage uid provided")
        company = self.request.user.get_company()
        return File.objects.filter(
            company=company,
            storage=storage,
            is_active=True,
        )

    def get_permissions(self):
        method = self.request.method

        if method == "GET":
            return [IsAuthenticated()]

        if method == "POST":
            return [IsAuthenticated()]

        return [IsAuthenticated()]


class StorageFileDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = StorageFileSerializer
    lookup_field = "uid"

    def get_permissions(self):
        method = self.request.method

        if method == "GET":
            return [IsAuthenticated()]

        if method in ["PUT", "PATCH"]:
            return [IsAuthenticated()]

        if method == "DELETE":
            return [OR(IsSuperAdmin, IsAdministrator())]

        return [IsAuthenticated()]

    def get_queryset(self):
        storage_uid = self.kwargs.get("storage_uid")
        storage = Storage.objects.filter(
            uid=storage_uid, type=StorageType.DRAWER
        ).first()
        if not storage:
            raise APIException("Invalid storage uid provided")
        company = self.request.user.get_company()
        return File.objects.filter(
            company=company,
            storag=storage,
            is_active=True,
        )

    def delete(self, request, *args, **kwargs):
        file = self.get_object()
        file.status = Status.REMOVED
        file.save()
        return Response(
            {"detail": "File deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )
