from rest_framework import serializers

from sample_manager.models import File


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ["id", "uid", "file", "file_name", "created_by", "status"]
        read_only_fields = ["id", "uid", "file_name", "created_by", "status"]

    def create(self, validated_data):
        user = self.context["request"].user
        uploaded_file = validated_data.get("file")
        file_name = uploaded_file.name
        file = File.objects.create(
            created_by=user, file_name=file_name, **validated_data
        )
        return file
