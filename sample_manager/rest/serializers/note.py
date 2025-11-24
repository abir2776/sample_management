from rest_framework import serializers

from organizations.models import Company
from sample_manager.models import Note


class NoteSerializer(serializers.ModelSerializer):
    company_uid = serializers.CharField(write_only=True)

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
        company_uid = validated_data.pop("company_uid")
        user = self.context["request"].user
        company = Company.objects.filter(uid=company_uid).first()
        if company == None:
            raise serializers.ValidationError("Invalid company UID")

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
