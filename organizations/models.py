from django.db import models
from django.utils import timezone

from common.choices import Status
from common.models import BaseModelWithUID
from core.models import User

from .choices import ActivityType, CompanyUserRole, DomainPlatformChoices


class Company(BaseModelWithUID):
    name = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(null=True, blank=True)
    trade_licence_no = models.CharField(null=True, blank=True)
    tax_code = models.CharField(null=True, blank=True)
    domain_name = models.CharField(null=True, blank=True)
    domain_platform = models.CharField(
        max_length=20, choices=DomainPlatformChoices, null=True, blank=True
    )
    custom_domain_platform = models.CharField(null=True, blank=True, max_length=255)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Company"
        verbose_name_plural = "Companys"

    def __str__(self):
        return self.name


class UserCompany(BaseModelWithUID):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="users")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="company_profile"
    )
    role = models.CharField(
        max_length=20, choices=CompanyUserRole, default=CompanyUserRole.STAFF
    )
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    class Meta:
        unique_together = ("company", "user")
        verbose_name = "Company User"
        verbose_name_plural = "Company Users"
        ordering = ["company", "user__username"]

    def __str__(self):
        return (
            f"{self.user.get_full_name() or self.user.username} ({self.company.name})"
        )

    def activate(self):
        self.is_active = True
        self.save()

    def deactivate(self):
        self.is_active = False
        self.save()

    def update_last_active(self):
        self.last_active = timezone.now()
        self.save()


class ActivityLog(BaseModelWithUID):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    type = models.CharField(
        max_length=20,
        choices=ActivityType.choices,
        default=ActivityType.LOGIN,
    )

    def __str__(self):
        return f"{self.user.get_name}-{self.type}"
