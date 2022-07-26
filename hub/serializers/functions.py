from rest_framework import serializers
from hub.models.functions import Function


class FuctionSerializer(serializers.ModelSerializer):
    """
    Model serializer for ITSM information
    """

    class Meta:
        model = Function
        fields = (
            "function_name",
            "location_id",
        )
