from rest_framework import serializers
from hub.models.itsm_data import ITSM


class ITSMSerializer(serializers.ModelSerializer):
    """
    Model serializer for ITSM information
    """

    class Meta:
        model = ITSM
        fields = (
            "RequestID","itsm_id","RequestType","Subject",
            "RequestStatus","CreatedTime","ServiceCategory",
            "Account","Priority","Technician",
            "Resolution",
        )
