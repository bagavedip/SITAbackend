from rest_framework import serializers
from hub.models.assets import Assets


class AssetSerializer(serializers.ModelSerializer):
    """
    Model serializer for ITSM information
    """

    class Meta:
        model = Assets
        fields = (
            "AssetName",
            "AssetType",
            "Category",
            "criticality",
            "function_id",
        )
