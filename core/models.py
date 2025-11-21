import logging
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from simple_history.models import HistoricalRecords
from versatileimagefield.fields import VersatileImageField

from common.choices import Status
from common.models import BaseModelWithUID

from .choices import UserGender
from .managers import CustomUserManager
from .utils import get_user_media_path_prefix

logger = logging.getLogger(__name__)


class User(AbstractUser, BaseModelWithUID):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, null=True, blank=True, editable=False)
    phone = PhoneNumberField(
        unique=True, db_index=True, verbose_name="Phone Number", blank=True, null=True
    )
    mobile = PhoneNumberField(
        unique=True, db_index=True, verbose_name="Mobile Number", blank=True, null=True
    )
    whatsapp = PhoneNumberField(
        unique=True,
        db_index=True,
        verbose_name="What's app Number",
        blank=True,
        null=True,
    )
    profile_picture = VersatileImageField(
        "Picture",
        upload_to=get_user_media_path_prefix,
        blank=True,
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    gender = models.CharField(
        max_length=20,
        blank=True,
        choices=UserGender.choices,
        default=UserGender.UNKNOWN,
    )
    created_by = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
    )
    history = HistoricalRecords()

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ("-date_joined",)

    def __str__(self):
        return f"UID: {self.uid}, Phone: {self.phone}"

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = uuid.uuid4()
        super().save(*args, **kwargs)

    def get_name(self):
        name = " ".join([self.first_name, self.last_name])
        return name.strip()

    def get_company(self):
        return (
            self.company_profile.filter(is_active=True)
            .select_related("company")
            .first()
            .company
        )

    def get_role(self):
        return self.company_profile.filter(is_active=True).first().role
