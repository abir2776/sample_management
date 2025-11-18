from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from common.choices import Status
from sample_manager.models import Bucket
from sample_manager.permissions import (
    IsAdmin,
    IsManager,
    IsMerchandiser,
    IsOwner,
)
from sample_manager.rest.serializers.bucket import BucketSerializer


class BucketListCreateView(ListCreateAPIView):
    serializer_class = BucketSerializer

    def get_queryset(self):
        organization = self.request.user.get_organization()
        return Bucket.objects.filter(organization=organization)

    def get_permissions(self):
        method = self.request.method

        if method == "GET":
            return [IsAuthenticated()]

        if method == "POST":
            return [IsOwner() | IsAdmin() | IsManager() | IsMerchandiser()]

        return [IsAuthenticated()]


class BucketDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = BucketSerializer
    queryset = Bucket.objects.all()
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

    def delete(self, request, *args, **kwargs):
        bucket = self.get_object()
        bucket.status = Status.REMOVED
        bucket.save()
        return Response(
            {"detail": "Bucket deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )
