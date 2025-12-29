from decimal import Decimal

from django.db import transaction
from rest_framework import serializers

from common.serializers import (
    BuyerSlimSerializer,
    ImageSlimSerializer,
    NoteSlimSerializer,
    ProjectSlimSerializer,
)
from organizations.choices import CompanyUserRole
from organizations.rest.serializers.users import UserSerializer
from sample_manager.choices import ActionTypes, SizeType, StorageType, WeightType
from sample_manager.models import (
    Buyer,
    GarmentSample,
    Image,
    ModifyRequest,
    Note,
    Project,
    ProjectSample,
    SampleBuyerConnection,
    SampleImage,
    SampleNote,
    Storage,
)
from sample_manager.rest.serializers.storage import StorageSerializer


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
    storage = StorageSerializer(read_only=True)

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
            "size_range",
            "types",
            "color",
            "size",
            "size_cen",
            "types",
            "comments",
            "company",
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
            "note_uids",
            "category",
            "sub_category",
            "notes",
        ]
        read_only_fields = [
            "storage",
            "size_cen",
            "id",
            "uid",
            "created_by",
            "company",
            "status",
            "storage",
        ]

    def get_images(self, obj):
        image_ids = SampleImage.objects.filter(sample=obj).values_list(
            "image_id", flat=True
        )
        images = Image.objects.filter(id__in=image_ids)
        return ImageSlimSerializer(
            images, many=True, context={"request": self.context["request"]}
        ).data

    def get_buyers(self, obj):
        buyer_ids = SampleBuyerConnection.objects.filter(sample=obj).values_list(
            "buyer_id", flat=True
        )
        buyers = Buyer.objects.filter(id__in=buyer_ids)
        return BuyerSlimSerializer(
            buyers, many=True, context={"request": self.context["request"]}
        ).data

    def get_projects(self, obj):
        project_ids = ProjectSample.objects.filter(sample=obj).values_list(
            "project_id", flat=True
        )
        projects = Project.objects.filter(id__in=project_ids)
        return ProjectSlimSerializer(
            projects, many=True, context={"request": self.context["request"]}
        ).data

    def get_notes(self, obj):
        note_ids = SampleNote.objects.filter(sample=obj).values_list(
            "note_id", flat=True
        )
        notes = Note.objects.filter(
            id__in=note_ids,
        )
        return NoteSlimSerializer(
            notes, many=True, context={"request": self.context["request"]}
        ).data

    def _prepare_request_data(
        self,
        validated_data,
        storage_uid,
        image_uids,
        buyer_uids,
        project_uids,
        note_uids,
    ):
        request_data = {}
        for key, value in validated_data.items():
            if hasattr(value, "isoformat"):
                request_data[key] = value.isoformat()
            elif isinstance(value, Decimal):
                request_data[key] = float(value)
            else:
                request_data[key] = value
        request_data["storage_uid"] = storage_uid
        request_data["image_uids"] = image_uids
        request_data["buyer_uids"] = buyer_uids
        request_data["project_uids"] = project_uids
        request_data["note_uids"] = note_uids

        return request_data

    @transaction.atomic
    def create(self, validated_data):
        storage_uid = validated_data.pop("storage_uid")
        image_uids = validated_data.pop("image_uids", [])
        buyer_uids = validated_data.pop("buyer_uids", [])
        project_uids = validated_data.pop("project_uids", [])
        note_uids = validated_data.pop("note_uids", [])
        weight_type = validated_data.get("weight_type")
        weight = validated_data.get("weight")
        size_type = validated_data.get("size_type")
        size = validated_data.get("size")

        user = self.context["request"].user
        company = user.get_company()
        images = Image.objects.filter(uid__in=image_uids)
        buyers = Buyer.objects.filter(uid__in=buyer_uids)
        projects = Project.objects.filter(uid__in=project_uids)
        notes = Note.objects.filter(uid__in=note_uids)

        if weight_type == WeightType.KG and weight is not None:
            validated_data["weight"] = Decimal(weight * 1000)

        if size_type == SizeType.CENTIMETER and size is not None:
            validated_data["size_cen"] = Decimal(str(size))

        storage = Storage.objects.filter(
            uid=storage_uid, type=StorageType.SPACE
        ).first()
        if storage is None:
            raise serializers.ValidationError("No Storage found with this given uid")
        if user.get_role() == CompanyUserRole.STAFF:
            validated_data["is_active"] = False

        sample = GarmentSample.objects.create(
            storage=storage,
            created_by=user,
            company=company,
            **validated_data,
        )
        SampleImage.objects.bulk_create(
            [SampleImage(sample=sample, image=img, company=company) for img in images]
        )
        SampleBuyerConnection.objects.bulk_create(
            [
                SampleBuyerConnection(sample=sample, buyer=buyer, company=company)
                for buyer in buyers
            ]
        )
        ProjectSample.objects.bulk_create(
            [
                ProjectSample(sample=sample, project=project, company=company)
                for project in projects
            ]
        )
        SampleNote.objects.bulk_create(
            [SampleNote(sample=sample, note=note, company=company) for note in notes]
        )
        if user.get_role() == CompanyUserRole.STAFF:
            request_data = self._prepare_request_data(
                validated_data,
                storage_uid,
                image_uids,
                buyer_uids,
                project_uids,
                note_uids,
            )

            ModifyRequest.objects.create(
                requested_user=user,
                company=company,
                sample=sample,
                requested_from=StorageType.SPACE,
                requested_action=ActionTypes.CREATE,
                requested_data=request_data,
                storage=storage,
            )

        return sample

    @transaction.atomic
    def update(self, instance, validated_data):
        storage_uid = validated_data.pop("storage_uid", None)
        image_uids = validated_data.pop("image_uids", None)
        buyer_uids = validated_data.pop("buyer_uids", None)
        project_uids = validated_data.pop("project_uids", None)
        note_uids = validated_data.pop("note_uids", None)

        weight_type = validated_data.get("weight_type")
        weight = validated_data.get("weight")
        size_type = validated_data.get("size_type")
        size = validated_data.get("size")

        if weight_type == WeightType.KG and weight is not None:
            validated_data["weight"] = Decimal(weight * 1000)

        if size_type == SizeType.CENTIMETER and size is not None:
            validated_data["size_cen"] = Decimal(str(size))

        user = self.context["request"].user
        company = user.get_company()
        if user.get_role() == CompanyUserRole.STAFF:
            update_data = validated_data.copy()

            request_data = self._prepare_request_data(
                update_data,
                storage_uid if storage_uid else instance.storage.uid,
                image_uids
                if image_uids is not None
                else list(
                    Image.objects.filter(
                        id__in=SampleImage.objects.filter(sample=instance).values_list(
                            "image_id", flat=True
                        )
                    ).values_list("uid", flat=True)
                ),
                buyer_uids
                if buyer_uids is not None
                else list(
                    Buyer.objects.filter(
                        id__in=SampleBuyerConnection.objects.filter(
                            sample=instance
                        ).values_list("buyer_id", flat=True)
                    ).values_list("uid", flat=True)
                ),
                project_uids
                if project_uids is not None
                else list(
                    Project.objects.filter(
                        id__in=ProjectSample.objects.filter(
                            sample=instance
                        ).values_list("project_id", flat=True)
                    ).values_list("uid", flat=True)
                ),
                note_uids
                if note_uids is not None
                else list(
                    Note.objects.filter(
                        id__in=SampleNote.objects.filter(sample=instance).values_list(
                            "note_id", flat=True
                        )
                    ).values_list("uid", flat=True)
                ),
            )

            ModifyRequest.objects.create(
                requested_user=user,
                company=company,
                sample=instance,
                requested_from=StorageType.SPACE,
                requested_action=ActionTypes.UPDATE,
                requested_data=request_data,
                storage=instance.storage,
            )
            return instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if storage_uid:
            storage = Storage.objects.filter(uid=storage_uid).first()
            if storage is None:
                raise serializers.ValidationError(
                    "No storage found with this given uid"
                )
            instance.storage = storage
        instance.save()
        if image_uids is not None:
            SampleImage.objects.filter(sample=instance, company=company).delete()
            images = Image.objects.filter(uid__in=image_uids)
            SampleImage.objects.bulk_create(
                [
                    SampleImage(sample=instance, image=img, company=company)
                    for img in images
                ]
            )
        if buyer_uids is not None:
            SampleBuyerConnection.objects.filter(sample=instance).delete()
            buyers = Buyer.objects.filter(uid__in=buyer_uids)
            SampleBuyerConnection.objects.bulk_create(
                [
                    SampleBuyerConnection(sample=instance, buyer=buyer, company=company)
                    for buyer in buyers
                ]
            )
        if project_uids is not None:
            ProjectSample.objects.filter(sample=instance).delete()
            projects = Project.objects.filter(uid__in=project_uids)
            ProjectSample.objects.bulk_create(
                [
                    ProjectSample(sample=instance, project=project, company=company)
                    for project in projects
                ]
            )
        if note_uids is not None:
            SampleNote.objects.filter(sample=instance).delete()
            notes = Note.objects.filter(uid__in=note_uids)
            SampleNote.objects.bulk_create(
                [
                    SampleNote(sample=instance, note=note, company=company)
                    for note in notes
                ]
            )

        return instance


class GarmentSampleHistorySerializer(serializers.ModelSerializer):
    changed_by = serializers.SerializerMethodField()

    class Meta:
        model = GarmentSample.history.model
        fields = [
            "id",
            "storage",
            "sample_id",
            "created_by",
            "arrival_date",
            "style_no",
            "sku_no",
            "item",
            "fabrication",
            "weight",
            "weight_type",
            "color",
            "size",
            "size_type",
            "types",
            "comments",
            "company",
            "name",
            "description",
            "status",
            "is_active",
            "history_id",
            "history_type",
            "history_date",
            "changed_by",
        ]

    def get_changed_by(self, obj):
        return UserSerializer(obj.history_user).data


class SampleUploadSerializer(serializers.Serializer):
    file = serializers.FileField(
        help_text="Excel file (.xlsx or .xls) containing garment samples"
    )
    storage_uid = serializers.CharField(
        max_length=255, help_text="UID of the storage space"
    )

    def validate_file(self, value):
        """Validate uploaded file is an Excel file"""
        if not value.name.endswith((".xlsx", ".xls")):
            raise serializers.ValidationError(
                "Invalid file format. Please upload an Excel file (.xlsx or .xls)"
            )
        return value


class SampleUploadResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    message = serializers.CharField()
    total_rows_processed = serializers.IntegerField()
    samples_created = serializers.IntegerField()
    samples_skipped = serializers.IntegerField()
    errors = serializers.IntegerField()
    unique_colors = serializers.ListField(child=serializers.CharField())
    error_details = serializers.ListField(child=serializers.DictField(), required=False)
