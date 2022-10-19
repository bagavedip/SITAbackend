import logging

from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from hub.models import Perspective
from hub.serializers.perspective_grid_view import PerspectiveGridSerializer
from hub.services.perspective import PerspectiveService

logger = logging.getLogger(__name__)


class PerspectiveViewSet(viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated]

    def perspective_master_dropdown(self, request):
        """
         Function for assign user for
        """
        logger.debug(f"Received request body {request.data}")
        response_data = PerspectiveService.perspective_dropdown_data()
        return Response(response_data, status=status.HTTP_201_CREATED)

    def perspective_grid_data(self, request):
        """
         Function for perspective_grid_data view.
        """
        logger.debug(f"Received request body {request.data}")

        response_obj = PerspectiveGridSerializer(request)

        data = PerspectiveService.perspective_grid(response_obj)

        return Response(response_obj.get_response(data), status=status.HTTP_201_CREATED)

    def add_perspective_record(self, request):
        try:
            logger.info("Validating data for Log In.")
            # serializer = PerspectiveSerializer(data=request.data)
            # serializer.is_valid(raise_exception=True)
            validated_data = request.data
            logger.info("Initiating Log in.")
            login_user = request.user
            with transaction.atomic():
                perspective = PerspectiveService.create_from_validated_data(login_user, validated_data)
            logger.debug("Database transaction finished")

            # response formatting
            response_data = {"id": perspective.pk}
            return Response({"message": f"perspective with {response_data} created successfully",
                            "status": status.HTTP_201_CREATED})
        except Exception as e:
            return Response({"message": f"{e}", "status": "failed to create perspective"})

    def edit_perspective_record_submit(self, request, *args, **kwargs):
        """
        Function which update asset information.
        """
        try:
            logger.debug(f"Parsed request body {request.data}")
            login_user = request.user
            validated_data = request.data
            logger.debug(f"Data after validation {validated_data}")

            # update asset and asset user information
            logger.debug("Database transaction started")
            with transaction.atomic():
                asset = PerspectiveService.update_from_validated_data(login_user, validated_data)
            logger.debug("Database transaction finished")

            # response formatting
            response_data = {
                "message": "Record Updated SuccessFully !",
                "status": "success"
            }
            return Response(response_data)
        except Exception as e:
            response_data = {
                "message": f"{e}",
                "status": "error"
            }
            return Response(response_data)

    def perspective_details_data(self, request):
        try:
            perspective_id = request.data.get("id")
            perspective = PerspectiveService.perspective_details_data(perspective_id)
            return Response(perspective, status=status.HTTP_200_OK)
        except Exception as e:
            response_data = f"{e}"
            return Response(response_data)

    def perspective_record_delete(self, request, *args, **kwargs):
        """[action to destory society]

        Args:
            request ([Request]): [Django Request instance]
        """
        try:
            login_user = request.user
            perspective_id = request.data.get("id")
            queryset = Perspective.objects.get(id=perspective_id)
            with transaction.atomic():
                PerspectiveService.delete(queryset)
                response_data = {
                    "message": f"Record {perspective_id} Deleted SuccessFully !",
                    "status": "success"
                }
            return Response(response_data)
        except Exception as e:
            response_data = {
                "message": f"{e}",
                "status": "error"
            }
            return Response(response_data)


