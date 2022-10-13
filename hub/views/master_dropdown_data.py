import logging

from django.db import transaction, IntegrityError
from rest_framework import viewsets, status
from rest_framework.response import Response

from hub.serializers.assign_user import AssignUserSerializer
from hub.services.assign_task import AssignTaskService

logger = logging.getLogger(__name__)


class MasterDropdownViewset(viewsets.GenericViewSet):

    def master_dropdown_data(self, request):
        """
         Function for assign user for selected incident
         in grid views.
        """
    
        # response formatting
        response_data = {
      "id": "PerspectiveType",
      "dropdownoption": [
        {
          "label": "Prospective Type",		
          "value": "Select"
        },
        {
          "label": "Incident",		
          "value": "Incident"
        },
        {
          "label": "Pattern",		
          "value": "Pattern"
        }
      ]
    },
   
    {
      "id": "ActionTaken",
      "dropdownoption": [
        {
          "label": "Action Taken",		
          "value": "Select"
        },
        {
          "label": "Notified",
          "value": "Notified"
        },
        {
          "label": "Under investigation",
          "value": "UnderInvestigation"
        },
        {
          "label": "Contained",
          "value": "Contained"
        },
        {
          "label": "Closed by Etek",
          "value": "ClosedByEtek"
        },
        {
          "label": "Closed by client",
          "value": "ClosedByClient"
        },
		{
          "label": "No action",
          "value": "NoAction"
        }
      ]
    },
    {
      "id": "Status",
      "dropdownoption": [
        {
          "value": "Select",
          "label": "Status"
        },
        {
          "label": "Confirmed",
          "value": "Confirmed"
        },
        {
          "label": "Under investigation",
          "value": "UnderInvestigation"
        },
        {
          "label": "False positive",
          "value": "FalsePositive"
        }
      ]
    }

    return Response(response_data, status=status.HTTP_201_CREATED)
