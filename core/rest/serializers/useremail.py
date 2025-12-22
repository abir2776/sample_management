from rest_framework import serializers


class ContactFormSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=True)
    email = serializers.EmailField(required=True)
    subject = serializers.CharField(max_length=500, required=True)
    message = serializers.CharField(required=True)
    phone = serializers.CharField(required=False)
    to_email = serializers.CharField(required=True)
