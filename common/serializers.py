from rest_framework import serializers

from sample_manager.models import Buyer, Image, Note, Project


class ImageSlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class BuyerSlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = "__all__"


class ProjectSlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class NoteSlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"
