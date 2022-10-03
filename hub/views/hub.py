import logging

from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import json
from collections import defaultdict as dd

from hub.models.hub import Hub
from hub.serializers.hub_timeline import HubTimeline
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
        # ("tyring to add", str(keys), " at depth ", depth)
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
        """
         Function for Insights(Hub) Donut Chart
        """
        logger.debug(f"Received request body {request.data}")

        serializser = InsightsSerializer(request)
        result = HubService.get_insights(serializser)
        hirarchial_data = self.convert_data(result)
        self.update_events(hirarchial_data)
        incidents_high = serializser.donut_center['2. Alta'] if "2. Alta" in serializser.donut_center.keys() else 0
        incidents_medium = serializser.donut_center['3. Media'] if "3. Media" in serializser.donut_center.keys() else 0
        incidents_low = serializser.donut_center['4. Baja'] if "4. Baja" in serializser.donut_center.keys() else 0
        total_incidents = incidents_high + incidents_medium + incidents_low
        legends = []
        if total_incidents == 0:
            return Response(None, status=status.HTTP_201_CREATED)
        else:
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
        """
         Function for Insights grid view.
        """
        logger.debug(f"Received request body {request.data}")

        response_obj = TicketDetailsSerializer(request)

        data = TicketsService.get_tickets(response_obj)

        return Response(response_obj.get_response(data), status=status.HTTP_201_CREATED)

    def master_data(self, request):
        """
         Dropdown data of Insights grid view
        """
        logger.debug(f"Received request body {request.data}")

        response_obj = MasterDataSerialiser()

        data = MasterDataService.get_master_data(response_obj)

        asset_types = Hub.objects.values_list('asset_type').distinct()
        asset_dropdown = [{
                        "value": "Select",
                        "label": "Asset Type | Select"
                    }]
        geo = Hub.objects.all().values_list('location_name').distinct()
        geo_dropdown = [{
                        "value": "Select",
                        "label": "Geo | Select"
                    }]
        entities = Hub.objects.values_list('entity_name').distinct()
        entity_dropdown = [{
                        "value": "Select",
                        "label": "Entity | Select"
                    }]
        for asset_type in asset_types:
            new_asset = {
                "value":asset_type,
                "label":asset_type
            }
            
            asset_dropdown.append(new_asset)
        for geos in geo:
            new_geo = {
                "value":geos,
                "label":geos
            }
            geo_dropdown.append(new_geo)
        for entity in entities:
            new_entity = {
                "value":entity,
                "label":entity
            }
            entity_dropdown.append(new_entity)
        response = [
            {
                "id": "Asset Type",
                "dropdownoption": asset_dropdown
            },
            {
                "id": "Geo",
                "dropdownoption": geo_dropdown
            },
            {
                "id": "Entity",
                "dropdownoption": entity_dropdown
            }
        ]

        return Response(response, status=status.HTTP_201_CREATED)

    def asset_details(self, request):
        """
         Function to get ticket details at Insights.
        """
        request_data = request.data
        incident = request_data.get("incidentId", None)
        queryset = HubService.asset_details(incident)
        return Response(queryset, status=status.HTTP_201_CREATED)

    def assign_task(self, request):
        """
        Function which used for assign task
        to user.
        """
        logger.debug(f"Parsed request body {request.data}")
        # Validating incoming request body
        serializer = request.data
        # update comment in sla and ticket information
        logger.debug("Database transaction started")
        try:
            with transaction.atomic():
                selected_incidents = serializer.get("selectedIncidents")
                user = serializer.get("userName")
                comment = HubService.assign_user(selected_incidents, user)
            logger.debug("Database transaction finished")
            # response formatting
            response_data = {
                "msg": comment,
                "status": True
            }
            return Response(response_data)
        except UnboundLocalError:
            return Response({"error": "there is no such selectedIncidents."})

    def hub_timeline(self, request):
        """
         Timeline view for insights
        """
        serializser = HubTimeline(request)
        result = HubService.hub_timeline(serializser)
        return Response(result, status=status.HTTP_200_OK)

    def incident_comment(self, request):
        """
        Function which update comment information.
        """
        logger.debug(f"Parsed request body {request.data}")
        # Validating incoming request body
        serializer = request.data
        # update comment in sla and ticket information
        logger.debug("Database transaction started")
        try:
            with transaction.atomic():
                selected_incidents = serializer.get("selectedIncidents")
                comment = serializer.get("Comment")
                comment = HubService.incident_comment(selected_incidents, comment)
            logger.debug("Database transaction finished")
            # response formatting
            response_data = {
                "msg": comment,
                "status": True
            }
            return Response(response_data)
        except UnboundLocalError:
            return Response({"error": "there is no such selectedIncidents."})
        
    #This function will add Updates on any incident
    def add_update(self, request):
        logger.debug(f"Parsed request body {request.data}")

        # Validating incoming request body
        serializer = request.data

        # update comment in sla and ticket information
        logger.debug("Database transaction started")
        try:
            with transaction.atomic():
                soar_id = serializer.get("incident")
                update = serializer.get("update")
                update_by = serializer.get("update_by")
                updates = HubService.add_update(soar_id,update,update_by)
            logger.debug("Database transaction finished")

            # response formatting
            response_data = {
                "message": updates,
                "status": status.HTTP_201_CREATED
            }
            return Response(response_data)
        except UnboundLocalError:
            return Response({"error": "there is no such selectedIncidents."})
