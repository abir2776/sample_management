from rest_framework import serializers

from organizations.choices import CompanyUserRole
from organizations.models import Company
from organizations.rest.serializers.company import CompanySerializer
from organizations.rest.serializers.users import UserSerializer
from sample_manager.models import Buyer


class BuyerSerializer(serializers.ModelSerializer):
    company_uid = serializers.CharField(write_only=True, required=False)
    company = CompanySerializer(read_only=True)

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


class BuyerHistorySerializer(serializers.ModelSerializer):
    changed_by = serializers.SerializerMethodField()

    class Meta:
        model = Buyer.history.model
        fields = [
            "id",
            "name",
            "street",
            "city",
            "state",
            "country",
            "status",
            "history_id",
            "history_type",
            "history_date",
            "changed_by",
        ]

    def get_changed_by(self, obj):
        return UserSerializer(obj.history_user).data
