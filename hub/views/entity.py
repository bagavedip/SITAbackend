from rest_framework import status, viewsets
from rest_framework.response import Response
from hub.services.geolocations import GeoLocationService
from hub.services.functions import FunctionService
from hub.services.assets import AssetService
from hub.services.itsm import ITSMService
from hub.services.soar import SOARService
from hub.services.siem import SIEMService
from hub.serializers.entity import EntitySerializer
from hub.services.entity import EntityService


class EntityViewSet(viewsets.ModelViewSet):

    serializer_class = EntitySerializer

    def entities(self, request):
        data = EntityService.get_queryset()
        if data:
            serializer = EntitySerializer(data, many=True)
        return Response(
            {
                "Status": status.HTTP_200_OK,
                "Data": serializer.data,
            }
        )

    def offence_entity(self, requset):
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
                                        entity_offences[entity.get('entityname')] = entity_offences.get(entity.get('entityname'), 0) + 1
        entity_offences['Total offence'] = sum(entity_offences.values())
        data = entity_offences

        return Response(
            {
                "Status": status.HTTP_200_OK,
                "Data": data,
            }
        )

    def offence_entity_asset_types(self, request):
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
                                    asset_types[asset_name.get('AssetType')] = asset_types.get(asset_name.get('AssetType'), 0) + 1
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
                                    functions[function.get('function_name')] = functions.get(function.get('function_name'), 0) + 1
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
                                    asset_types[asset_name.get('AssetType')] = asset_types.get(asset_name.get('AssetType'), 0) + 1
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
                                    functions[function.get('function_name')] = functions.get(function.get('function_name'), 0) + 1
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
