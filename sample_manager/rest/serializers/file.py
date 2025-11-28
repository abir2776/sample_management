from django.db import transaction
from rest_framework import serializers

from common.serializers import ImageSlimSerializer
from sample_manager.choices import StorageType
from sample_manager.models import (
    File,
    FileImage,
    FileNote,
    Image,
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
            "description",
            "status",
            "comments",
            "image_uids",
            "images",
            "note_uids",
            "notes",
            "project_uids",
            "projects",
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

    @transaction.atomic
    def create(self, validated_data):
        storage_uid = validated_data.pop("storage_uid")
        image_uids = validated_data.pop("image_uids", [])
        note_uids = validated_data.pop("note_uids", [])
        project_uids = validated_data.pop("project_uids", [])

        user = self.context["request"].user
        company = user.get_company()

        storage = Storage.objects.filter(
            uid=storage_uid, type=StorageType.DRAWER
        ).first()
        if storage is None:
            raise serializers.ValidationError("No storage found with given uid")

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

        return file_obj

    @transaction.atomic
    def update(self, instance, validated_data):
        storage_uid = validated_data.pop("storage_uid", None)
        image_uids = validated_data.pop("image_uids", None)
        note_uids = validated_data.pop("note_uids", None)
        project_uids = validated_data.pop("project_uids", None)
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

        return instance
