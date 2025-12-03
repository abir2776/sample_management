from django.db import transaction
from rest_framework import serializers

from sample_manager.choices import ActionTypes, ModifyRequestStatus, StorageType
from sample_manager.models import (
    Buyer,
    FileBuyerConnection,
    FileImage,
    FileNote,
    Image,
    ModifyRequest,
    Note,
    Project,
    ProjectFile,
    ProjectSample,
    SampleBuyerConnection,
    SampleImage,
    SampleNote,
    Storage,
)


class ModifyRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModifyRequest
        fields = "__all__"
        read_only_fields = [
            "id",
            "uid",
            "requested_user",
            "responded_user",
            "company",
            "storage",
            "sample",
            "file",
            "requested_from",
            "requested_action",
            "requested_data",
        ]

    @transaction.atomic
    def update(self, instance, validated_data):
        status = validated_data.get("status")
        user = self.context["request"].user

        if status == ModifyRequestStatus.ACCEPTED:
            if instance.requested_action == ActionTypes.CREATE:
                if instance.requested_from == StorageType.SPACE:
                    instance.sample.is_active = True
                    instance.sample.save()
                elif instance.requested_from == StorageType.DRAWER:
                    instance.file.is_active = True
                    instance.file.save()

            elif instance.requested_action == ActionTypes.UPDATE:
                request_data = instance.requested_data

                if instance.requested_from == StorageType.SPACE:
                    sample = instance.sample
                    storage_uid = request_data.pop("storage_uid", None)
                    image_uids = request_data.pop("image_uids", None)
                    buyer_uids = request_data.pop("buyer_uids", None)
                    project_uids = request_data.pop("project_uids", None)
                    note_uids = request_data.pop("note_uids", None)
                    for attr, value in request_data.items():
                        if hasattr(sample, attr):
                            setattr(sample, attr, value)
                    if storage_uid:
                        storage = Storage.objects.filter(
                            uid=storage_uid, type=StorageType.SPACE
                        ).first()
                        if storage:
                            sample.storage = storage

                    sample.save()
                    if image_uids is not None:
                        SampleImage.objects.filter(sample=sample).delete()
                        images = Image.objects.filter(uid__in=image_uids)
                        SampleImage.objects.bulk_create(
                            [SampleImage(sample=sample, image=img) for img in images]
                        )
                    if buyer_uids is not None:
                        SampleBuyerConnection.objects.filter(sample=sample).delete()
                        buyers = Buyer.objects.filter(uid__in=buyer_uids)
                        SampleBuyerConnection.objects.bulk_create(
                            [
                                SampleBuyerConnection(sample=sample, buyer=buyer)
                                for buyer in buyers
                            ]
                        )
                    if project_uids is not None:
                        ProjectSample.objects.filter(sample=sample).delete()
                        projects = Project.objects.filter(uid__in=project_uids)
                        ProjectSample.objects.bulk_create(
                            [
                                ProjectSample(sample=sample, project=project)
                                for project in projects
                            ]
                        )
                    if note_uids is not None:
                        SampleNote.objects.filter(sample=sample).delete()
                        notes = Note.objects.filter(uid__in=note_uids)
                        SampleNote.objects.bulk_create(
                            [SampleNote(sample=sample, note=note) for note in notes]
                        )

                elif instance.requested_from == StorageType.DRAWER:
                    file_obj = instance.file
                    company = instance.company
                    storage_uid = request_data.pop("storage_uid", None)
                    image_uids = request_data.pop("image_uids", None)
                    note_uids = request_data.pop("note_uids", None)
                    project_uids = request_data.pop("project_uids", None)
                    buyer_uids = request_data.pop("buyer_uids", None)
                    for attr, value in request_data.items():
                        if hasattr(file_obj, attr):
                            setattr(file_obj, attr, value)
                    if storage_uid:
                        storage = Storage.objects.filter(
                            uid=storage_uid, type=StorageType.DRAWER
                        ).first()
                        if storage:
                            file_obj.storage = storage

                    file_obj.save()
                    if image_uids is not None:
                        FileImage.objects.filter(file=file_obj).delete()
                        images = Image.objects.filter(uid__in=image_uids)
                        FileImage.objects.bulk_create(
                            [FileImage(file=file_obj, image=img) for img in images]
                        )
                    if note_uids is not None:
                        FileNote.objects.filter(file=file_obj).delete()
                        notes = Note.objects.filter(uid__in=note_uids)
                        FileNote.objects.bulk_create(
                            [FileNote(file=file_obj, note=n) for n in notes]
                        )
                    if project_uids is not None:
                        ProjectFile.objects.filter(file=file_obj).delete()
                        projects = Project.objects.filter(uid__in=project_uids)
                        ProjectFile.objects.bulk_create(
                            [ProjectFile(file=file_obj, project=p) for p in projects]
                        )
                    if buyer_uids is not None:
                        FileBuyerConnection.objects.filter(file=file_obj).delete()
                        buyers = Buyer.objects.filter(uid__in=buyer_uids)
                        FileBuyerConnection.objects.bulk_create(
                            [
                                FileBuyerConnection(
                                    file=file_obj, buyer=buyer, company=company
                                )
                                for buyer in buyers
                            ]
                        )
            instance.responded_user = user

        return super().update(instance, validated_data)
