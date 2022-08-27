from rest_framework import serializers

from hub.models.assign_task import AssignTask


class AssignUserSerializer(serializers.Serializer):
    userName = serializers.CharField(max_length=100, required=True)
    selectedIncidents = serializers.ListField()

    class meta:
        model = AssignTask
        fields = (
            "userName",
            "selectedIncidents"
        )
