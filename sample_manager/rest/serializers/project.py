from django.db import transaction
from rest_framework import serializers

from common.serializers import ImageSlimSerializer
from organizations.models import Company
from sample_manager.models import (
    Image,
    Project,
    ProjectImage,
)


class ProjectSerializer(serializers.ModelSerializer):
    company_uid = serializers.CharField(write_only=True)
    image_uids = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        max_length=3,
        allow_empty=True,
        required=False,
    )
    images = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "uid",
            "company",
            "name",
            "started_at",
            "will_finish_at",
            "created_at",
            "updated_at",
            "company_uid",
            "image_uids",
            "images",
        ]
        read_only_fields = ["id", "uid", "created_at", "updated_at", "company"]

    def get_images(self, obj):
        image_ids = ProjectImage.objects.filter(project=obj).values_list(
            "image_id", flat=True
        )
        images = Image.objects.filter(id__in=image_ids)
        return ImageSlimSerializer(images, many=True).data

    @transaction.atomic
    def create(self, validated_data):
        company_uid = validated_data.pop("company_uid")
        image_uids = validated_data.pop("image_uids", [])

        company = Company.objects.filter(uid=company_uid).first()
        if company == None:
            raise serializers.ValidationError("Invalid company UID")

        project = Project.objects.create(
            company=company,
            **validated_data,
        )
        if image_uids:
            images = Image.objects.filter(uid__in=image_uids)
            ProjectImage.objects.bulk_create(
                [ProjectImage(project=project, image=img) for img in images]
            )

        return project

    @transaction.atomic
    def update(self, instance, validated_data):
        image_uids = validated_data.pop("image_uids", None)
        company_uid = validated_data.pop("company_uid")
        company = Company.objects.filter(uid=company_uid).first()
        if company == None:
            raise serializers.ValidationError("Invalid company UID")
        instance.company = company
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        if image_uids is not None:
            ProjectImage.objects.filter(project=instance).delete()
            images = Image.objects.filter(uid__in=image_uids)
            ProjectImage.objects.bulk_create(
                [ProjectImage(project=instance, image=img) for img in images]
            )

        return instance
