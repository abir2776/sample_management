from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import OR, IsAuthenticated
from rest_framework.response import Response

from core.models import User
from organizations.choices import CompanyUserRole
from organizations.models import UserCompany
from organizations.rest.serializers.users import (
    AdminUserCreateSerializer,
    AdminUserListSerializer,
    CompanyUserSerializer,
)
from sample_manager.permissions import (
    IsAccountant,
    IsAdministrator,
    IsManager,
    IsMerchandiser,
    IsSuperAdmin,
)


class CompanyUserListCreateView(ListCreateAPIView):
    serializer_class = CompanyUserSerializer

    def get_queryset(self):
        company = self.request.user.get_company()
        role = self.request.user.get_role()
        if role == CompanyUserRole.SUPER_ADMIN:
            return UserCompany.objects.filter()
        queryset = UserCompany.objects.filter(company=company)
        return queryset

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
                        OR(IsManager(), IsMerchandiser()),
                    ),
                )
            ]

        return [IsAuthenticated()]


class CompanyUserDetailsView(RetrieveUpdateDestroyAPIView):
    serializer_class = CompanyUserSerializer
    queryset = UserCompany.objects.filter()
    lookup_field = "uid"

    def get_permissions(self):
        method = self.request.method

        if method == "GET":
            return [IsAuthenticated()]

        if method == "PUT" or method == "PATCH":
            return [
                OR(
                    IsAdministrator(),
                    OR(
                        IsAccountant(),
                        OR(IsManager(), IsMerchandiser()),
                    ),
                )
            ]

        return [IsAuthenticated()]


class AdminUserView(ListCreateAPIView):
    permission_classes = [IsSuperAdmin]
    queryset = User.objects.all()
    serializer_class = AdminUserListSerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AdminUserCreateSerializer
        return AdminUserListSerializer

    def create(self, request, *args, **kwargs):
        serializer = AdminUserCreateSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        output_serializer = AdminUserListSerializer(user)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
