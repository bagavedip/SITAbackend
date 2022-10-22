import logging
from rest_framework import viewsets,status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from hub.serializers.dashboard_grid import DashboardGridGridSerializer
from hub.serializers.security_pulse_grid import SecurityPulseGridSerializer
from hub.services.dashboard import DashboardService

logger = logging.getLogger(__name__)


class DashboardViewSet(viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated]

    def dashboard_grid_data(self, request):
        """
         function to check last three record according last_updated date on
         dashboard
        """
        logger.debug(f"Received request body {request.data}")
        response_obj = DashboardGridGridSerializer(request)
        data = DashboardService.dashboard_grid_data(response_obj)
        return Response(response_obj.get_response(data), status=status.HTTP_200_OK)
