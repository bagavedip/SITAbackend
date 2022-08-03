import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
import json

from hub.services.hub import HubService
from hub.constants.dataset import Dataset
from hub.serializers.hub import InsightsSerializer
from hub.serializers.ticket_details import TicketDetailsSerializer
from hub.services.ticket import TicketsService

logger = logging.getLogger(__name__)


class InsightHub(viewsets.GenericViewSet):

    def convert_data(self, dataset):
        if len(dataset) == 0:
            pass
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
        for key, value in data.items():
            events = self.calculate_events(value)
            data[key]['events'] = events

    def insights_hub(self, request):
        logger.debug(f"Received request body {request.data}")

        serializser = InsightsSerializer(request)

        result = HubService.get_insights(serializser)

        hirarchial_data = self.convert_data(result)

        self.update_events(hirarchial_data)
        total_incidents = (
                serializser.donut_center['High'] + serializser.donut_center['Medium'] + serializser.donut_center['Low'])
        final_response = {
            "legends": {
                "header": request.data.get('filterOptions').get('headerOption'),
                "items": {}
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
                        "text": "High {high}".format(high=serializser.donut_center['High']),
                        "font": {
                            "size": "25"
                        },
                        "color": "red"
                    },
                    {
                        "text": "Medium {Medium}".format(Medium=serializser.donut_center['Medium']),
                        "font": {
                            "size": "25"
                        },
                        "color": "yellow"
                    },
                    {
                        "text": "Low {Low}".format(Low=serializser.donut_center['Low']),
                        "font": {
                            "size": "25"
                        },
                        "color": "green"
                    }
                ]
            },
            "datasets": serializser.datasets

        }

        return Response({"Response": final_response}, status=status.HTTP_201_CREATED)

    def insight_tickets(self, request):
        logger.debug(f"Received request body {request.data}")

        response_obj = TicketDetailsSerializer(request)

        data = TicketsService.get_tickets(response_obj)

        return Response({"Response": response_obj.get_response(data)}, status=status.HTTP_201_CREATED)
