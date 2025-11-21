from rest_framework import serializers

from sample_manager.models import Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"
        read_only_fields = ["id", "uid", "company", "created_by", "status", "file_name"]

    def create(self, validated_data):
        user = self.context["request"].user
        company = user.get_company()
        uploaded_image = validated_data.get("file")
        file_name = uploaded_image.name
        file = Image.objects.create(
            created_by=user, company=company, file_name=file_name, **validated_data
        )
        return file
