import logging
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from hub.serializers.itsm import ITSMSerializer
from hub.serializers.masterdata import OeiMasterDataSerialiser
from hub.services.itsm import ITSMService


logger = logging.getLogger(__name__)


class ITSMViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    queryset = ITSMService.get_queryset()

    def request_modes(self, request):
        try:
            Total_modes = []
            for mode in self.queryset.values():
                    Total_modes.append(mode.get('Request_mode'))
            # Created blank dict, added asset_type wise count in blank dict
            mode_types = dict()  
            for modes in Total_modes:
                mode_types[modes] = mode_types.get(modes, 0) + 1
            # added total asset types in dict by using other asset type counts
            mode_types['Total Requests'] = sum(mode_types.values())
            data = mode_types
            return Response(
                {
                    "Status": "Success",
                    "Data": data
                }
            )
        except:
            return Response(
                {
                    "Status": "Failed",
                    "Message": "You Don't have data"
                }
            )
        
    def false_positives(self, request):
        false_positive = 0
        ITSM_data = ITSMService.get_queryset()
        if ITSM_data:
            for data in ITSM_data:
                if data.Application_Status == "False Positive":
                    false_positive += 1
            data = {
                "False Positives": false_positive,
            }
            return Response(
                {
                    "Status": "Success",
                    "Data": data
                }
            )
        else:
            return Response(
                {
                    "Status": "Failed",
                    "Message": "You Don't have any ITSM data"
                }
            )

    def get_ticket_id(self, request):
        query_params = request.query_params
        ticket = query_params.get("ticket_id", None)
        data = ITSMService.get_queryset().filter(SIEM_id=ticket)
        serializer = ITSMSerializer(data, many=True)
        logger.info("Successfully Fetch for ticket id.")
        return Response(serializer.data, status=status.HTTP_200_OK)

    def master_data(self, request):
        logger.debug(f"Received request body {request.data}")
        response = [
                {
                    "id": "Category ",
                    "dropdownoption": [
                        {
                            "value": "Select",
                            "label": "Category | Select"
                        },
                        {
                            "value": "Within SLA",
                            "label": "Category |Within SLA"
                        },
                        {
                            "value": "value2",
                            "label": "Category | value2"
                        },
                        {
                            "value": "value3",
                            "label": "Category | value3"
                        }
                    ]
                },
                {
                    "id": "Priority",
                    "dropdownoption": [
                        {
                            "value": "Select",
                            "label": "Priority | Select"
                        },
                        {
                            "value": "All",
                            "label": "Priority | All"
                        },
                        {
                            "label": " Priority | value2",
                            "value": "value2"
                        },
                        {
                            "label": "Priority | value3",
                            "value": "value3"
                        }
                    ]
                },
                {
                    "id": "Status",
                    "dropdownoption": [
                        {
                            "value": "Select",
                            "label": "Status | Select"
                        },
                        {
                            "label": "Status | All",
                            "value": "All"
                        },
                        {
                            "label": "Status | value2",
                            "value": "value2"
                        },
                        {
                            "label": "Status | value3",
                            "value": "value3"
                        }
                    ]
                }, {
                "id": "Service",
                "dropdownoption": [
                    {
                        "value": "Select",
                        "label": "Service | Select"
                    },
                    {
                        "label": "Service | SOC",
                        "value": "SOC"
                    },
                    {
                        "label": "Service | value2",
                        "value": "value2"
                    },
                    {
                        "label": "Service | value3",
                        "value": "value3"
                    }
                ]
            }, {
                "id": "Reopened %",
                "dropdownoption": [
                    {
                        "value": "Select",
                        "label": "Reopened % | Select"
                    },
                    {
                        "label": "Reopened % | All",
                        "value": "All"
                    },
                    {
                        "label": "Reopened % | value2",
                        "value": "value2"
                    },
                    {
                        "label": "Reopened % | value3",
                        "value": "value3"
                    }
                ]
            }, {
                "id": "First response Time",
                "dropdownoption": [
                    {
                        "value": "Select",
                        "label": "ORG | Select"
                    },
                    {
                        "label": "First response Time | All",
                        "value": "All"
                    },
                    {
                        "label": "First response Time | value2",
                        "value": "value2"
                    },
                    {
                        "label": "First response Time | value3",
                        "value": "value3"
                    }
                ]
            }
            ]

        return Response(response, status=status.HTTP_201_CREATED)

    