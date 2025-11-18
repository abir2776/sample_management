from rest_framework import serializers

from sample_manager.models import Buyer, File


class FileSlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"


class BuyerSlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = "__all__"
