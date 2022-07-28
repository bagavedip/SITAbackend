from rest_framework import serializers
from hub.models.assets import Assets


class AssetSerializer(serializers.ModelSerializer):
    """
    Model serializer for ITSM information
    """
    AssetName = serializers.CharField(required=False, max_length=256)

    class Meta:
        model = Assets
        fields = (
            "AssetName",
            "AssetType",
            "Category",
            "criticality",
            "function_id",
        )
