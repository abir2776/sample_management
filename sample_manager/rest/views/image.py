from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import OR, IsAuthenticated
from rest_framework.response import Response

from common.choices import Status
from sample_manager.models import Image
from sample_manager.permissions import (
    IsAccountant,
    IsAdministrator,
    IsManager,
    IsMerchandiser,
    IsSuperAdmin,
)
from sample_manager.rest.serializers.image import ImageSerializer


class ImageListCreateView(ListCreateAPIView):
    serializer_class = ImageSerializer

    def get_queryset(self):
        return Image.objects.filter()

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


class ImageDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ImageSerializer
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

    def get_queryset(self):
        return Image.objects.filter()

    def delete(self, request, *args, **kwargs):
        file = self.get_object()
        file.status = Status.REMOVED
        file.save()
        return Response(
            {"detail": "Image deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )
