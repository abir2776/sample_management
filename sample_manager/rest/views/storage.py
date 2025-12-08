from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import OR, IsAuthenticated
from rest_framework.response import Response

from common.choices import Status
from organizations.choices import CompanyUserRole
from sample_manager.models import Storage
from sample_manager.permissions import (
    IsAccountant,
    IsAdministrator,
    IsManager,
    IsMerchandiser,
    IsSuperAdmin,
)
from sample_manager.rest.serializers.storage import (
    StorageHistorySerializer,
    StorageSerializer,
)


class StorageListCreateView(ListCreateAPIView):
    serializer_class = StorageSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["type"]
    search_fields = ["name"]

    def get_queryset(self):
        request = self.request
        parent_uid = request.query_params.get("parent_uid")
        company = request.user.get_company()
        role = request.user.get_role()
        base_queryset = Storage.objects.all()
        if role != CompanyUserRole.SUPER_ADMIN:
            base_queryset = base_queryset.filter(company=company, status=Status.ACTIVE)
        if parent_uid:
            return base_queryset.filter(parent__uid=parent_uid, status=Status.ACTIVE)
        return base_queryset.filter(parent__isnull=True, status=Status.ACTIVE)

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
    queryset = Storage.objects.filter(status=Status.ACTIVE)
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
            return [OR(IsSuperAdmin(), IsAdministrator())]

        return [IsAuthenticated()]

    def delete(self, request, *args, **kwargs):
        storage = self.get_object()
        storage.status = Status.REMOVED
        storage.save()
        return Response(
            {"detail": "Storage deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class StorageHistoryListView(ListAPIView):
    permission_classes = [OR(IsSuperAdmin(), IsAdministrator())]
    serializer_class = StorageHistorySerializer

    def get_queryset(self):
        storage_uid = self.kwargs.get("uid")
        return Storage.history.filter(id=storage_uid).order_by("-history_date")
