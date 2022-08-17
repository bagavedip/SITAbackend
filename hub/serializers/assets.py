from rest_framework import serializers
from hub.models.assets import Assets


class AssetSerializer(serializers.ModelSerializer):
    """
    Model serializer for Asset information
    """
    category_name = serializers.CharField(source='category.category')
    function_name = serializers.CharField(source='function_id.function_name')

    class Meta:
        model = Assets
        fields = (
            "AssetName",
            "category_name",
            "criticality",
            "function_name",
        )
