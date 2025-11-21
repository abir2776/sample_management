from rest_framework.permissions import BasePermission


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        role = request.user.get_role()
        return role == "SUPER_ADMIN"


class IsAdministrator(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        role = request.user.get_role()
        return role == "ADMINISTRATOR"


class IsManager(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        role = request.user.get_role()
        return role == "MANAGER"


class IsAccountant(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        role = request.user.get_role()
        return role == "ACCOUNTANT"


class IsMerchandiser(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        role = request.user.get_role()
        return role == "MERCHANDISER"


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        role = request.user.get_role()
        return role == "STAFF"
