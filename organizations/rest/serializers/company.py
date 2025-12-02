from rest_framework import serializers

from core.models import User
from organizations.models import Company, UserCompany


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"
        read_only_fields = ["uid", "status"]


class CompanyAddUserSerializer(serializers.Serializer):
    company_uid = serializers.CharField(write_only=True)
    user_id = serializers.CharField(write_only=True)
    role = serializers.CharField(write_only=True)

    def create(self, validated_data):
        company_uid = validated_data.pop("company_uid")
        user_id = validated_data.pop("user_id")
        role = validated_data.pop("role")
        company = Company.objects.filter(uid=company_uid).first()
        if company == None:
            raise serializers.ValidationError("Invalid Company uid")
        user = User.objects.filter(id=user_id).first()
        if user == None:
            raise serializers.ValidationError("Invalid User uid")
        company_user = UserCompany.objects.create(user=user, company=company, role=role)
        return company_user
