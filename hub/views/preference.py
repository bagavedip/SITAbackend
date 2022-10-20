import logging

from django.db import transaction
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from hub.models import Preference
from hub.models.perspective import Perspective
from hub.models.hub import Hub
from hub.serializers.perspective_grid_view import PerspectiveGridSerializer
from hub.services.perspective import PerspectiveService

logger = logging.getLogger(__name__)


class Preference(viewsets.GenricViewSet):

    def preference_input(self, request):
        try:
            logger.debug(f"Parsed request body {request.data}")
            login_user = request.user
            validated_data = request.data
            logger.debug(f"Data after validation {validated_data}")
            # user_preference = Preference.objects.get("")
            logger.debug("Database transaction started")
            with transaction.atomic():
                asset = PreferenceService.update_from_validated_data(login_user, validated_data)
            logger.debug("Database transaction finished")

            # response formatting
            response_data = {
                "message": "Preference Saved SuccessFully !",
                "status": "success"
            }
            return Response(response_data)
            pass
        except Exception as e:
            response_data = {
                "message": f"{e}",
                "status": "error"
            }