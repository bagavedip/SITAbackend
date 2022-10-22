import logging
from rest_framework import viewsets,status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from hub.serializers.security_pulse_grid import SecurityPulseGridSerializer
from hub.services.security_pulse import SecurityPulseService

logger = logging.getLogger(__name__)


class DashboardViewSet(viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated]

    def security_pulse_grid_data(self, request):
        logger.debug(f"Received request body {request.data}")

        response_obj = SecurityPulseGridSerializer(request)

        data = SecurityPulseService.security_pulse_grid(response_obj)
        return Response(response_obj.get_response(data), status=status.HTTP_200_OK)