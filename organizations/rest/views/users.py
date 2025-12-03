from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response

from common.choices import Status
from core.models import User
from organizations.choices import CompanyUserRole
from organizations.models import UserCompany
from organizations.rest.serializers.users import (
    AdminUserCreateSerializer,
    AdminUserDetailsSerializer,
    AdminUserListSerializer,
    CompanyUserSerializer,
)
from sample_manager.permissions import (
    IsAdministrator,
    IsSuperAdmin,
)


class CompanyUserListCreateView(ListCreateAPIView):
    serializer_class = CompanyUserSerializer
    permission_classes = [IsAdministrator]

    def get_queryset(self):
        company = self.request.user.get_company()
        role = self.request.user.get_role()
        if role == CompanyUserRole.SUPER_ADMIN:
            return UserCompany.objects.filter(status=Status.ACTIVE)
        queryset = UserCompany.objects.filter(company=company, status=Status.ACTIVE)
        return queryset


class CompanyUserDetailsView(RetrieveUpdateDestroyAPIView):
    serializer_class = CompanyUserSerializer
    permission_classes = [IsAdministrator]
    queryset = UserCompany.objects.filter(status=Status.ACTIVE)
    lookup_field = "uid"

    def delete(self, request, *args, **kwargs):
        company_user = self.get_object()
        company_user.status = Status.REMOVED
        company_user.save()
        company_user.user.is_active = False
        company_user.user.save()
        return Response(
            {"detail": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )


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


class AdminUserDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSuperAdmin]
    queryset = User.objects.all()
    serializer_class = AdminUserDetailsSerializer
    lookup_field = "id"
