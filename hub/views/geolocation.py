from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from hub.serializers.geolocations import GeoLocationSerializer
from hub.services.geolocations import GeoLocationService
from hub.services.functions import FunctionService
from hub.services.assets import AssetService
from hub.services.itsm import ITSMService
from hub.services.soar import SOARService
from hub.services.siem import SIEMService


class GeoLocationViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    
    serializer_class = GeoLocationSerializer
    queryset = GeoLocationService.get_queryset()

    def geo_locations(self, request):
        queryset = GeoLocationService.get_queryset().select_related('entity_id')
        if queryset:
            dataset = []
            for location in queryset:
                data = {
                    "id": location.id,
                    "location": location.location,
                    "entity": location.entity_id.entityname,
                }
                dataset.append(data)
        return Response(
            {
                "Status": "Success",
                "Data": dataset,
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

    @action(detail=False, methods=["post"])
    def addlocation(self, request,**kwargs):
        if request.method == 'POST':
            Serializer = self.serializer_class(data=request.data)
            data = {}
            if Serializer.is_valid():
                if not self.queryset.filter(location=request.data["location"]).exists():
                    location = Serializer.save()
                    data["Id"] = location.id
                    data['Location'] = location.location
                    data["Entity"] = location.entity_id.entityname
                    return Response(
                        {
                            "Status": status.HTTP_200_OK,
                            "Message": "Location Successfully Added",
                            "Process_details": data
                        }
                    )
                else:
                    return Response(
                        {
                            "Status":status.HTTP_400_BAD_REQUEST,
                            "Message": "Location allready Exist",
                        }
                    )
            else:
                data = Serializer.errors
                return Response(
                    {
                        "Status":status.HTTP_204_NO_CONTENT,
                        "Message": "Fill required data",
                        "Location_Details" : data
                    }
                )

    @action(detail=False, methods=["put"])
    def update_location(self, request, location_id):
        """
            Function to update asset queryset
        """
        serializer = GeoLocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        with transaction.atomic():
            location_queryset = GeoLocationService.get_queryset().filter(id=location_id)
            if location_queryset:
                for data in location_queryset:
                    location = GeoLocationService.update(data, **validated_data)
                    data = {
                        "id": location.pk,
                        "Location Name": location.location,
                    }
                return Response(
                    {
                        "Status": status.HTTP_200_OK,
                        "Message": "",
                        "Data": data
                    })
            else:
                return Response(
                    {
                        "Status": status.HTTP_404_NOT_FOUND,
                        "Message": "Data not not found"
                    })

    def location_delete(self, request, location_id):
        queryset = GeoLocationService.get_queryset().filter(id=location_id)
        if queryset:
            queryset.delete()
            message = f"Record deleted for id {location_id}"
            Status = status.HTTP_200_OK
        else:
            message = f"Record not found for id {location_id}"
            Status = status.HTTP_404_NOT_FOUND
        return Response(
            {
                "Status": Status,
                "Message": message
            })
