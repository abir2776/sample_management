from rest_framework import serializers

from organizations.rest.serializers.users import UserSerializer
from sample_manager.models import Storage


class StorageSerializer(serializers.ModelSerializer):
    parent_uid = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Storage
        fields = "__all__"
        read_only_fields = ["id", "uid", "company", "created_by", "parent"]

    def create(self, validated_data):
        parent_uid = validated_data.pop("parent_uid", None)
        user = self.context["request"].user
        company = user.get_company()
        parent = None
        if parent_uid:
            parent = Storage.objects.filter(uid=parent_uid).first()
            if not parent:
                raise serializers.ValidationError(
                    "No Storage found with this given uid"
                )

        storage = Storage.objects.create(
            created_by=user, company=company, parent=parent, **validated_data
        )
        return storage

    def update(self, instance, validated_data):
        parent_uid = validated_data.pop("parent_uid", None)
        if parent_uid:
            parent = Storage.objects.filter(uid=parent_uid).first()
            if parent is None:
                raise serializers.ValidationError(
                    "No Storage found with this given uid"
                )

            instance.parent = parent

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class StorageHistorySerializer(serializers.ModelSerializer):
    changed_by = serializers.SerializerMethodField()

    class Meta:
        model = Storage.history.model
        fields = [
            "id",
            "company",
            "created_by",
            "name",
            "description",
            "parent",
            "status",
            "type",
            "image",
            "history_id",
            "history_type",
            "history_date",
            "changed_by",
        ]

    def get_changed_by(self, obj):
        return UserSerializer(obj.history_user).data
