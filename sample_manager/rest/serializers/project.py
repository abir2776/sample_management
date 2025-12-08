from django.db import transaction
from rest_framework import serializers

from common.serializers import BuyerSlimSerializer, ImageSlimSerializer
from organizations.choices import CompanyUserRole
from organizations.models import Company
from organizations.rest.serializers.company import CompanySerializer
from organizations.rest.serializers.users import UserSerializer
from sample_manager.models import (
    Buyer,
    Image,
    Project,
    ProjectBuyerConnection,
    ProjectImage,
)


class ProjectSerializer(serializers.ModelSerializer):
    company_uid = serializers.CharField(write_only=True, required=False)
    image_uids = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        max_length=3,
        allow_empty=True,
        required=False,
    )
    buyer_uids = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        max_length=3,
        allow_empty=True,
        required=False,
    )
    images = serializers.SerializerMethodField()
    buyers = serializers.SerializerMethodField()
    company = CompanySerializer(read_only=True)

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
            "buyer_uids",
            "buyers",
        ]
        read_only_fields = ["id", "uid", "created_at", "updated_at", "company"]

    def get_images(self, obj):
        image_ids = ProjectImage.objects.filter(project=obj).values_list(
            "image_id", flat=True
        )
        images = Image.objects.filter(id__in=image_ids)
        return ImageSlimSerializer(
            images, many=True, context={"request": self.context["request"]}
        ).data

    def get_buyers(self, obj):
        buyer_ids = ProjectBuyerConnection.objects.filter(project=obj).values_list(
            "buyer_id", flat=True
        )
        buyers = Buyer.objects.filter(id__in=buyer_ids)
        return BuyerSlimSerializer(
            buyers, many=True, context={"request": self.context["request"]}
        ).data

    @transaction.atomic
    def create(self, validated_data):
        user = self.context["request"].user
        role = user.get_role()
        company_uid = validated_data.pop("company_uid", None)

        if role == CompanyUserRole.SUPER_ADMIN:
            company = Company.objects.filter(uid=company_uid).first()
            if company == None:
                raise serializers.ValidationError("Invalid company UID")
        else:
            company = user.get_company()

        image_uids = validated_data.pop("image_uids", [])
        buyer_uids = validated_data.pop("buyer_uids", [])

        project = Project.objects.create(
            company=company,
            **validated_data,
        )
        if image_uids:
            images = Image.objects.filter(uid__in=image_uids)
            ProjectImage.objects.bulk_create(
                [
                    ProjectImage(project=project, image=img, company=company)
                    for img in images
                ]
            )
        if buyer_uids:
            buyers = Buyer.objects.filter(uid__in=buyer_uids)
            ProjectBuyerConnection.objects.bulk_create(
                [
                    ProjectBuyerConnection(
                        project=project, buyer=buyer, company=company
                    )
                    for buyer in buyers
                ]
            )

        return project

    @transaction.atomic
    def update(self, instance, validated_data):
        image_uids = validated_data.pop("image_uids", None)
        buyer_uids = validated_data.pop("buyer_uids", None)
        company_uid = validated_data.pop("company_uid", None)
        if company_uid:
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
                [
                    ProjectImage(project=instance, image=img, company=company)
                    for img in images
                ]
            )
        if buyer_uids is not None:
            ProjectBuyerConnection.objects.filter(project=instance).delete()
            buyers = Buyer.objects.filter(uid__in=buyer_uids)
            ProjectBuyerConnection.objects.bulk_create(
                [
                    ProjectBuyerConnection(
                        project=instance, buyer=buyer, company=company
                    )
                    for buyer in buyers
                ]
            )

        return instance


class ProjectHistorySerializer(serializers.ModelSerializer):
    changed_by = serializers.SerializerMethodField()

    class Meta:
        model = Project.history.model
        fields = [
            "id",
            "name",
            "company",
            "started_at",
            "will_finish_at",
            "status",
            "history_id",
            "history_type",
            "history_date",
            "changed_by",
        ]

    def get_changed_by(self, obj):
        return UserSerializer(obj.history_user).data
