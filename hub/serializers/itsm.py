from rest_framework import serializers
from hub.models.itsm_data import ITSM


class ITSMSerializer(serializers.ModelSerializer):
    """
    Model serializer for ITSM information
    """

    class Meta:
        model = ITSM
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    """
    Model serializer for ITSM information
    """

    selectedIncidents = serializers.CharField(max_length=100, required=True)
    Comment = serializers.CharField(max_length=100, allow_null=True)

    class Meta:
        model = ITSM
        fields = (
            "SIEM_id",
            "comment")
