from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import OR

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
        return [
            OR(
                IsAdministrator(),
                OR(
                    IsAccountant(),
                    OR(IsSuperAdmin(), OR(IsManager(), IsMerchandiser())),
                ),
            )
        ]

    def get_queryset(self):
        user = self.request.user
        company = user.get_company()
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
