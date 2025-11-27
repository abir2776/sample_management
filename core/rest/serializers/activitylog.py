from rest_framework import serializers

from organizations.models import ActivityLog


class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = "__all__"
        read_only_fields = ["id", "uid", "user", "company"]

    def create(self, validated_data):
        user = self.context["request"].user
        company = user.get_company()
        return ActivityLog.objects.create(user=user, company=company, **validated_data)
