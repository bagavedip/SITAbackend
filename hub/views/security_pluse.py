from rest_framework import viewsets,status
from rest_framework.response import Response

from SITAbackend.hub.models import SecurityPulse


class SecurityPluseDetailsViewset(viewsets.GenericViewSet):
    def security_pulse_details_data(self, request):
        try:
            security_pulse_id = request.data.get("id")
            security_pulse = SecurityPluseDetailsViewset.security_pulse_details_data(security_pulse_id)
            return Response(security_pulse)
        except Exception as e:
            response_data = f"{e}"
            return Response(response_data)
