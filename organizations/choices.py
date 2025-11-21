from django.db import models


class CompanyUserRole(models.TextChoices):
    SUPER_ADMIN = "SUPER_ADMIN", "Super_admin"
    ADMINISTRATOR = "ADMINISTRATOR", "Administrator"
    MANAGER = "MANAGER", "Manager"
    ACCOUNTANT = "ACCOUNTANT", "Accountant"
    MERCHANDISER = "MERCHANDISER", "Merchandiser"
    STAFF = "STAFF", "Staff"


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
