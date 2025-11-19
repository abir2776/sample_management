from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import OR, IsAuthenticated
from rest_framework.response import Response

from common.choices import Status
from sample_manager.models import Sample
from sample_manager.permissions import (
    IsAdmin,
    IsManager,
    IsMerchandiser,
    IsOwner,
)
from sample_manager.rest.serializers.sample import SampleSerializer


class SampleListCreateView(ListCreateAPIView):
    serializer_class = SampleSerializer

    def get_queryset(self):
        storage_uid = self.kwargs.get("storage_uid")
        organization = self.request.user.get_organization()
        return Sample.objects.filter(
            organization=organization, storage__uid=storage_uid
        )

    def get_permissions(self):
        method = self.request.method

        if method == "GET":
            return [IsAuthenticated()]

        if method == "POST":
            return [OR(IsOwner(), OR(IsAdmin(), OR(IsManager(), IsMerchandiser())))]

        return [IsAuthenticated()]


class SampleDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = SampleSerializer
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
        return Sample.objects.filter(
            organization=organization, storage__uid=storage_uid
        )

    def delete(self, request, *args, **kwargs):
        sample = self.get_object()
        sample.status = Status.REMOVED
        sample.save()
        return Response(
            {"detail": "Sample deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )
