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
from sample_manager.models import Buyer
from sample_manager.permissions import IsAdministrator, IsSuperAdmin
from sample_manager.rest.serializers.buyer import (
    BuyerHistorySerializer,
    BuyerSerializer,
)


class BuyerListCreateView(ListCreateAPIView):
    serializer_class = BuyerSerializer
    filter_backends = [SearchFilter]
    search_fields = ["name"]

    def get_queryset(self):
        role = self.request.user.get_role()
        if role == CompanyUserRole.SUPER_ADMIN:
            return Buyer.objects.filter(status=Status.ACTIVE)
        company = self.request.user.get_company()
        return Buyer.objects.filter(company=company, status=Status.ACTIVE)

    def get_permissions(self):
        method = self.request.method

        if method == "GET":
            return [IsAuthenticated()]

        if method == "POST":
            return [OR(IsSuperAdmin(), IsAdministrator())]

        return [IsAuthenticated()]


class BuyerDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = BuyerSerializer
    queryset = Buyer.objects.filter(status=Status.ACTIVE)
    lookup_field = "uid"

    def get_permissions(self):
        method = self.request.method

        if method == "GET":
            return [IsAuthenticated()]

        if method in ["PUT", "PATCH"]:
            return [OR(IsSuperAdmin(), IsAdministrator())]

        if method == "DELETE":
            return [OR(IsSuperAdmin(), IsAdministrator())]

        return [IsAuthenticated()]

    def delete(self, request, *args, **kwargs):
        buyer = self.get_object()
        buyer.status = Status.REMOVED
        buyer.save()
        return Response(
            {"detail": "Buyer deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )


class BuyerHistoryListView(ListAPIView):
    serializer_class = BuyerHistorySerializer
    permission_classes = [OR(IsSuperAdmin(), IsAdministrator())]

    def get_queryset(self):
        buyer_uid = self.kwargs.get("uid")
        return Buyer.history.filter(id=buyer_uid).order_by("-history_date")
