from rest_framework import serializers
from hub.models.category import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Model serializer for Category information
    """

    class Meta:
        model = Category
        fields = (
            "category",
        )
