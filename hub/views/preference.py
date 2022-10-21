import logging

from django.db import transaction
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from hub.models.preference import Preference
from hub.models.perspective import Perspective
from hub.models.hub import Hub
from hub.serializers.perspective_grid_view import PerspectiveGridSerializer
from hub.services.perspective import PerspectiveService

from hub.services.preference import PreferenceService
from hub.serializers.preference import PreferenceSerializer
logger = logging.getLogger(__name__)


class PreferenceViewSet(viewsets.GenericViewSet):

    def preference_input(self, request):
        try:
            logger.debug(f"Parsed request body {request.data}")
            login_user = request.user
            serializer = PreferenceSerializer(data=request.data)
            if serializer.is_valid():
                print("serializer is saved")
                serializer.save()
            print("serializer is valid")

            print(serializer.data)
            print("inside the transaction")
            graph = serializer.get("graph")
            graph_name = serializer.get("graph_name")
            user_id = serializer.get("user_id")
            value= serializer.get("value")
            # asset = PreferenceService.preference_input(graph,graph_name, user_id,value)
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