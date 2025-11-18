from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from common.choices import Status
from sample_manager.models import Buyer
from sample_manager.permissions import (
    IsAdmin,
    IsOwner,
)
from sample_manager.rest.serializers.buyer import BuyerSerializer


class BuyerListCreateView(ListCreateAPIView):
    serializer_class = BuyerSerializer

    def get_queryset(self):
        organization = self.request.user.get_organization()
        return Buyer.objects.filter(organization=organization)

    def get_permissions(self):
        method = self.request.method

        if method == "GET":
            return [IsAuthenticated()]

        if method == "POST":
            return [IsOwner() | IsAdmin()]

        return [IsAuthenticated()]


class BuyerDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = BuyerSerializer
    lookup_field = "uid"

    def get_permissions(self):
        method = self.request.method

        if method == "GET":
            return [IsAuthenticated()]

        if method in ["PUT", "PATCH"]:
            return [IsOwner() | IsAdmin()]

        if method == "DELETE":
            return [IsOwner() | IsAdmin()]

        return [IsAuthenticated()]

    def get_queryset(self):
        organization = self.request.user.get_organization()
        return Buyer.objects.filter(organization=organization)

    def delete(self, request, *args, **kwargs):
        buyer = self.get_object()
        buyer.status = Status.REMOVED
        buyer.save()
        return Response(
            {"detail": "Buyer deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )
