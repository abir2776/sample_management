from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import OR, IsAuthenticated

from organizations.choices import CompanyUserRole
from sample_manager.models import ModifyRequest
from sample_manager.permissions import (
    IsAccountant,
    IsAdministrator,
    IsManager,
    IsMerchandiser,
    IsSuperAdmin,
)
from sample_manager.rest.serializers.requests import ModifyRequestSerializer


class ModifyRequestListView(ListAPIView):
    serializer_class = ModifyRequestSerializer

    def get_permissions(self):
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        role = user.get_role()
        company = user.get_company()
        if role == CompanyUserRole.STAFF:
            return ModifyRequest.objects.filter(
                requested_user=user, company=company
            ).order_by("-created_at")
        if role == CompanyUserRole.SUPER_ADMIN:
            return ModifyRequest.objects.filter()
        return ModifyRequest.objects.filter(company=company).order_by("-created_at")


class ModifyRequestRetrieveUpdateView(RetrieveUpdateAPIView):
    serializer_class = ModifyRequestSerializer

    def get_permissions(self):
        return [
            OR(
                IsAdministrator(),
                OR(
                    IsAccountant(),
                    OR(IsSuperAdmin(), OR(IsManager(), IsMerchandiser())),
                ),
            )
        ]

    lookup_field = "uid"

    def get_queryset(self):
        user = self.request.user
        company = user.get_company()
        return ModifyRequest.objects.filter(company=company)
