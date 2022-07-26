from rest_framework import serializers
from hub.models.process import Process


class ProcessSerializer(serializers.ModelSerializer):
    """
    Model serializer for ITSM information
    """

    class Meta:
        model = Process
        fields = (
            "process",
        )

