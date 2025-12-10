from rest_framework import serializers

from core.models import User
from organizations.rest.serializers.company import CompanySerializer


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = "__all__"

    def get_role(self, obj):
        request_user = self.context["request"].user
        return request_user.get_role()

    def get_company(self, obj):
        company = self.context["request"].user.get_company()
        return CompanySerializer(company).data

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
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        email = validated_data.get("email", None)
        if password:
            instance.set_password(password)
        if email:
            instance.username = email
        instance.save()
        return super().update(instance, validated_data)
