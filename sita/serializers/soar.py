from rest_framework import serializers
from sita.models.soar_data import SOAR


class SOARSerializer(serializers.ModelSerializer):
    """
    Model serializer for SOAR information
    """

    class Meta:
        model = SOAR
        fields = (
            "SOAR_ID","AssignedUser","Title","Time",
            "Tags","Products","Incident",
            "Suspicious","Important","Ports",
            "Outcomes","Status","Environment","Priority",
            "Stage","TicketIDs","ClosingTime",
            "Sources","Reason","RootCause",
        )
