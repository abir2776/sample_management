from django.db import transaction
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from organizations.models import Organization, OrganizationUser
from organizations.rest.serializers.organizations import OrganizationSerializer
from sample_manager.permissions import (
    IsAdmin,
    IsManager,
    IsMerchandiser,
    IsOwner,
)


class MyOrganizationListCreate(ListCreateAPIView):
    serializer_class = OrganizationSerializer

    def get_queryset(self):
        user = self.request.user
        organization_ids = OrganizationUser.objects.filter(user=user).values_list(
            "organization_id", flat=True
        )
        organizations = Organization.objects.filter(id__in=organization_ids)
        return organizations

    def get_permissions(self):
        method = self.request.method

        if method == "GET":
            return [IsAuthenticated()]

        if method == "POST":
            return [IsOwner() | IsAdmin() | IsManager() | IsMerchandiser()]

        return [IsAuthenticated()]


class SwitchOrganizationAPIView(APIView):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user = request.user
        org_uid = request.data.get("organization_uid")

        if not org_uid:
            return Response(
                {"detail": "organization_uid is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        org = Organization.objects.filter(uid=org_uid).first()
        if not org:
            return Response(
                {"detail": "No organization found with this UID"},
                status=status.HTTP_404_NOT_FOUND,
            )
        org_user = OrganizationUser.objects.filter(user=user, organization=org).first()

        if not org_user:
            return Response(
                {"detail": "You are not a member of this organization"},
                status=status.HTTP_403_FORBIDDEN,
            )
        OrganizationUser.objects.filter(user=user, is_active=True).update(
            is_active=False
        )
        org_user.is_active = True
        org_user.save()

        return Response(
            {"detail": "Organization switched successfully"}, status=status.HTTP_200_OK
        )
