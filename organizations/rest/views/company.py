from django.db import transaction
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from organizations.models import Company, UserCompany
from organizations.rest.serializers.company import (
    CompanySerializer,
    CompanyAddUserSerializer,
)
from sample_manager.permissions import IsSuperAdmin


class MyCompanyListCreate(ListCreateAPIView):
    serializer_class = CompanySerializer

    def get_queryset(self):
        user = self.request.user
        company_ids = UserCompany.objects.filter(user=user).values_list(
            "organization_id", flat=True
        )
        companys = Company.objects.filter(id__in=company_ids)
        return companys

    def get_permissions(self):
        method = self.request.method

        if method == "GET":
            return [IsAuthenticated()]

        if method == "POST":
            return [IsSuperAdmin]

        return [IsAuthenticated()]


class SwitchCompanyAPIView(APIView):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user = request.user
        company_uid = request.data.get("company_uid")

        if not company_uid:
            return Response(
                {"detail": "company_uid is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        company = Company.objects.filter(uid=company_uid).first()
        if not company:
            return Response(
                {"detail": "No company found with this UID"},
                status=status.HTTP_404_NOT_FOUND,
            )
        company_user = UserCompany.objects.filter(user=user, company=company).first()

        if not company_user:
            return Response(
                {"detail": "You are not a member of this company"},
                status=status.HTTP_403_FORBIDDEN,
            )
        UserCompany.objects.filter(user=user, is_active=True).update(is_active=False)
        company_user.is_active = True
        company_user.save()

        return Response(
            {"detail": "Company switched successfully"}, status=status.HTTP_200_OK
        )


class CompanyAddUserView(CreateAPIView):
    permission_classes = [IsSuperAdmin]
    serializer_class = CompanyAddUserSerializer
