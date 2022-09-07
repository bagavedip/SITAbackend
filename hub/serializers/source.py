from rest_framework import serializers
from .creadentials import CredentialSerializer
from hub.models.source_data import Source


class SourceSerializer(serializers.ModelSerializer):
    """
    Model serializer for Source information
    """
    credentials = serializers.ListField(
        child=CredentialSerializer(), allow_empty=False, min_length=1, max_length=5
    )
   
    class Meta:
        model = Source
        fields = (
            "name",
            "type",
            "credentials",
        )
