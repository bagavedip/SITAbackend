import logging
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from hub.constants.dataset import Dataset
from hub.models import ITSM
from hub.serializers.itsm import ITSMSerializer
from hub.serializers.oei_serializers import OeiSerializer
from hub.serializers.oei_ticket_details import TicketDetailsSerializer
from hub.services.itsm import ITSMService
import json
from collections import defaultdict as dd


logger = logging.getLogger(__name__)


class ITSMViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    queryset = ITSMService.get_queryset()

    def convert_data(self, dataset):
        if len(dataset) == 0:
            print("Empty Result set")
        else:
            keys = dataset[0].keys()
            key_var = ""
            nested_dict_str = "dd(list)"

            key_index = 0
            for key in keys:
                if key_index < len(keys) -1:
                    if key_index < len(keys) -2:
                        nested_dict_str = "dd(lambda: " + nested_dict_str + ")"
                    key_var = key_var + "[data.get('" + key + "')]"
                    key_index += 1

            nested_dict = eval(nested_dict_str)
            # sala = ITSM.objects.filter(sla_name=keys.).count()
            temp1 = "nested_dict" + key_var + ".append(data.get('events'))"
            # Note that variable name here has to be "data" as this is what is used to build the executable string above
            for data in dataset:
                exec(temp1)
            nested_dict = json.loads(json.dumps(nested_dict))
            return nested_dict

    def build(self, dictionary, depth, datasets):
        keys = dictionary.keys()
        print("tyring to add", str(keys), " at depth ", depth)
        datasets[depth]['labels'].extend(list(keys))
        depth += 1
        for key in keys:
            value = dictionary.get(key)
            if type(value) is dict:
                self.build(value, depth, datasets)

    def build_response(self, req_data, data):

        labels = req_data.get('filterOptions').get('headerFilters')
        labels.append(req_data.get('filterOptions').get('headerOption'))

        id = 1
        datasets = []
        for label in labels:
            ds = Dataset().init_response_dataset()
            ds['id'] = id
            ds['label'] = label
            id += 1
            datasets.append(ds)

        depth = 0
        self.build(data, depth, datasets)
        return datasets

    def calculate_events(self, data):
        last_event_count = 0
        for key, value in data.items():
            if type(value) is dict:
                last_event_count = self.calculate_events(value)
            else:
                last_event_count = last_event_count + value[0]
        return last_event_count

    def update_events(self, data):
        if data is not None:
            for key, value in data.items():
                events = self.calculate_events(value)
                data[key]['events'] = events

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

    def ticket_dropdown_data(self, request):
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

    def sla_dropdown_data(self, request):
        data = {
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
            }
        return Response(data, status=status.HTTP_201_CREATED)

    def oei_tickets(self, request):
        logger.debug(f"Received request body {request.data}")
        response_obj = TicketDetailsSerializer(request)
        data = ITSMService.get_tickets(response_obj)
        return Response(response_obj.get_response(data), status=status.HTTP_201_CREATED)

    def ticket_details(self, request):
        request_data = request.data
        ticket = request_data.get("requestId", None)
        queryset = ITSMService.asset_details(ticket)
        return Response(queryset, status=status.HTTP_201_CREATED)

    def oei_chart_data(self, request, **kwargs):
        logger.info("Validating data for Log In.")
        serializser = OeiSerializer(request)
        result = ITSMService.get_oei(serializser)
        hirarchial_data = self.convert_data(result)
        self.update_events(hirarchial_data)
        query_data = ITSM.objects.filter(CreatedTime__gte=serializser.start_date,
                                         Ending_time__lte=serializser.end_date).count()
        data = ITSM.objects.filter(CreatedTime__gte=serializser.start_date,
                                   Ending_time__lte=serializser.end_date, is_overdue='1').count()
        percentage = round((data*100)/query_data)
        total_ticket = query_data
        legends = []
        Compliance = percentage
        final_response = {
            "charFooter": {
                "label": "SLA  Compliance",
                "value": str((Compliance)) + "%",
                "valueFontColor": "green"
            },
            "legends": {
                "header": request.data.get('filterOptions').get('headerOption'),
                "items": legends
            },
            "doughnutlabel": {
                "labels": [
                    {
                        "text": "Tickets {total_ticket}".format(total_ticket=total_ticket),
                        "font": {
                            "size": "25"
                        },
                        "color": "black"
                    },
                ]
            },
            "datasets": serializser.datasets
        }
        return Response(final_response, status=status.HTTP_201_CREATED)

    