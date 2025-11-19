from rest_framework import serializers

from sample_manager.models import Storage


class StorageSerializer(serializers.ModelSerializer):
    parent_uid = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Storage
        fields = "__all__"
        read_only_fields = ["id", "uid", "organization", "created_by", "parent"]

    def create(self, validated_data):
        parent_uid = validated_data.pop("parent_uid", None)
        user = self.context["request"].user
        organization = user.get_organization()
        parent = None
        if parent_uid:
            parent = Storage.objects.filter(uid=parent_uid).first()
            if not parent:
                raise serializers.ValidationError(
                    "No Storage found with this given uid"
                )

        bucket = Storage.objects.create(
            created_by=user, organization=organization, parent=parent, **validated_data
        )
        bucket.history._history_user = user
        bucket.save()
        return bucket

    def update(self, instance, validated_data):
        parent_uid = validated_data.pop("parent_uid", None)
        user = self.context["request"].user
        if parent_uid:
            parent = Storage.objects.filter(uid=parent_uid).first()
            if parent is None:
                raise serializers.ValidationError(
                    "No Storage found with this given uid"
                )

            instance.parent = parent

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.history._history_user = user
        instance.save()

        return instance
