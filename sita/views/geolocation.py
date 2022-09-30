import csv
import codecs
import logging

from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models.geolocations import GeoLocation
from ..models.entity import Entity

from sita.serializers.geolocations import GeoLocationSerializer
from sita.services.assets import AssetService
from sita.services.functions import FunctionService
from sita.services.geolocations import GeoLocationService
from sita.services.itsm import ITSMService
from sita.services.siem import SIEMService
from sita.services.soar import SOARService

logger = logging.getLogger(__name__)


class GeoLocationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    serializer_class = GeoLocationSerializer

    def geo_locations(self, request):
        """
         function to get details of geo_location
        """
        logger.info(f"request data is {request.data}")
        queryset = GeoLocationService.get_queryset().select_related('entity_id')
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

    def single_geo_locations(self, request, location_id):
        """
         function to get details single record of geo_location
        """
        logger.info(f"request data is {request.data}")
        queryset = GeoLocationService.get_queryset().filter(id=location_id).select_related('entity_id')
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
        else:
            return Response({
                "Status": status.HTTP_404_NOT_FOUND,
                "Message": "Data not Found"
            })

    def offence_location(self, request):
        """
         function to get combine details of offence and location
        """
        logger.info(f"request data is {request.data}")
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
    def addlocation(self, request):
        """
         function to add location details
        """
        logger.info(f"request data is {request.data}")
        if request.method == 'POST':
            Serializer = self.serializer_class(data=request.data)
            data = {}
            if Serializer.is_valid():
                if not GeoLocationService.get_queryset().filter(location__iexact=request.data["location"]).exists():
                    entity_query = Entity.objects.get(entityname=request.data['entity_name'])
                    location_list = GeoLocation(
                        location=request.data["location"],
                        entity_id=entity_query
                    )
                    location_list.save()
                    data["Id"] = location_list.id
                    data['Location'] = location_list.location
                    data["Entity"] = location_list.entity_id.entityname
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
                            "Status": status.HTTP_400_BAD_REQUEST,
                            "Message": "Location allready Exist",
                        }
                    )
            else:
                data = Serializer.errors
                return Response(
                    {
                        "Status": status.HTTP_204_NO_CONTENT,
                        "Message": "Fill required data",
                        "Location_Details": data
                    }
                )

    @action(detail=False, methods=['POST'])
    def validate_location(self, request):
        """
         function to validate csv file of location
        """
        logger.info(f"request data is {request.data}")
        file = request.FILES.get("File")

        reader = csv.DictReader(codecs.iterdecode(file, "utf-8"), delimiter=",")
        data = list(reader)
        serializer = GeoLocationSerializer(data=data, many=True)
        if serializer.is_valid():
            return Response({
                "Status": status.HTTP_200_OK,
                "Message": "Validation Successful",
                "Data": data
            }
            )
        else:
            cate_data = serializer.errors
            return Response({
                "Status": status.HTTP_406_NOT_ACCEPTABLE,
                "Message": serializer.errors,
                "Data": cate_data
            }
            )

    @action(detail=False, methods=['POST'])
    def upload_location(self, request):
        """
         function to upload csv file of location
        """
        logger.info(f"request data is {request.data}")
        file = request.FILES.get("File")

        reader = csv.DictReader(codecs.iterdecode(file, "utf-8"), delimiter=",")
        data = list(reader)
        serializer = GeoLocationSerializer(data=data, many=True)
        if serializer.is_valid():
            location_list = []
            for row in serializer.data:
                entity_queryset = Entity.objects.get(entityname=row["entity_name"])
                location_list.append(
                    GeoLocation(
                        location=row["location"],
                        entity_id=entity_queryset,
                    )
                )
            GeoLocation.objects.bulk_create(location_list)

            return Response({
                "Status": status.HTTP_200_OK,
                "Message": "Successfully upload the data",
                "Data": data
            }
            )
        else:
            geo_data = serializer.errors
            return Response({
                "Status": status.HTTP_406_NOT_ACCEPTABLE,
                "Message": serializer.errors,
                "Data": geo_data
            }
            )

    @action(detail=False, methods=["put"])
    def update_location(self, request, location_id):
        """
         function to update details of location
        """
        logger.info(f"request data is {request.data}")
        serializer = GeoLocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            entity_query = Entity.objects.get(entityname=request.data["entity_name"])
            valid_data = {
                "location": request.data["location"],
                "entity_id": entity_query,
            }
            location_queryset = GeoLocationService.get_queryset().filter(id=location_id)
            if location_queryset:
                for data in location_queryset:
                    location = GeoLocationService.update(data, **valid_data)
                    data = {
                        "id": location.pk,
                        "Location Name": location.location,
                    }
                return Response({
                    "Status": status.HTTP_200_OK,
                    "Message": "Data Updated Successfully",
                    "Data": data
                })
            else:
                return Response({
                    "Status": status.HTTP_404_NOT_FOUND,
                    "Message": "Data not Founded for this id"
                })

    def location_delete(self, request, location_id):
        """
         function to delete details of location
        """
        logger.info(f"request data is {request.data}")
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
