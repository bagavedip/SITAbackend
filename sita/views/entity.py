import csv
import codecs
import logging

from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from sita.services.geolocations import GeoLocationService
from sita.services.functions import FunctionService
from sita.services.assets import AssetService
from sita.services.itsm import ITSMService
from sita.services.soar import SOARService
from sita.services.siem import SIEMService
from sita.serializers.entity import EntitySerializer
from sita.models.entity import Entity
from sita.services.entity import EntityService

logger = logging.getLogger(__name__)


class EntityViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = EntitySerializer

    # queryset = EntityService.get_queryset()

    def entities(self, request):
        """
         Function to get details of entity.
        """
        logger.info(f"request data is {request.data}")
        queryset = EntityService.get_queryset()
        dataset = []
        for entity in queryset:
            data = ({
                "id": entity.id,
                "entityname": entity.entityname
            })
            dataset.append(data)
        return Response(
            {
                "Status": status.HTTP_200_OK,
                "Data": dataset,
            }
        )

    def single_entities(self, request, entity_id):
        """
         Function to get details of single entity.
        """
        logger.info(f"request data is {request.data}")
        queryset = EntityService.get_queryset().filter(id=entity_id)
        dataset = []
        if queryset:
            for entity in queryset:
                data = ({
                    "id": entity.id,
                    "entityname": entity.entityname
                })
                dataset.append(data)
        return Response(
            {
                "Status": status.HTTP_200_OK,
                "Data": dataset,
            }
        )

    def offence_entity(self, request):
        """
         Function to get combine details of ofence and entity.
        """
        logger.info(f"request data is {request.data}")
        queryset = EntityService.get_queryset()
        entity_offences = dict()
        for entity in queryset.values():
            entity_offences[entity.get('entityname')] = 0
            location_data = GeoLocationService.location_filter(entity.get('id'))
            if location_data:
                for location in location_data.values():
                    function_data = FunctionService.function_filter(location.get('id'))
                    for functions in function_data.values():
                        asset_data = AssetService.asset_filter(functions.get('id'))
                        for asset_name in asset_data.values():
                            itsm_data = ITSMService.itsm_filter(asset_name.get('AssetName'))
                            for itsm in itsm_data.values():
                                soar_data = SOARService.soar_filter(itsm.get('Affair'))
                                for soar in soar_data.values():
                                    siem_data = SIEMService.siem_filter(soar.get('TicketIDs'))
                                    for siem in siem_data.values():
                                        entity_offences[entity.get('entityname')] = entity_offences.get(
                                            entity.get('entityname'), 0) + 1
        entity_offences['Total offence'] = sum(entity_offences.values())
        data = entity_offences

        return Response(
            {
                "Status": status.HTTP_200_OK,
                "Data": data,
            }
        )

    def offence_entity_asset_types(self, request):
        """
         Function is used to get combine details of offence entity and asset types
        """
        logger.info(f"request data is {request.data}")
        queryset = EntityService.get_queryset()
        entities = dict()
        for entity in queryset.values():
            location_data = GeoLocationService.location_filter(entity.get('id'))
            for location in location_data.values():
                function_data = FunctionService.function_filter(location.get('id'))
                for function in function_data.values():
                    asset_data = AssetService.asset_filter(function.get('id'))
                    asset_types = dict()
                    for asset_name in asset_data.values():
                        itsm_data = ITSMService.itsm_filter(asset_name.get('AssetName'))
                        for itsm in itsm_data.values():
                            soar_data = SOARService.soar_filter(itsm.get('Affair'))
                            for soar in soar_data.values():
                                siem_data = SIEMService.siem_filter(soar.get('TicketIDs'))
                                for siem in siem_data.values():
                                    asset_types[asset_name.get('AssetType')] = asset_types.get(
                                        asset_name.get('AssetType'), 0) + 1
                    assetsdata = asset_types
                    entities[entity.get('entityname')] = assetsdata
        data = entities
        return Response(
            {
                "Status": status.HTTP_200_OK,
                "Data": data,
            }
        )

    def offence_entity_location(self, request):
        """
         Function is used to get combine details of offence, entity, location
        """
        logger.info(f"request data is {request.data}")
        queryset = EntityService.get_queryset()
        entities = dict()
        for entity in queryset.values():
            location_data = GeoLocationService.location_filter(entity.get('id'))
            locations = dict()
            for location in location_data.values():
                function_data = FunctionService.function_filter(location.get('id'))
                for function in function_data.values():
                    asset_data = AssetService.asset_filter(function.get('id'))
                    for asset_name in asset_data.values():
                        itsm_data = ITSMService.itsm_filter(asset_name.get('AssetName'))
                        for itsm in itsm_data.values():
                            soar_data = SOARService.soar_filter(itsm.get('Affair'))
                            for soar in soar_data.values():
                                siem_data = SIEMService.siem_filter(soar.get('TicketIDs'))
                                for siem in siem_data.values():
                                    locations[location.get('location')] = locations.get(location.get('location'), 0) + 1
            locationsdata = locations
            entities[entity.get('entityname')] = locationsdata
        data = entities
        return Response(
            {
                "Status": status.HTTP_200_OK,
                "Data": data,
            }
        )

    def offence_entity_function(self, request):
        """
         Function is used to get combine details of offence, entity, functions
        """
        logger.info(f"request data is {request.data}")
        queryset = EntityService.get_queryset()
        entities = dict()
        for entity in queryset.values():
            location_data = GeoLocationService.location_filter(entity.get('id'))
            for location in location_data.values():
                function_data = FunctionService.function_filter(location.get('id'))
                functions = dict()
                for function in function_data.values():
                    asset_data = AssetService.asset_filter(function.get('id'))
                    for asset_name in asset_data.values():
                        itsm_data = ITSMService.itsm_filter(asset_name.get('AssetName'))
                        for itsm in itsm_data.values():
                            soar_data = SOARService.soar_filter(itsm.get('Affair'))
                            for soar in soar_data.values():
                                siem_data = SIEMService.siem_filter(soar.get('TicketIDs'))
                                for siem in siem_data.values():
                                    functions[function.get('function_name')] = functions.get(
                                        function.get('function_name'), 0) + 1
                functionsdata = functions
                entities[entity.get('entityname')] = functionsdata
        data = entities
        return Response(
            {
                "Status": status.HTTP_200_OK,
                "Data": data,
            }
        )

    def offence_entity_geo_asset_types(self, request):
        """
         Function is used to get combine details of offence, entity, Geo and asset_types
        """
        logger.info(f"request data is {request.data}")
        queryset = EntityService.get_queryset()
        entities = dict()
        for entity in queryset.values():
            location_data = GeoLocationService.location_filter(entity.get('id'))
            locations = dict()
            for location in location_data.values():
                function_data = FunctionService.function_filter(location.get('id'))
                for function in function_data.values():
                    asset_data = AssetService.asset_filter(function.get('id'))
                    asset_types = dict()
                    for asset_name in asset_data.values():
                        itsm_data = ITSMService.itsm_filter(asset_name.get('AssetName'))
                        for itsm in itsm_data.values():
                            soar_data = SOARService.soar_filter(itsm.get('Affair'))
                            for soar in soar_data.values():
                                siem_data = SIEMService.siem_filter(soar.get('TicketIDs'))
                                for siem in siem_data.values():
                                    asset_types[asset_name.get('AssetType')] = asset_types.get(
                                        asset_name.get('AssetType'), 0) + 1
                    assetsdata = asset_types
                    locations[location.get('location')] = assetsdata
            entities[entity.get('entityname')] = locations
        data = entities
        return Response(
            {
                "Status": status.HTTP_200_OK,
                "Data": data,
            }
        )

    def offence_entity_geo_function(self, request):
        """
         Function to get combine details of offence, entity, Geo and function
        """
        logger.info(f"request data is {request.data}")
        queryset = EntityService.get_queryset()
        entities = dict()
        for entity in queryset.values():
            location_data = GeoLocationService.location_filter(entity.get('id'))
            locations = dict()
            for location in location_data.values():
                function_data = FunctionService.function_filter(location.get('id'))
                functions = dict()
                for function in function_data.values():
                    asset_data = AssetService.asset_filter(function.get('id'))
                    for asset_name in asset_data.values():
                        itsm_data = ITSMService.itsm_filter(asset_name.get('AssetName'))
                        for itsm in itsm_data.values():
                            soar_data = SOARService.soar_filter(itsm.get('Affair'))
                            for soar in soar_data.values():
                                siem_data = SIEMService.siem_filter(soar.get('TicketIDs'))
                                for siem in siem_data.values():
                                    functions[function.get('function_name')] = functions.get(
                                        function.get('function_name'), 0) + 1
                functionsdata = functions
                locations[location.get('location')] = functionsdata
            entities[entity.get('entityname')] = locations
        data = entities
        return Response(
            {
                "Status": status.HTTP_200_OK,
                "Data": data,
            }
        )

    @action(detail=False, methods=["post"])
    def addentity(self, request):
        """
        Function to add entity details
        """
        logger.info(f"request data is {request.data}")
        if request.method == 'POST':
            Serializer = EntitySerializer(data=request.data)
            data = {}
            if Serializer.is_valid():
                if not EntityService.get_queryset().filter(entityname__iexact=request.data["entityname"]).exists():
                    entity = Serializer.save()
                    data["Id"] = entity.id
                    data['Entity'] = entity.entityname
                    return Response(
                        {
                            "Status": status.HTTP_200_OK,
                            "Message": "Entity Successfully Added",
                            "Process_details": data
                        }
                    )
                else:
                    return Response(
                        {
                            "Status": status.HTTP_400_BAD_REQUEST,
                            "Message": "Entity allready Exist",
                        }
                    )
            else:
                data = Serializer.errors
                return Response(
                    {
                        "Status": status.HTTP_204_NO_CONTENT,
                        "Message": "Fill required data",
                        "Entity_Details": data
                    }
                )

    @action(detail=False, methods=['POST'])
    def validate_entity(self, request):
        """
         Function to validate csv file of entity
        """
        logger.info(f"request data is {request.data}")
        file = request.FILES.get("File")

        reader = csv.DictReader(codecs.iterdecode(file, "utf-8"), delimiter=",")
        data = list(reader)
        serializer = EntitySerializer(data=data, many=True)
        if serializer.is_valid():
            return Response({
                "Status": status.HTTP_200_OK,
                "Message": "Validation Successful",
                "Data": data
            }
            )
        else:
            entity_err = serializer.errors
            return Response({
                "Status": status.HTTP_406_NOT_ACCEPTABLE,
                "Message": serializer.errors,
                "Data": entity_err
            }
            )

    @action(detail=False, methods=['POST'])
    def upload_entity(self, request):
        """
        Upload data from CSV, with validation.
        """
        logger.info(f"request data is {request.data}")
        file = request.FILES.get("File")

        reader = csv.DictReader(codecs.iterdecode(file, "utf-8"), delimiter=",")
        data = list(reader)
        serializer = EntitySerializer(data=data, many=True)
        if serializer.is_valid():
            entity_list = []
            for row in serializer.data:
                entity_list.append(
                    Entity(
                        entityname=row["entityname"],
                    )
                )
            Entity.objects.bulk_create(entity_list)

            return Response({
                "Status": status.HTTP_200_OK,
                "Message": "Successfully upload the data",
                "Data": data
            }
            )
        else:
            entity_err = serializer.errors
            return Response({
                "Status": status.HTTP_406_NOT_ACCEPTABLE,
                "Message": serializer.errors,
                "Data": entity_err
            }
            )

    @action(detail=False, methods=["put"])
    def update_entity(self, request, entity_id):
        """
            Function to update entity queryset
        """
        logger.info(f"request data is {request.data}")
        serializer = EntitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        with transaction.atomic():
            Entity_queryset = EntityService.get_queryset().filter(id=entity_id)
            for data in Entity_queryset:
                entity = EntityService.update(data, **validated_data)
                data = {
                    "id": entity.pk,
                    "Entity Name": entity.entityname,
                }
        return Response(data)

    def entity_delete(self, request, entity_id):
        """
         Function to delete entity
        """
        logger.info(f"request data is {request.data}")
        queryset = EntityService.get_queryset().filter(id=entity_id)
        if queryset:
            queryset.delete()
            message = f"Record deleted for id {entity_id}"
            Status = status.HTTP_200_OK
        else:
            message = f"Record not found for id {entity_id}"
            Status = status.HTTP_404_NOT_FOUND
        return Response(
            {
                "Status": Status,
                "Message": message
            })
