from rest_framework import serializers
from sita.models.process import Process


class ProcessSerializer(serializers.ModelSerializer):
    """
    Model serializer for Process information
    """

    class Meta:
        model = Process
        fields = (
            "process",
        )

