from django.db import transaction
from rest_framework import serializers

from common.serializers import BuyerSlimSerializer, FileSlimSerializer
from sample_manager.models import (
    Buyer,
    File,
    Sample,
    SampleBuyerConnection,
    SampleFile,
    Storage,
)


class SampleSerializer(serializers.ModelSerializer):
    file_uids = serializers.ListField(
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
    files = serializers.SerializerMethodField()
    buyers = serializers.SerializerMethodField()
    storage_uid = serializers.CharField(write_only=True)

    class Meta:
        model = Sample
        fields = [
            "id",
            "uid",
            "date",
            "bucket",
            "created_by",
            "style_no",
            "sku_no",
            "item",
            "fabrication",
            "weight",
            "color",
            "size",
            "sample_type",
            "comments",
            "organization",
            "name",
            "description",
            "status",
            "file_uids",
            "files",
            "storage_uid",
            "buyer_uids",
            "buyers",
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
        files_ids = SampleFile.objects.filter(sample=obj).values_list(
            "file_id", flat=True
        )
        files = File.objects.filter(id__in=files_ids)
        return FileSlimSerializer(files, many=True).data

    def get_buyers(self, obj):
        buyer_ids = SampleBuyerConnection.objects.filter(sample=obj).values_list(
            "id", flat=True
        )
        buyers = Buyer.objects.filter(id__in=buyer_ids)
        return BuyerSlimSerializer(buyers, many=True).data

    @transaction.atomic
    def create(self, validated_data):
        storage_uid = validated_data.pop("storage_uid")
        file_uids = validated_data.pop("file_uids", [])
        buyer_uids = validated_data.pop("buyer_uids", [])
        user = self.context["request"].user
        organization = user.get_organization()

        bucket = Storage.objects.filter(uid=storage_uid).first()
        if bucket is None:
            raise serializers.ValidationError("No bucket found with this given uid")

        files = File.objects.filter(uid__in=file_uids)
        buyers = Buyer.objects.filter(uid__in=buyer_uids)

        sample = Sample.objects.create(
            bucket=bucket, created_by=user, organization=organization, **validated_data
        )

        sample_files = [SampleFile(sample=sample, file=f) for f in files]
        sample_buyer_connection = [
            SampleBuyerConnection(sample=sample, buyer=buyer) for buyer in buyers
        ]
        SampleFile.objects.bulk_create(sample_files)
        SampleBuyerConnection.objects.bulk_create(sample_buyer_connection)

        return sample

    @transaction.atomic
    def update(self, instance, validated_data):
        storage_uid = validated_data.pop("storage_uid", None)
        file_uids = validated_data.pop("file_uids", None)
        buyer_uids = validated_data.pop("buyer_uids", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if storage_uid:
            bucket = Storage.objects.filter(uid=storage_uid).first()
            if bucket is None:
                raise serializers.ValidationError("No bucket found with this given uid")
            instance.bucket = bucket

        instance.save()
        if file_uids is not None:
            SampleFile.objects.filter(sample=instance).delete()
            files = File.objects.filter(uid__in=file_uids)
            sample_files = [SampleFile(sample=instance, file=f) for f in files]
            SampleFile.objects.bulk_create(sample_files)
        if buyer_uids is not None:
            SampleBuyerConnection.objects.filter(sample=instance).delete()
            buyers = Buyer.objects.filter(uid__in=buyer_uids)
            sample_buyers = [
                SampleBuyerConnection(sample=instance, buyer=buyer) for buyer in buyers
            ]
            SampleBuyerConnection.objects.bulk_create(sample_buyers)

        return instance
