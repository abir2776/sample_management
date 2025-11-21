from django.db import transaction
from rest_framework import serializers

from common.serializers import (
    BuyerSlimSerializer,
    ImageSlimSerializer,
    NoteSlimSerializer,
    ProjectSlimSerializer,
)
from sample_manager.choices import StorageType
from sample_manager.models import (
    Buyer,
    GarmentSample,
    Image,
    Note,
    Project,
    ProjectSample,
    SampleBuyerConnection,
    SampleImage,
    SampleNote,
    Storage,
)


class SampleSerializer(serializers.ModelSerializer):
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
        allow_empty=True,
        required=False,
    )
    project_uids = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        allow_empty=True,
        required=False,
    )
    note_uids = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        allow_empty=True,
        required=False,
    )
    images = serializers.SerializerMethodField()
    buyers = serializers.SerializerMethodField()
    projects = serializers.SerializerMethodField()
    notes = serializers.SerializerMethodField()
    storage_uid = serializers.CharField(write_only=True)

    class Meta:
        model = GarmentSample
        fields = [
            "id",
            "uid",
            "arrival_date",
            "storage",
            "storage_id",
            "created_by",
            "style_no",
            "sku_no",
            "item",
            "fabrication",
            "weight",
            "weight_type",
            "size_type",
            "types",
            "color",
            "size",
            "type",
            "comments",
            "organization",
            "name",
            "description",
            "status",
            "image_uids",
            "images",
            "storage_uid",
            "buyer_uids",
            "buyers",
            "project_uids",
            "projects",
        ]
        read_only_fields = [
            "bucket",
            "id",
            "uid",
            "created_by",
            "organization",
            "status",
        ]

    def get_files(self, obj):
        image_ids = SampleImage.objects.filter(sample=obj).values_list(
            "file_id", flat=True
        )
        images = Image.objects.filter(id__in=image_ids)
        return ImageSlimSerializer(images, many=True).data

    def get_buyers(self, obj):
        buyer_ids = SampleBuyerConnection.objects.filter(sample=obj).values_list(
            "id", flat=True
        )
        buyers = Buyer.objects.filter(id__in=buyer_ids)
        return BuyerSlimSerializer(buyers, many=True).data

    def get_projects(self, obj):
        project_ids = ProjectSample.objects.filter(sample=obj).values_list(
            "project_id", flat=True
        )
        projects = Project.objects.filter(id__in=project_ids)
        return ProjectSlimSerializer(projects, many=True).data

    def get_notes(self, obj):
        note_ids = SampleNote.objects.filter(sample=obj).values_list(
            "note_id", flat=True
        )
        notes = Note.objects.filter(id__in=note_ids)
        return NoteSlimSerializer(notes, many=True).data

    @transaction.atomic
    def create(self, validated_data):
        storage_uid = validated_data.pop("storage_uid")
        image_uids = validated_data.pop("image_uids", [])
        buyer_uids = validated_data.pop("buyer_uids", [])
        project_uids = validated_data.pop("project_uids", [])
        note_uids = validated_data.pop("note_uids", [])

        user = self.context["request"].user
        company = user.get_company()

        storage = Storage.objects.filter(
            uid=storage_uid, type=StorageType.SPACE
        ).first()
        if storage is None:
            raise serializers.ValidationError("No Storage found with this given uid")

        # Main sample creation
        sample = GarmentSample.objects.create(
            storage=storage,
            created_by=user,
            company=company,
            **validated_data,
        )

        # Images
        images = Image.objects.filter(uid__in=image_uids)
        SampleImage.objects.bulk_create(
            [SampleImage(sample=sample, image=img) for img in images]
        )

        # Buyers
        buyers = Buyer.objects.filter(uid__in=buyer_uids)
        SampleBuyerConnection.objects.bulk_create(
            [SampleBuyerConnection(sample=sample, buyer=buyer) for buyer in buyers]
        )

        # Projects
        projects = Project.objects.filter(uid__in=project_uids)
        ProjectSample.objects.bulk_create(
            [ProjectSample(sample=sample, project=project) for project in projects]
        )

        # Notes
        notes = Note.objects.filter(uid__in=note_uids)
        SampleNote.objects.bulk_create(
            [SampleNote(sample=sample, note=note) for note in notes]
        )

        return sample

    @transaction.atomic
    def update(self, instance, validated_data):
        storage_uid = validated_data.pop("storage_uid", None)
        image_uids = validated_data.pop("image_uids", None)
        buyer_uids = validated_data.pop("buyer_uids", None)
        project_uids = validated_data.pop("project_uids", None)
        note_uids = validated_data.pop("note_uids", None)

        # Update primitive fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Update storage
        if storage_uid:
            storage = Storage.objects.filter(uid=storage_uid).first()
            if storage is None:
                raise serializers.ValidationError(
                    "No storage found with this given uid"
                )
            instance.storage = storage

        instance.save()

        # Update images
        if image_uids is not None:
            SampleImage.objects.filter(sample=instance).delete()
            images = Image.objects.filter(uid__in=image_uids)
            SampleImage.objects.bulk_create(
                [SampleImage(sample=instance, image=img) for img in images]
            )

        # Update buyers
        if buyer_uids is not None:
            SampleBuyerConnection.objects.filter(sample=instance).delete()
            buyers = Buyer.objects.filter(uid__in=buyer_uids)
            SampleBuyerConnection.objects.bulk_create(
                [
                    SampleBuyerConnection(sample=instance, buyer=buyer)
                    for buyer in buyers
                ]
            )

        # Update projects
        if project_uids is not None:
            ProjectSample.objects.filter(sample=instance).delete()
            projects = Project.objects.filter(uid__in=project_uids)
            ProjectSample.objects.bulk_create(
                [
                    ProjectSample(sample=instance, project=project)
                    for project in projects
                ]
            )

        # Update notes
        if note_uids is not None:
            SampleNote.objects.filter(sample=instance).delete()
            notes = Note.objects.filter(uid__in=note_uids)
            SampleNote.objects.bulk_create(
                [SampleNote(sample=instance, note=note) for note in notes]
            )

        return instance
