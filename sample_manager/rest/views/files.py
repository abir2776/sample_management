from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import OR, IsAuthenticated
from rest_framework.response import Response

from common.choices import Status
from sample_manager.models import File
from sample_manager.permissions import (
    IsAdmin,
    IsManager,
    IsMerchandiser,
    IsOwner,
)
from sample_manager.rest.serializers.files import FileSerializer


class FileListCreateView(ListCreateAPIView):
    serializer_class = FileSerializer

    def get_queryset(self):
        return File.objects.filter()

    def get_permissions(self):
        method = self.request.method

        if method == "GET":
            return [IsAuthenticated()]

        if method == "POST":
            return [OR(IsOwner(), OR(IsAdmin(), OR(IsManager(), IsMerchandiser())))]

        return [IsAuthenticated()]


class FileDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = FileSerializer
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
        return File.objects.filter()

    def delete(self, request, *args, **kwargs):
        file = self.get_object()
        file.status = Status.REMOVED
        file.save()
        return Response(
            {"detail": "File deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )
