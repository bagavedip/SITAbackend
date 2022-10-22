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
from django.core import serializers
import json
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
            ################ Q(graph= request.data.get("graph"))

            queryset = list(Preference.objects.filter(user_id=request.user.pk).all())
            print(request.user.pk)

            response_data=[]
            # queryset = serializers.serialize("json", Preference.objects.all())
            # print(queryset)
            # for filter in queryset:
            #     for value in filter:
            #         resopnse"graph": preference.get("graph"),
            #         "graph_name": preference.get("graph_name"),
            #         "value": preference.get("value"),
            # res = json.loads(queryset)
            response_data = [key for key,value in queryset.items()]
            # response_data = {
                # [
            #     # "message": "Preference fetched SuccessFully !",
            #     "oei":{
            #         "graph": preference.get("graph"),
            #         "graph_name": preference.get("graph_name"),
            #         "value": preference.get("value"),
            #     },
            #     "insights": {
            #         "graph": preference.get("graph"),
            #         "graph_name": preference.get("graph_name"),
            #         "value": preference.get("value"),
            #     },
            #     "perspective": {
            #         "graph": preference.get("graph"),
            #         "graph_name": preference.get("graph_name"),
            #         "value": preference.get("value"),
            #     },
            #     "location": {
            #         "graph": preference.get("graph"),
            #         "graph_name": preference.get("graph_name"),
            #         "value": preference.get("value"),
            #     },
            #     "status": "success"
            #
            # }
            return Response(response_data)
        except Exception as e:
            response_data = {
                "message": f"{e}",
                "status": "error"
            }
            return Response(response_data)
