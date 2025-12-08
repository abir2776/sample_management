from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import OR, IsAuthenticated
from rest_framework.response import Response

from common.choices import Status
from organizations.choices import CompanyUserRole
from sample_manager.models import Project
from sample_manager.permissions import (
    IsAdministrator,
    IsSuperAdmin,
)
from sample_manager.rest.serializers.project import (
    ProjectHistorySerializer,
    ProjectSerializer,
)


class ProjectListCreateView(ListCreateAPIView):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        role = self.request.user.get_role()
        company = self.request.user.get_company()
        if role == CompanyUserRole.SUPER_ADMIN:
            return Project.objects.filter(status=Status.ACTIVE)
        return Project.objects.filter(company=company, status=Status.ACTIVE)

    def get_permissions(self):
        method = self.request.method

        if method == "GET":
            return [IsAuthenticated()]

        if method == "POST":
            return [OR(IsSuperAdmin(), IsAdministrator())]

        return [IsAuthenticated()]


class ProjectDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    lookup_field = "uid"

    def get_queryset(self):
        return Project.objects.filter(status=Status.ACTIVE)

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
        project = self.get_object()
        project.status = Status.REMOVED
        project.save()

        return Response(
            {"detail": "Project deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class ProjectHistoryListView(ListAPIView):
    permission_classes = [OR(IsSuperAdmin(), IsAdministrator())]
    serializer_class = ProjectHistorySerializer

    def get_queryset(self):
        project_uid = self.kwargs.get("uid")
        return Project.history.filter(id=project_uid).order_by("-history_date")
