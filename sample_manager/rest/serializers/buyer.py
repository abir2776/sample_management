from rest_framework import serializers

from sample_manager.models import Buyer


class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = "__all__"
        read_only_fields = ["id", "uid", "created_by", "organization", "status"]

    def create(self, validated_data):
        user = self.context["request"].user
        company = user.get_company()
        buyer = Buyer.objects.create(company=company, created_by=user, **validated_data)
        buyer.history._history_user = user
        buyer.save()
        return buyer
