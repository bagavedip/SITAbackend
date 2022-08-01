from rest_framework import serializers
from hub.models.assets import Assets


class AssetSerializer(serializers.ModelSerializer):
    """
    Model serializer for Asset information
    """

    class Meta:
        model = Assets
        fields = (
            "AssetName",
            "category",
            "criticality",
            "function_id",
        )
