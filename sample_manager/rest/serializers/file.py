from decimal import Decimal

from django.db import transaction
from rest_framework import serializers

from common.serializers import BuyerSlimSerializer, ImageSlimSerializer
from organizations.choices import CompanyUserRole
from sample_manager.choices import ActionTypes, StorageType
from sample_manager.models import (
    Buyer,
    File,
    FileBuyerConnection,
    FileImage,
    FileNote,
    Image,
    ModifyRequest,
    Note,
    Project,
    ProjectFile,
    Storage,
)


class StorageFileSerializer(serializers.ModelSerializer):
    image_uids = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        max_length=10,
        allow_empty=True,
        required=False,
    )
    images = serializers.SerializerMethodField()

    note_uids = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        allow_empty=True,
        required=False,
    )
    notes = serializers.SerializerMethodField()

    project_uids = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        allow_empty=True,
        required=False,
    )
    projects = serializers.SerializerMethodField()

    buyer_uids = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        allow_empty=True,
        required=False,
    )
    buyers = serializers.SerializerMethodField()

    storage_uid = serializers.CharField(write_only=True)

    class Meta:
        model = File
        fields = [
            "id",
            "uid",
            "file_id",
            "created_by",
            "storage",
            "company",
            "name",
            "status",
            "comments",
            "image_uids",
            "images",
            "note_uids",
            "notes",
            "project_uids",
            "projects",
            "buyer_uids",
            "buyers",
            "storage_uid",
        ]
        read_only_fields = [
            "id",
            "uid",
            "created_by",
            "company",
            "storage",
            "status",
        ]

    def get_images(self, obj):
        image_ids = FileImage.objects.filter(file=obj).values_list(
            "image_id", flat=True
        )
        images = Image.objects.filter(id__in=image_ids)
        return ImageSlimSerializer(images, many=True).data

    def get_notes(self, obj):
        note_ids = FileNote.objects.filter(file=obj).values_list("note_id", flat=True)
        notes = Note.objects.filter(id__in=note_ids)
        return [{"uid": n.uid, "title": n.title, "text": n.text} for n in notes]

    def get_projects(self, obj):
        project_ids = ProjectFile.objects.filter(file=obj).values_list(
            "project_id", flat=True
        )
        projects = Project.objects.filter(id__in=project_ids)
        return [{"uid": p.uid, "name": p.name} for p in projects]

    def get_buyers(self, obj):
        buyer_ids = FileBuyerConnection.objects.filter(file=obj).values_list(
            "buyer_id", flat=True
        )
        buyers = Buyer.objects.filter(id__in=buyer_ids)
        return BuyerSlimSerializer(
            buyers, many=True, context={"request": self.context.get("request")}
        ).data

    def _prepare_request_data(
        self,
        validated_data,
        storage_uid,
        image_uids,
        note_uids,
        project_uids,
        buyer_uids,
    ):
        """Helper method to prepare JSON serializable request data"""
        request_data = {}

        # Handle primitive fields
        for key, value in validated_data.items():
            if hasattr(value, "isoformat"):
                request_data[key] = value.isoformat()
            elif isinstance(value, Decimal):
                request_data[key] = float(value)
            else:
                request_data[key] = value

        # Add UIDs instead of serialized objects
        request_data["storage_uid"] = storage_uid
        request_data["image_uids"] = image_uids
        request_data["note_uids"] = note_uids
        request_data["project_uids"] = project_uids
        request_data["buyer_uids"] = buyer_uids

        return request_data

    @transaction.atomic
    def create(self, validated_data):
        storage_uid = validated_data.pop("storage_uid")
        image_uids = validated_data.pop("image_uids", [])
        note_uids = validated_data.pop("note_uids", [])
        project_uids = validated_data.pop("project_uids", [])
        buyer_uids = validated_data.pop("buyer_uids", [])

        user = self.context["request"].user
        company = user.get_company()

        storage = Storage.objects.filter(
            uid=storage_uid, type=StorageType.DRAWER
        ).first()
        if storage is None:
            raise serializers.ValidationError("No storage found with given uid")

        # Set is_active to False for staff users
        if user.get_role() == CompanyUserRole.STAFF:
            validated_data["is_active"] = False

        file_obj = File.objects.create(
            storage=storage, created_by=user, company=company, **validated_data
        )

        images = Image.objects.filter(uid__in=image_uids)
        FileImage.objects.bulk_create(
            [FileImage(file=file_obj, image=img) for img in images]
        )

        notes = Note.objects.filter(uid__in=note_uids)
        FileNote.objects.bulk_create([FileNote(file=file_obj, note=n) for n in notes])

        projects = Project.objects.filter(uid__in=project_uids)
        ProjectFile.objects.bulk_create(
            [ProjectFile(file=file_obj, project=p) for p in projects]
        )

        buyers = Buyer.objects.filter(uid__in=buyer_uids)
        FileBuyerConnection.objects.bulk_create(
            [
                FileBuyerConnection(file=file_obj, buyer=buyer, company=company)
                for buyer in buyers
            ]
        )

        # Create ModifyRequest for staff users
        if user.get_role() == CompanyUserRole.STAFF:
            request_data = self._prepare_request_data(
                validated_data,
                storage_uid,
                image_uids,
                note_uids,
                project_uids,
                buyer_uids,
            )

            ModifyRequest.objects.create(
                requested_user=user,
                company=company,
                storage=storage,
                file=file_obj,
                requested_from=StorageType.DRAWER,
                requested_action=ActionTypes.CREATE,
                requested_data=request_data,
            )

        return file_obj

    @transaction.atomic
    def update(self, instance, validated_data):
        storage_uid = validated_data.pop("storage_uid", None)
        image_uids = validated_data.pop("image_uids", None)
        note_uids = validated_data.pop("note_uids", None)
        project_uids = validated_data.pop("project_uids", None)
        buyer_uids = validated_data.pop("buyer_uids", None)

        user = self.context["request"].user
        company = user.get_company()

        # If user is staff, create ModifyRequest instead of updating directly
        if user.get_role() == CompanyUserRole.STAFF:
            # Prepare request data with current values if not provided
            update_data = validated_data.copy()

            request_data = self._prepare_request_data(
                update_data,
                storage_uid if storage_uid else instance.storage.uid,
                image_uids
                if image_uids is not None
                else list(
                    Image.objects.filter(
                        id__in=FileImage.objects.filter(file=instance).values_list(
                            "image_id", flat=True
                        )
                    ).values_list("uid", flat=True)
                ),
                note_uids
                if note_uids is not None
                else list(
                    Note.objects.filter(
                        id__in=FileNote.objects.filter(file=instance).values_list(
                            "note_id", flat=True
                        )
                    ).values_list("uid", flat=True)
                ),
                project_uids
                if project_uids is not None
                else list(
                    Project.objects.filter(
                        id__in=ProjectFile.objects.filter(file=instance).values_list(
                            "project_id", flat=True
                        )
                    ).values_list("uid", flat=True)
                ),
                buyer_uids
                if buyer_uids is not None
                else list(
                    Buyer.objects.filter(
                        id__in=FileBuyerConnection.objects.filter(
                            file=instance
                        ).values_list("buyer_id", flat=True)
                    ).values_list("uid", flat=True)
                ),
            )

            ModifyRequest.objects.create(
                requested_user=user,
                company=company,
                storage=instance.storage,
                file=instance,
                requested_from=StorageType.DRAWER,
                requested_action=ActionTypes.UPDATE,
                requested_data=request_data,
            )

            # Return instance without modifications
            return instance

        # For non-staff users, update directly
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if storage_uid:
            storage = Storage.objects.filter(
                uid=storage_uid, type=StorageType.DRAWER
            ).first()
            if storage is None:
                raise serializers.ValidationError("No storage found with given uid")
            instance.storage = storage

        instance.save()

        if image_uids is not None:
            FileImage.objects.filter(file=instance).delete()
            images = Image.objects.filter(uid__in=image_uids)
            FileImage.objects.bulk_create(
                [FileImage(file=instance, image=img) for img in images]
            )

        if note_uids is not None:
            FileNote.objects.filter(file=instance).delete()
            notes = Note.objects.filter(uid__in=note_uids)
            FileNote.objects.bulk_create(
                [FileNote(file=instance, note=n) for n in notes]
            )

        if project_uids is not None:
            ProjectFile.objects.filter(file=instance).delete()
            projects = Project.objects.filter(uid__in=project_uids)
            ProjectFile.objects.bulk_create(
                [ProjectFile(file=instance, project=p) for p in projects]
            )

        if buyer_uids is not None:
            FileBuyerConnection.objects.filter(file=instance).delete()
            buyers = Buyer.objects.filter(uid__in=buyer_uids)
            FileBuyerConnection.objects.bulk_create(
                [
                    FileBuyerConnection(file=instance, buyer=buyer, company=company)
                    for buyer in buyers
                ]
            )

        return instance
