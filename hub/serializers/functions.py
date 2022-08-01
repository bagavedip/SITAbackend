from rest_framework import serializers
from hub.models.functions import Function


class FunctionSerializer(serializers.ModelSerializer):
    """
    Model serializer for function information
    """

    class Meta:
        model = Function
        fields = (
            "function_name",
            "location_id",
        )
