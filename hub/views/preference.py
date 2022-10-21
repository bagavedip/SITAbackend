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
from django.db.models import Q

from hub.services.preference import PreferenceService
from hub.serializers.preference import PreferenceSerializer
logger = logging.getLogger(__name__)


class PreferenceViewSet(viewsets.GenericViewSet):

    def preference_input(self, request):
        try:
            logger.debug(f"Parsed request body {request.data}")
            user_id = request.user
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
            user_id = request.user
            validated_data = request.data
            ################
            # Get list of product ids of a particular order
            preference = Preference.objects.filter(Q(user_id=request.user.pk), Q(graph= request.data.get("graph")))
            user = Preference.objects.filter(user_id=request.user.pk)
            print(request.user.pk)
            print(preference)

            # Get products from list of product ids
            # products = Product.objects.filter(id__in=product_ids)
###################################################3
            response_data = {
                "message": "Preference fetched SuccessFully !",
                "graph": preference.get("graph"),
                "graph_name": preference.get("graph_name"),
                "value" : preference.get("value"),
                "status": "success"
            }
            return Response(response_data)
        except Exception as e:
            response_data = {
                "message": f"{e}",
                "status": "error"
            }
            return Response(response_data)
