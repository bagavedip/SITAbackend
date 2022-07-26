from rest_framework import serializers


class credentialSerializer(serializers.Serializer):
    """Serializer class for credential seializer json field.
    """

    filename = serializers.CharField(max_length=100)
    path = serializers.CharField(max_length=100)
