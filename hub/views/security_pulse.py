import logging

from django.db import transaction
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from hub.models import SecurityPulse
from hub.services.perspective import PerspectiveService
from hub.services.security_pulse import SecurityPulseService

logger = logging.getLogger(__name__)


class PerspectiveViewSet(viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated]

    def security_pulse_record_delete(self, request):
        """[action to destory society]

        Args:
            request ([Request]): [Django Request instance]
        """
        try:
            login_user = request.user
            security_pulse_id = request.data.get("id")
            queryset = SecurityPulse.objects.get(id=security_pulse_id)
            with transaction.atomic():
                PerspectiveService.delete(queryset)
                response_data = {
                    "message": f"Record {security_pulse_id} Deleted SuccessFully !",
                    "status": "success"
                }
            return Response(response_data)
        except Exception as e:
            response_data = {
                "message": "Error while deleting record",
                "status": "error"
            }
            return Response(response_data)
