from django.db import transaction
from rest_framework import serializers

from core.models import User
from core.rest.serializers.users import UserSerializer
from organizations.models import Company, UserCompany


class CompanyUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    email = serializers.CharField(write_only=True)
    phone = serializers.CharField(write_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserCompany
        fields = "__all__"
        read_only_fields = [
            "id",
            "uid",
            "first_name",
            "last_name",
            "password",
            "user",
            "is_active",
            "joined_at",
            "lat_active",
            "created_by",
            "company",
            "email",
            "phone",
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
        company = user.get_company()
        company_user = user.get_company_user()

        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")
        password = validated_data.pop("password")
        email = validated_data.pop("email", "")
        phone = validated_data.pop("phone", "")
        role = validated_data.get("role", "")
        company_user.validate_role_permission(role)
        with transaction.atomic():
            new_user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                username=email,
            )
            new_user.set_password(password)
            new_user.save()
            user_company = UserCompany.objects.create(
                company=company, user=new_user, created_by=user, **validated_data
            )

        return user_company

    def update(self, instance, validated_data):
        user = self.context["request"].user
        company_user = user.get_company_user()
        role = validated_data.get("role")

        if instance.user.id != user.id:
            company_user.validate_role_permission(role)

        first_name = validated_data.pop("first_name", None)
        if first_name:
            instance.user.first_name = first_name
        last_name = validated_data.pop("last_name", None)
        if last_name:
            instance.user.last_name = last_name
        email = validated_data.pop("email", None)
        if email:
            instance.user.email = email
        phone = validated_data.pop("phone")
        if phone:
            instance.user.phone = phone
        password = validated_data.pop("password")
        if password:
            instance.user.set_password(password)
        instance.user.save()
        return super().update(instance, validated_data)


class AdminUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class AdminUserCreateSerializer(serializers.Serializer):
    email = serializers.CharField()
    phone = serializers.CharField(required=False)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    company_uid = serializers.CharField()
    password = serializers.CharField()
    role = serializers.CharField()

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
        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")
        password = validated_data.pop("password")
        email = validated_data.get("email", "")
        phone = validated_data.get("phone", "")
        company_uid = validated_data.pop("company_uid", "")
        role = validated_data.pop("role", "")
        user = self.context["request"].user
        company = Company.objects.filter(uid=company_uid).first()
        if not company:
            raise serializers.ValidationError("Invalid Company UID")

        with transaction.atomic():
            new_user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                username=email,
            )
            new_user.set_password(password)
            new_user.save()
            UserCompany.objects.create(
                company=company, user=new_user, role=role, created_by=user
            )

        return new_user


class AdminUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone", "password"]

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)
        instance.save()
        return super().update(instance, validated_data)
