from rest_framework import serializers

from core.models import User
from organizations.rest.serializers.company import CompanySerializer


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = "__all__"

    def get_role(self, obj):
        request_user = self.context["request"].user
        return request_user.get_role()

    def get_company(self, obj):
        company = self.context["request"].user.get_company()
        return CompanySerializer(company).data

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return super().create(validated_data)
