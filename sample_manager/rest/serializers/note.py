from rest_framework import serializers

from organizations.choices import CompanyUserRole
from organizations.models import Company
from sample_manager.models import Note
from organizations.rest.serializers.company import CompanySerializer
from organizations.rest.serializers.users import UserSerializer


class NoteSerializer(serializers.ModelSerializer):
    company_uid = serializers.CharField(write_only=True, required=False)
    company = CompanySerializer(read_only=True)

    class Meta:
        model = Note
        fields = [
            "id",
            "uid",
            "company",
            "company_uid",
            "title",
            "description",
            "created_by",
            "status",
        ]
        read_only_fields = ["id", "uid", "company", "created_by", "status"]

    def create(self, validated_data):
        company_uid = validated_data.pop("company_uid", None)
        user = self.context["request"].user
        role = user.get_role()
        if role == CompanyUserRole.SUPER_ADMIN:
            company = Company.objects.filter(uid=company_uid).first()
            if company == None:
                raise serializers.ValidationError("Invalid company UID")
        else:
            company = user.get_company()

        note = Note.objects.create(company=company, created_by=user, **validated_data)
        return note

    def update(self, instance, validated_data):
        company_uid = validated_data.pop("company_uid")
        company = Company.objects.filter(uid=company_uid).first()
        if company == None:
            raise serializers.ValidationError("Invalid company UID")
        instance.company = company
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class NoteHistorySerializer(serializers.ModelSerializer):
    changed_by = serializers.SerializerMethodField()

    class Meta:
        model = Note.history.model
        fields = [
            "id",
            "title",
            "description",
            "company",
            "created_by",
            "status",
            "history_id",
            "history_type",
            "history_date",
            "changed_by",
        ]

    def get_changed_by(self, obj):
        return UserSerializer(obj.history_user).data
