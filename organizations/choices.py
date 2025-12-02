from django.db import models


class CompanyUserRole(models.TextChoices):
    SUPER_ADMIN = "SUPER_ADMIN", "Super_admin"
    ADMINISTRATOR = "ADMINISTRATOR", "Administrator"
    MANAGER = "MANAGER", "Manager"
    ACCOUNTANT = "ACCOUNTANT", "Accountant"
    MERCHANDISER = "MERCHANDISER", "Merchandiser"
    STAFF = "STAFF", "Staff"

    @classmethod
    def get_hierarchy(cls):
        return {
            cls.SUPER_ADMIN: 6,
            cls.ADMINISTRATOR: 5,
            cls.MANAGER: 4,
            cls.ACCOUNTANT: 3,
            cls.MERCHANDISER: 2,
            cls.STAFF: 1,
        }

    @classmethod
    def compare_roles(cls, role1, role2):
        hierarchy = cls.get_hierarchy()
        level1 = hierarchy.get(role1, 0)
        level2 = hierarchy.get(role2, 0)

        if level1 > level2:
            return 1
        elif level1 < level2:
            return -1
        return 0

    @classmethod
    def can_manage(cls, manager_role, target_role):
        return cls.compare_roles(manager_role, target_role) > 0


class DomainPlatformChoices(models.TextChoices):
    NAMECHEAP = "NAMECHEAP", "Namecheap"
    HOSTINGER = "HOSTINGER", "Hostinger"
    GODADDY = "GODADDY", "Godaddy"
    SPACESHIP = "SPACESHIP", "Spaceship"
    DREAMHOST = "DREAMHOST", "Dreamhost"
    BTCL = "BTCL", "BTCL"
    SQUARESPACE = "SQUARESPACE", "Squarespace"
    ZOHO = "ZOHO", "Zoho"
    NAME_DOT_COM = "NAME_DOT_COM", "Name_dot_com"
    GOOGLE = "GOOGLE", "Google"
    OTHERS = "OTHERS", "Others"


class ActivityType(models.TextChoices):
    LOGIN = "LOGIN", "Login"
    LOGOUT = "LOGOUT", "Logout"
