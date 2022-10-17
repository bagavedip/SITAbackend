import logging

from django.db import transaction,IntegrityError
from rest_framework import viewsets,status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from hub.serializers.assign_user import AssignUserSerializer
from hub.services.assign_task import AssignTaskService
from hub.services.perspective import PerspectiveService

from hub.serializers.perspective_grid_data import PerspectiveSerializer

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
         Function created for perspective_grid_data view
        """
        logger.debug(f"Recieved request body {request.data}")

        response_obj = PerspectiveSerializer(request)

        data = PerspectiveService.perspective_grid_data(response_obj)

        perspective_grid_data = {
            "gridAddOn": {
                "showFirstColumnAsCheckbox": False,
                "showLastColumnAsAction": True
            },
            "gridHeader": [
                {
                    "key": "column1",
                    "headerText": "INCIDENT ID",
                    "isSorting": False,
                    "type": "TEXT",
                    "hideOnUI": True,
                    "dataDisplayLength": 0
                },
                {
                    "key": "column2",
                    "headerText": "Publish / Draft",
                    "isSorting": False,
                    "type": "TEXT",
                    "hideOnUI": False,
                    "dataDisplayLength": 0
                },
                {
                    "key": "column3",
                    "headerText": "PERSPECTIVE DATE",
                    "isSorting": True,
                    "type": "DATE",
                    "hideOnUI": False,
                    "dataDisplayLength": 0
                },
                {
                    "key": "column4",
                    "headerText": "PERSECTIVE TYPE",
                    "isSorting": True,
                    "type": "TEXT",
                    "hideOnUI": False,
                    "dataDisplayLength": 0
                },
                {
                    "key": "column5",
                    "headerText": "PERSPECTIVE  TITLE",
                    "isSorting": True,
                    "type": "TEXT",
                    "hideOnUI": False,
                    "dataDisplayLength": 200
                },
                {
                    "key": "column6",
                    "headerText": " STATUS",
                    "isSorting": True,
                    "type": "TEXT",
                    "hideOnUI": False,
                    "dataDisplayLength": 0
                },
                {
                    "key": "column7",
                    "headerText": "ACTION",
                    "isSorting": True,
                    "type": "TEXT",
                    "hideOnUI": False,
                    "dataDisplayLength": 0
                }
            ],
            "gridData": [
                {
                    "column1": "62adc39f7b7522fbb5dc86d6c",
                    "column2": "Publish",
                    "column3": "09.09.2022",
                    "column4": "Incident",
                    "column5": "Lorem apsum dolor sit amet, consectetur.",
                    "column6": "Confirmed",
                    "column7": "Notified"
                },
                {
                    "column1": "62bdc39f7b7522fbb5dc86d6c",
                    "column2": "Publish",
                    "column3": "11.09.2022",
                    "column4": "Pattern",
                    "column5": "Lorem zapsum dolor sit amet, consectetur.",
                    "column6": "Under investigation",
                    "column7": "Under investigation"
                },
                {
                    "column1": "62gdc39f7b7522fbb5dc86d6c",
                    "column2": "Publish",
                    "column3": "09.12.2022",
                    "column4": "Event",
                    "column5": "Lorem xapsum dolor sit amet, consectetur.",
                    "column6": "False positive",
                    "column7": "Contained"
                },
                {
                    "column1": "62pdc39f7b7522fbb5dc86d6c",
                    "column2": "Draft",
                    "column3": "09.19.2022",
                    "column4": "Incident",
                    "column5": "Lorem wapsum dolor sit amet, consectetur.",
                    "column6": "Confirmed",
                    "column7": "Notified"
                },
                {
                    "column1": "62pdc39f7b7522fbb5dc86d6c",
                    "column2": "Draft",
                    "column3": "09.19.2022",
                    "column4": "Incident",
                    "column5": "Lorem wapsum dolor sit amet, consectetur.",
                    "column6": "Confirmed",
                    "column7": "Notified"
                },
                {
                    "column1": "62pdc39f7b7522fbb5dc86d6c",
                    "column2": "Draft",
                    "column3": "09.19.2022",
                    "column4": "Incident",
                    "column5": "Lorem wapsum dolor sit amet, consectetur.",
                    "column6": "Confirmed",
                    "column7": "Notified"
                },
                {
                    "column1": "62pdc39f7b7522fbb5dc86d6c",
                    "column2": "Publish",
                    "column3": "09.19.2022",
                    "column4": "Incident",
                    "column5": "Lorem wapsum dolor sit amet, consectetur.",
                    "column6": "Confirmed",
                    "column7": "Notified"
                },
                {
                    "column1": "62pdc39f7b7522fbb5dc86d6c",
                    "column2": "Publish",
                    "column3": "09.19.2022",
                    "column4": "Incident",
                    "column5": "Lorem wapsum dolor sit amet, consectetur.",
                    "column6": "Confirmed",
                    "column7": "Notified"
                },
                {
                    "column1": "62pdc39f7b7522fbb5dc86d6c",
                    "column2": "Publish",
                    "column3": "09.19.2022",
                    "column4": "Incident",
                    "column5": "Lorem wapsum dolor sit amet, consectetur.",
                    "column6": "Confirmed",
                    "column7": "Notified"
                }
            ]
        }
        return Response(response_obj.get_response(data), status=status.HTTP_200_OK)

    def security_pulse_grid_data(self, request):
        response_data = {
            "gridAddOn" : {
                "showFirstColumnAsCheckbox" : False,
                "showLastColumnAsAction" : True
            },
            "gridHeader" : [
                {
                    "key" : "column1",
                    "headerText" : "INCIDENT ID",
                    "isSorting" : True,
                    "type" : "TEXT",
                    "hideOnUI" : True,
                    "dataDisplayLength" : 0
                },
                {
                    "key" : "column2",
                    "headerText" : "Publish / Draft",
                    "isSorting" : False,
                    "type" : "TEXT",
                    "hideOnUI" : False,
                    "dataDisplayLength" : 0
                },
                {
                    "key" : "column3",
                    "headerText" : "NEWSLETTER DATE",
                    "isSorting" : True,
                    "type" : "DATE",
                    "hideOnUI" : False,
                    "dataDisplayLength" : 0
                },
                {
                    "key" : "column4",
                    "headerText" : "TITLE",
                    "isSorting" : True,
                    "type" : "TEXT",
                    "hideOnUI" : False,
                    "dataDisplayLength" : 0
                },
                {
                    "key" : "column5",
                    "headerText" : "CRITICALITY",
                    "isSorting" : True,
                    "type" : "TEXT",
                    "hideOnUI" : False,
                    "dataDisplayLength" : 0
                },
                {
                    "key" : "column6",
                    "headerText" : "ASSET TYPE",
                    "isSorting" : True,
                    "type" : "TEXT",
                    "hideOnUI" : False,
                    "dataDisplayLength" : 0
                },
                {
                    "key" : "column7",
                    "headerText" : "ANALYST",
                    "isSorting" : False,
                    "type" : "TEXT",
                    "hideOnUI" : False,
                    "dataDisplayLength" : 0
                }
            ],
            "gridData" : [
                {
                    "column1" : "000000053",
                    "column2" : "Publish",
                    "column3" : "09.09.2022",
                    "column4" : "Lorem ipsum dolor sit amet, consectetur.",
                    "column5" : "High",
                    "column6" : "Laptop",
                    "column7" : "Suresh Kumar"
                },
                {
                    "column1" : "000000053",
                    "column2" : "Publish",
                    "column3" : "09.09.2022",
                    "column4" : "Lorem ipsum dolor sit amet, consectetur.",
                    "column5" : "Medium",
                    "column6" : "Mobile , Laptop",
                    "column7" : "Ram Kumar"
                },{
                    "column1" : "000000053",
                    "column2" : "Publish",
                    "column3" : "09.09.2022",
                    "column4" : "Lorem ipsum dolor sit amet, consectetur.",
                    "column5" : "Medium",
                    "column6" : "Laptop",
                    "column7" : "Suresh Kumar"
                },{
                    "column1" : "000000053",
                    "column2" : "Publish",
                    "column3" : "09.09.2022",
                    "column4" : "Lorem ipsum dolor sit amet, consectetur.",
                    "column5" : "Medium",
                    "column6" : "Laptop",
                    "column7" : "Suresh Kumar"
                },{
                    "column1" : "000000053",
                    "column2" : "Publish",
                    "column3" : "09.09.2022",
                    "column4" : "Lorem ipsum dolor sit amet, consectetur.",
                    "column5" : "Medium",
                    "column6" : "Laptop",
                    "column7" : "Suresh Kumar"
                },{
                    "column1" : "000000053",
                    "column2" : "Publish",
                    "column3" : "09.09.2022",
                    "column4" : "Lorem ipsum dolor sit amet, consectetur.",
                    "column5" : "Low",
                    "column6" : "Laptop",
                    "column7" : "Suresh Kumar"
                },{
                    "column1" : "000000053",
                    "column2" : "Publish",
                    "column3" : "09.09.2022",
                    "column4" : "Lorem ipsum dolor sit amet, consectetur.",
                    "column5" : "Low",
                    "column6" : "Laptop",
                    "column7" : "Suresh Kumar"
                },{
                    "column1" : "000000053",
                    "column2" : "Publish",
                    "column3" : "09.09.2022",
                    "column4" : "Lorem ipsum dolor sit amet, consectetur.",
                    "column5" : "Low",
                    "column6" : "Laptop",
                    "column7" : "Suresh Kumar"
                }
            ]
        }
        return Response(response_data, status=status.HTTP_200_OK)
