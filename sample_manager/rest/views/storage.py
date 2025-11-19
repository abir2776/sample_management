from rest_framework import status
from rest_framework.permissions import IsAuthenticated, OR
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from common.choices import Status
from sample_manager.models import Storage
from sample_manager.permissions import (
    IsAdmin,
    IsManager,
    IsMerchandiser,
    IsOwner,
)
from sample_manager.rest.serializers.storage import StorageSerializer


class StorageListCreateView(ListCreateAPIView):
    serializer_class = StorageSerializer

    def get_queryset(self):
        organization = self.request.user.get_organization()
        return Storage.objects.filter(organization=organization)

    def get_permissions(self):
        method = self.request.method

        if method == "GET":
            return [IsAuthenticated()]

        if method == "POST":
            return [OR(IsOwner(), OR(IsAdmin(), OR(IsManager(), IsMerchandiser())))]

        return [IsAuthenticated()]


class StorageDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = StorageSerializer
    queryset = Storage.objects.all()
    lookup_field = "uid"

    def get_permissions(self):
        method = self.request.method

        if method == "GET":
            return [IsAuthenticated()]

        if method in ["PUT", "PATCH"]:
            return [OR(IsOwner(), OR(IsAdmin(), OR(IsManager(), IsMerchandiser())))]

        if method == "DELETE":
            return [OR(IsOwner(), IsAdmin())]

        return [IsAuthenticated()]

    def delete(self, request, *args, **kwargs):
        storage = self.get_object()
        storage.status = Status.REMOVED
        storage.save()
        return Response(
            {"detail": "Bucket deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )
