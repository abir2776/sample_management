from rest_framework import serializers


class ContactFormSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=True)
    email = serializers.EmailField(required=True)
    subject = serializers.CharField(max_length=500, required=True)
    message = serializers.CharField(required=True)

    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError(
                "Name must be at least 2 characters long."
            )
        return value.strip()

    def validate_message(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError(
                "Message must be at least 10 characters long."
            )
        return value.strip()
