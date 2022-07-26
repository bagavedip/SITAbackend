from rest_framework import viewsets
from rest_framework.response import Response
from hub.serializers.geolocations import GeoLocationSerializer
from hub.services.geolocations import GeoLocationService
from hub.services.functions import FunctionService
from hub.services.assets import AssetService
from hub.services.itsm import ITSMService
from hub.services.soar import SOARService
from hub.services.siem import SIEMService


class GeoLocationViewSet(viewsets.ModelViewSet):

    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    
    serializer_class = GeoLocationSerializer

    def geo_locations(self, request):
        data = GeoLocationService.get_queryset()
        if data:
            serializer = self.serializer_class(data, many = True)
        return Response(
            {
                "Status": "Success",
                "Data": serializer.data,
            }
        )        

    def offence_location(self, request):
        queryset = GeoLocationService.get_queryset()
        location_offences = dict()
        for location in queryset.values():
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
                                location_offences[location.get('location')] = (
                                    location_offences.get(location.get('location'), 0) + 1)
        location_offences['Total offence'] = sum(location_offences.values())
        data = location_offences
        return Response({
            "Status": "Success",
            "Data": data,
        }
        )
