import logging

from django.db import transaction
from rest_framework import viewsets
from rest_framework.response import Response
from hub.models.preference import Preference
from django.db.models import Q
import json
from hub.services.preference import PreferenceService
logger = logging.getLogger(__name__)


class PreferenceViewSet(viewsets.GenericViewSet):

    def preference_input(self, request):
        try:
            logger.debug(f"Parsed request body {request.data}")
            user_id = request.user.pk
            validated_data = request.data

            asset = PreferenceService.preference_input(user_id, validated_data)
            logger.debug("Database transaction finished")

            # response formatting
            response_data = {
                "message": "Preference Saved SuccessFully !",
                "status": "success"
            }
            return Response(response_data)
        except Exception as e:
            response_data = {
                "message": f"{e}",
                "status": "error"
            }
            return Response(response_data)

    def preference_fetch(self, request):
        try:
            logger.debug(f"Parsed request body {request.data}")

            queryset = Preference.objects.filter(user=request.user.pk).values("user_id","session")
            query = queryset[0]
            print(request.user.pk)

            return Response(query)
        except Exception as e:
            response_data = {
                "message": f"{e}",
                "status": "error"
            }
            return Response(response_data)
