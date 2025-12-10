from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import OR, IsAuthenticated
from rest_framework.response import Response

from common.choices import Status
from sample_manager.choices import StorageType
from sample_manager.models import GarmentSample, Storage
from sample_manager.permissions import (
    IsAdministrator,
    IsSuperAdmin,
)
from sample_manager.rest.filters.sample_filter import GarmentSampleFilter
from sample_manager.rest.serializers.sample import (
    GarmentSampleHistorySerializer,
    SampleSerializer,
)


class SampleListCreateView(ListCreateAPIView):
    serializer_class = SampleSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = GarmentSampleFilter
    search_fields = ["name", "style_no", "sku_no", "fabrication"]
    ordering_fields = ["name", "arrival_date", "color"]
    ordering = ["created_at"]

    def get_queryset(self):
        storage_uid = self.kwargs.get("storage_uid")
        storage = Storage.objects.filter(
            uid=storage_uid, type=StorageType.SPACE, status=Status.ACTIVE
        ).first()
        if not storage:
            raise APIException("Invalid storage uid provided")
        company = self.request.user.get_company()
        return GarmentSample.objects.filter(
            company=company,
            storage__uid=storage_uid,
            is_active=True,
            status=Status.ACTIVE,
        )

    def get_permissions(self):
        method = self.request.method

        if method == "GET":
            return [IsAuthenticated()]

        if method == "POST":
            return [IsAuthenticated()]

        return [IsAuthenticated()]


class SampleDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = SampleSerializer
    lookup_field = "uid"

    def get_permissions(self):
        method = self.request.method

        if method == "GET":
            return [IsAuthenticated()]

        if method in ["PUT", "PATCH"]:
            return [IsAuthenticated()]

        if method == "DELETE":
            return [OR(IsSuperAdmin(), IsAdministrator())]

        return [IsAuthenticated()]

    def get_queryset(self):
        storage_uid = self.kwargs.get("storage_uid")
        storage = Storage.objects.filter(
            uid=storage_uid, type=StorageType.SPACE, status=Status.ACTIVE
        ).first()
        if not storage:
            raise APIException("Invalid storage uid provided")
        company = self.request.user.get_company()
        return GarmentSample.objects.filter(
            company=company,
            storage__uid=storage_uid,
            is_active=True,
            status=Status.ACTIVE,
        )

    def delete(self, request, *args, **kwargs):
        sample = self.get_object()
        sample.status = Status.REMOVED
        sample.save()
        return Response(
            {"detail": "Sample deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )


class GarmentSampleHistoryListView(ListAPIView):
    permission_classes = [OR(IsSuperAdmin(), IsAdministrator())]
    serializer_class = GarmentSampleHistorySerializer

    def get_queryset(self):
        uid = self.kwargs.get("uid")
        return GarmentSample.history.filter(id=uid).order_by("-history_date")
