import logging
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import json

from rest_framework_simplejwt.authentication import JWTAuthentication

from hub.services.insight_hub_service import HubService
from hub.constants.dataset import Dataset
from hub.serializers.hub import InsightsSerializer
from hub.serializers.ticket_details import TicketDetailsSerializer
from hub.serializers.masterdata import MasterDataSerialiser
from hub.services.tickets_service import TicketsService
from hub.services.masterdata import MasterDataService

logger = logging.getLogger(__name__)


class InsightHub(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    def convert_data(self, dataset):
        if len(dataset) == 0:
            print("Empty Result set")
        else:
            keys = dataset[0].keys()
            key_var = ""
            nested_dict_str = "dd(list)"

            key_index = 0
            for key in keys:
                if key_index < len(keys) - 1:
                    if key_index < len(keys) - 2:
                        nested_dict_str = "dd(lambda: " + nested_dict_str + ")"
                    key_var = key_var + "[data.get('" + key + "')]"
                    key_index += 1

            nested_dict = eval(nested_dict_str)

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

    def insights_hub(self, request):
        logger.debug(f"Received request body {request.data}")

        serializser = InsightsSerializer(request)

        result = HubService.get_insights(serializser)

        hirarchial_data = self.convert_data(result)

        self.update_events(hirarchial_data)
        incidents_high = serializser.donut_center['High'] if "High" in serializser.donut_center.keys() else 0
        incidents_medium = serializser.donut_center['Medium'] if "Medium" in serializser.donut_center.keys() else 0
        incidents_low = serializser.donut_center['Low'] if "Low" in serializser.donut_center.keys() else 0
        total_incidents = incidents_high + incidents_medium + incidents_low
        print(serializser.donut_center)

        # legends = HubService.get_legends(serializser)
        legends = []

        final_response = {
            "legends": {
                "header": request.data.get('filterOptions').get('headerOption'),
                "items": legends
            },
            "doughnutlabel": {
                "labels": [
                    {
                        "text": "Incidents {total_incidents}".format(total_incidents=total_incidents),
                        "font": {
                            "size": "25"
                        },
                        "color": "black"
                    },
                    {
                        "text": "High {high}".format(high=incidents_high),
                        "font": {
                            "size": "25"
                        },
                        "color": "red"
                    },
                    {
                        "text": "Medium {Medium}".format(Medium=incidents_medium),
                        "font": {
                            "size": "25"
                        },
                        "color": "yellow"
                    },
                    {
                        "text": "Low {Low}".format(Low=incidents_low),
                        "font": {
                            "size": "25"
                        },
                        "color": "green"
                    }
                ]
            },
            "datasets": serializser.datasets

        }

        return Response(final_response, status=status.HTTP_201_CREATED)

    def insight_tickets(self, request):
        logger.debug(f"Received request body {request.data}")

        response_obj = TicketDetailsSerializer(request)

        data = TicketsService.get_tickets(response_obj)

        print('Sending Response', data)

        return Response(response_obj.get_response(data), status=status.HTTP_201_CREATED)

    def master_data(self, request):
        logger.debug(f"Received request body {request.data}")

        response_obj = MasterDataSerialiser()

        data = MasterDataService.get_master_data(response_obj)

        print('Sending Response', data)

        response = [
            {
                "id": "Asset Type",
                "dropdownoption": [
                    {
                        "value": "Select",
                        "label": "Asset Type | Select"
                    },
                    {
                        "value": "Email",
                        "label": "Asset Type | Email"
                    },
                    {
                        "value": "value2",
                        "label": "Asset Type | value2"
                    },
                    {
                        "value": "value3",
                        "label": "Asset Type | value3"
                    }
                ]
            },
            {
                "id": "Geography",
                "dropdownoption": [
                    {
                        "value": "Select",
                        "label": "Geography | Select"
                    },
                    {
                        "label": "Geography | USA Central",
                        "value": "USA Central"
                    },
                    {
                        "label": " Geography | value2",
                        "value": "value2"
                    },
                    {
                        "label": "Geography | value3",
                        "value": "value3"
                    }
                ]
            },
            {
                "id": "ORG",
                "dropdownoption": [
                    {
                        "value": "Select",
                        "label": "ORG | Select"
                    },
                    {
                        "label": "ORG | SUV22",
                        "value": "SUV22"
                    },
                    {
                        "label": "ORG | value2",
                        "value": "value2"
                    },
                    {
                        "label": "ORG | value3",
                        "value": "value3"
                    }
                ]
            }
        ]

        return Response(response, status=status.HTTP_201_CREATED)

    def asset_details(self, request):
        request_param = request.query_params.dict()
        incident = request_param.get("incident", None)
        print(incident)
        queryset = HubService.asset_details(incident)
        print(f"{queryset}queryset")

        return Response(queryset, status=status.HTTP_201_CREATED)

