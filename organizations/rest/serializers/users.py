from django.db import transaction
from rest_framework import serializers

from core.models import User
from organizations.models import OrganizationUser


class OrganizationUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = OrganizationUser
        fields = "__all__"
        read_only_fields = [
            "id",
            "uid",
            "organization",
            "first_name",
            "last_name",
            "password",
            "user",
            "is_active",
            "joined_at",
            "lat_active",
        ]

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

    def create(self, validated_data):
        user = self.context["request"].user
        organization = user.get_organization()

        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")
        password = validated_data.pop("password")
        email = validated_data.get("email", "")
        phone = validated_data.get("phone", "")

        with transaction.atomic():
            new_user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
            )
            new_user.set_password(password)
            new_user.save()
            organization_user = OrganizationUser.objects.create(
                organization=organization, user=new_user, **validated_data
            )

        return organization_user
