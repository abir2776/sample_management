from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import OR, IsAuthenticated
from rest_framework.response import Response

from common.choices import Status
from sample_manager.models import Storage
from sample_manager.permissions import (
    IsAccountant,
    IsAdministrator,
    IsManager,
    IsMerchandiser,
    IsSuperAdmin,
)
from sample_manager.rest.serializers.storage import StorageSerializer


class StorageListCreateView(ListCreateAPIView):
    serializer_class = StorageSerializer

    def get_queryset(self):
        company = self.request.user.get_company()
        return Storage.objects.filter(company=company)

    def get_permissions(self):
        method = self.request.method

        if method == "GET":
            return [IsAuthenticated()]

        if method == "POST":
            return [
                OR(
                    IsAdministrator(),
                    OR(
                        IsAccountant(),
                        OR(IsSuperAdmin(), OR(IsManager(), IsMerchandiser())),
                    ),
                )
            ]

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
            return [
                OR(
                    IsAdministrator(),
                    OR(
                        IsAccountant(),
                        OR(IsSuperAdmin(), OR(IsManager(), IsMerchandiser())),
                    ),
                )
            ]

        if method == "DELETE":
            return [OR(IsSuperAdmin, IsAdministrator())]

        return [IsAuthenticated()]

    def delete(self, request, *args, **kwargs):
        storage = self.get_object()
        storage.status = Status.REMOVED
        storage.save()
        return Response(
            {"detail": "Bucket deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )
