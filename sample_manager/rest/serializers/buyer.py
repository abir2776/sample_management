from rest_framework import serializers

from organizations.choices import CompanyUserRole
from organizations.models import Company
from sample_manager.models import Buyer


class BuyerSerializer(serializers.ModelSerializer):
    company_uid = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Buyer
        fields = "__all__"
        read_only_fields = [
            "id",
            "uid",
            "created_by",
            "company",
            "status",
            "company_uid",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        role = user.get_role()
        if role == CompanyUserRole.SUPER_ADMIN:
            company_uid = validated_data.pop("company_uid", "")
            company = Company.objects.filter(uid=company_uid).first()
            if not company:
                raise serializers.ValidationError("Invalid company uid")
        else:
            company = user.get_company()
        buyer = Buyer.objects.create(company=company, created_by=user, **validated_data)
        return buyer
