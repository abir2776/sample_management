from django.db import transaction
from rest_framework import serializers

from common.serializers import FileSlimSerializer
from sample_manager.models import Bucket, Drawer, DrawerFile, File


class DrawerSerializer(serializers.ModelSerializer):
    file_uids = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        max_length=3,
        allow_empty=True,
        required=False,
    )
    files = serializers.SerializerMethodField()
    bucket_uid = serializers.CharField()

    class Meta:
        model = Drawer
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
        files_ids = DrawerFile.objects.filter(sample=obj).values_list(
            "file_id", flat=True
        )
        files = File.objects.filter(id__in=files_ids)
        return FileSlimSerializer(files, many=True).data

    @transaction.atomic
    def create(self, validated_data):
        bucket_uid = validated_data.pop("bucket_uid")
        file_uids = validated_data.pop("file_uids", [])
        user = self.context["request"].user
        organization = user.get_organization()

        bucket = Bucket.objects.filter(uid=bucket_uid).first()
        if bucket is None:
            raise serializers.ValidationError("No bucket found with this given uid")

        files = File.objects.filter(uid__in=file_uids)
        drawer = Drawer.objects.create(
            bucket=bucket, created_by=user, organization=organization, **validated_data
        )

        drawer_files = [DrawerFile(drawer=drawer, file=f) for f in files]
        DrawerFile.objects.bulk_create(drawer_files)
        return drawer

    @transaction.atomic
    def update(self, instance, validated_data):
        bucket_uid = validated_data.pop("bucket_uid", None)
        file_uids = validated_data.pop("file_uids", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if bucket_uid:
            bucket = Bucket.objects.filter(uid=bucket_uid).first()
            if bucket is None:
                raise serializers.ValidationError("No bucket found with this given uid")
            instance.bucket = bucket

        instance.save()
        if file_uids is not None:
            DrawerFile.objects.filter(drawer=instance).delete()
            files = File.objects.filter(uid__in=file_uids)
            drawer_files = [DrawerFile(drawer=instance, file=f) for f in files]
            DrawerFile.objects.bulk_create(drawer_files)

        return instance
