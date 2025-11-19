from django.db import transaction
from rest_framework import serializers

from common.serializers import FileSlimSerializer
from sample_manager.models import File, Storage, StorageFile, StorageFileFile


class StorageFileSerializer(serializers.ModelSerializer):
    file_uids = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        max_length=3,
        allow_empty=True,
        required=False,
    )
    files = serializers.SerializerMethodField()
    storage_uid = serializers.CharField(write_only=True)

    class Meta:
        model = StorageFile
        fields = [
            "id",
            "uid",
            "created_by",
            "date",
            "organization",
            "name",
            "description",
            "status",
            "file_uids",
            "files",
            "storage_uid",
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
        files_ids = StorageFileFile.objects.filter(sample=obj).values_list(
            "file_id", flat=True
        )
        files = File.objects.filter(id__in=files_ids)
        return FileSlimSerializer(files, many=True).data

    @transaction.atomic
    def create(self, validated_data):
        storage_uid = validated_data.pop("storage_uid")
        file_uids = validated_data.pop("file_uids", [])
        user = self.context["request"].user
        organization = user.get_organization()

        storage = Storage.objects.filter(uid=storage_uid).first()
        if storage is None:
            raise serializers.ValidationError("No Storage found with this given uid")

        files = File.objects.filter(uid__in=file_uids)
        storage_file = StorageFile.objects.create(
            storage=storage,
            created_by=user,
            organization=organization,
            **validated_data,
        )

        storage_files_files = [
            StorageFileFile(storage_file=storage_file, file=f) for f in files
        ]
        StorageFileFile.objects.bulk_create(storage_files_files)
        return storage_file

    @transaction.atomic
    def update(self, instance, validated_data):
        storage_uid = validated_data.pop("storage_uid", None)
        file_uids = validated_data.pop("file_uids", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if storage_uid:
            storage = Storage.objects.filter(uid=storage_uid).first()
            if storage is None:
                raise serializers.ValidationError(
                    "No Storage found with this given uid"
                )
            instance.storage = storage

        instance.save()
        if file_uids is not None:
            StorageFileFile.objects.filter(storage_file=instance).delete()
            files = File.objects.filter(uid__in=file_uids)
            storage_file_files = [
                StorageFileFile(storage_file=instance, file=f) for f in files
            ]
            StorageFileFile.objects.bulk_create(storage_file_files)

        return instance
