from rest_framework import serializers
from hub.models.geolocations import GeoLocation


class GeoLocationSerializer(serializers.ModelSerializer):
    """
    Model serializer for Location information
    """

    class Meta:
        model = GeoLocation
        fields = (
            "location",
            "entity_id",
        )
