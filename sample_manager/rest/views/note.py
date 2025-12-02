from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import OR, IsAuthenticated
from rest_framework.response import Response

from common.choices import Status
from organizations.choices import CompanyUserRole
from sample_manager.models import Note
from sample_manager.permissions import (
    IsAdministrator,
    IsSuperAdmin,
)
from sample_manager.rest.serializers.note import NoteSerializer


class NoteListCreateView(ListCreateAPIView):
    serializer_class = NoteSerializer

    def get_queryset(self):
        role = self.request.user.get_role()
        company = self.request.user.get_company()
        if role == CompanyUserRole.SUPER_ADMIN:
            return Note.objects.filter()
        company = self.request.user.get_company()
        return Note.objects.filter(company=company)

    def get_permissions(self):
        method = self.request.method

        if method == "GET":
            return [IsAuthenticated()]

        if method == "POST":
            return [OR(IsSuperAdmin(), IsAdministrator())]

        return [IsAuthenticated()]


class NoteDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer
    lookup_field = "uid"

    def get_queryset(self):
        company = self.request.user.get_company()
        return Note.objects.filter(company=company)

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
        note = self.get_object()
        note.status = Status.REMOVED
        note.save()

        return Response(
            {"detail": "Note deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
