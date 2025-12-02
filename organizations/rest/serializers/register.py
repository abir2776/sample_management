import logging

from django.db import transaction
from rest_framework import serializers
from versatileimagefield.serializers import VersatileImageFieldSerializer

from core.models import User
from organizations.choices import CompanyUserRole
from organizations.models import Company, UserCompany

logger = logging.getLogger(__name__)


class PublicOrganizationRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    phone = serializers.CharField(min_length=7, max_length=20)
    first_name = serializers.CharField(min_length=2, max_length=50)
    last_name = serializers.CharField(min_length=2, max_length=50)
    org_name = serializers.CharField(min_length=2, max_length=100)
    org_website = serializers.URLField(required=False, allow_null=True)
    address = serializers.CharField(required=False, allow_null=True)
    country = serializers.CharField(required=False, allow_null=True)
    org_description = serializers.CharField(required=False, allow_null=True)
    logo = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at256", "crop__256x256"),
            ("at512", "crop__512x512"),
        ],
        required=False,
    )

    def validate_email(self, data):
        email = data.lower()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with email already exists!")
        return data

    def validate_phone(self, data):
        phone = data
        if User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError("User with phone already exists!")
        return data

    def create(self, validated_data, *args, **kwargs):
        with transaction.atomic():
            email = validated_data["email"].lower()
            phone = validated_data["phone"]
            first_name = validated_data["first_name"]
            last_name = validated_data["last_name"]
            password = validated_data["password"]

            user = User.objects.create(
                email=email,
                username=email,
                phone=phone,
                first_name=first_name,
                last_name=last_name,
                is_active=True,
            )
            user.set_password(password)
            user.save()
            logger.debug(f"Created new user: {user}")

            org_name = validated_data["org_name"]
            if len(org_name) == 0:
                org_name = f"{first_name} {last_name}"
            company = Company.objects.create(name=org_name)
            logger.debug(f"Created new user: {user}")
            UserCompany.objects.create(
                user=user,
                created_by=user,
                company=company,
                role=CompanyUserRole.SUPER_ADMIN,
                is_active=True,
            )
            logger.debug(f"Added user: {user} to company: {company}")
        return user
