from rest_framework import serializers
from hub.models.entity import Entity


class EntitySerializer(serializers.ModelSerializer):
    """
    Model serializer for ITSM information
    """

    class Meta:
        model = Entity
        fields = (
            "entityname",
        )
        

