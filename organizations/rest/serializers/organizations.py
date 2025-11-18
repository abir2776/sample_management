from rest_framework import serializers

from organizations.choices import OrganizationUserRole
from organizations.models import Organization, OrganizationUser


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"

    def create(self, validated_data):
        user = self.context["request"].user
        organization = Organization.objects.create(**validated_data)
        OrganizationUser.objects.create(
            user=user, organization=organization, role=OrganizationUserRole.OWNER
        )
        return organization
