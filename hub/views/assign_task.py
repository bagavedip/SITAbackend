import logging

from django.db import transaction, IntegrityError
from rest_framework import viewsets, status
from rest_framework.response import Response

from hub.serializers.assign_user import AssignUserSerializer
from hub.services.assign_task import AssignTaskService

logger = logging.getLogger(__name__)


class AssignTaskViewset(viewsets.GenericViewSet):

    def assign_user(self, request):
        try:
            serializer = AssignUserSerializer(data=request.data)
            print(serializer, "serializer")
            serializer.is_valid(raise_exception=True)
            validateddata = serializer.data
            with transaction.atomic():
                selectedIncidents = validateddata["selectedIncidents"]
                userName = validateddata["userName"]
                assign_user = AssignTaskService.assign_user(selectedIncidents, userName)
            logger.debug("Database transaction finished")
            # response formatting
            response_data = {
                "msg": "Comment added successfully !!",
                "status": True
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response("user already assign.")

