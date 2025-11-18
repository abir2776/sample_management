import uuid

from autoslug import AutoSlugField
from django.db import models
from django.utils import timezone
from versatileimagefield.fields import VersatileImageField

from common.choices import Status
from common.models import BaseModelWithUID
from core.models import User

from .choices import OrganizationInvitationStatus, OrganizationUserRole
from .utils import (
    get_organization_media_path_prefix,
    get_organization_slug,
)


class Organization(BaseModelWithUID):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from=get_organization_slug, unique=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    logo = VersatileImageField(
        "Logo",
        upload_to=get_organization_media_path_prefix,
        blank=True,
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"

    def __str__(self):
        return self.name


class OrganizationUser(BaseModelWithUID):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="users"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="organization_profile"
    )
    role = models.CharField(
        max_length=20, choices=OrganizationUserRole, default="viewer"
    )
    title = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    class Meta:
        unique_together = ("organization", "user")
        verbose_name = "Organization User"
        verbose_name_plural = "Organization Users"
        ordering = ["organization", "user__username"]

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.organization.name})"

    def activate(self):
        self.is_active = True
        self.save()

    def deactivate(self):
        self.is_active = False
        self.save()

    def update_last_active(self):
        self.last_active = timezone.now()
        self.save()


class OrganizationUserInvitation(BaseModelWithUID):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="invitations"
    )
    email = models.EmailField()
    role = models.CharField(
        max_length=20, choices=OrganizationUserRole, default="viewer"
    )
    token = models.UUIDField(
        db_index=True, unique=True, default=uuid.uuid4, editable=False
    )
    sender = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="sent_invitations"
    )
    invitation_status = models.CharField(
        max_length=20,
        choices=OrganizationInvitationStatus.choices,
        default="pending",
    )
    sent_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Organization Invitation"
        verbose_name_plural = "Organization Invitations"
        ordering = ["-sent_at"]

    def __str__(self):
        return f"Invitation to {self.email} for {self.organization.name}"
