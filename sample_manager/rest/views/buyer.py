from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, OR
from rest_framework.response import Response

from common.choices import Status
from sample_manager.models import Buyer
from sample_manager.permissions import IsSuperAdmin, IsAdministrator
from sample_manager.rest.serializers.buyer import BuyerSerializer


class BuyerListCreateView(ListCreateAPIView):
    serializer_class = BuyerSerializer

    def get_queryset(self):
        company = self.request.user.get_company()
        return Buyer.objects.filter(company=company)

    def get_permissions(self):
        method = self.request.method

        if method == "GET":
            return [IsAuthenticated()]

        if method == "POST":
            return [IsSuperAdmin()]

        return [IsAuthenticated()]


class BuyerDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = BuyerSerializer
    lookup_field = "uid"

    def get_permissions(self):
        method = self.request.method

        if method == "GET":
            return [IsAuthenticated()]

        if method in ["PUT", "PATCH"]:
            return [OR(IsSuperAdmin(), IsAdministrator())]

        if method == "DELETE":
            return [IsSuperAdmin()]

        return [IsAuthenticated()]

    def get_queryset(self):
        company = self.request.user.get_company()
        return Buyer.objects.filter(company=company)

    def delete(self, request, *args, **kwargs):
        buyer = self.get_object()
        buyer.status = Status.REMOVED
        buyer.save()
        return Response(
            {"detail": "Buyer deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )
