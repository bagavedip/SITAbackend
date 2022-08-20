import csv
import codecs
from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models.geolocations import GeoLocation
from ..models.functions import Function
from hub.serializers.functions import FunctionSerializer
from hub.services.functions import FunctionService
from hub.services.geolocations import GeoLocationService
from hub.services.assets import AssetService
from hub.services.itsm import ITSMService
from hub.services.soar import SOARService
from hub.services.siem import SIEMService


class FunctionViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = FunctionSerializer

    # queryset = FunctionService.get_queryset()

    def function(self, request, *args, **kwargs):
        queryset = FunctionService.get_queryset()
        dataset = []
        for functions in queryset:
            data = ({
                "Function_id": functions.id,
                "Function_name": functions.function_name,
                "Location_id": functions.location_id.id,
                "Location": functions.location_id.location
            })
            dataset.append(data)
        return Response(
            {
                "Status": status.HTTP_200_OK,
                "Data": dataset,
            }
        )

    def single_function_details(self, request, function_id):
        queryset = FunctionService.get_queryset().filter(id=function_id)
        if queryset:
            queryset_details = []
            for functions in queryset:
                query_data = ({
                    "Function_id": functions.id,
                    "Function_name": functions.function_name,
                    "Location_id": functions.location_id.id,
                    "Location": functions.location_id.location
                })
                queryset_details.append(query_data)

            return Response(
                {
                    "Status": status.HTTP_200_OK,
                    "Data": queryset_details
                }
            )
        else:
            return Response({
                "Status": status.HTTP_404_NOT_FOUND,
                "Message": "Data Not Existing"
            }
            )

    @action(detail=False, methods=['POST'])
    def validate_function_csv(self, request):
        # """Upload data from CSV, with validation."""
        file = request.FILES.get("File")
        # df = pd.read_csv(file)
        # new_df = df.isnull()
        # print(new_df)

        reader = csv.DictReader(codecs.iterdecode(file, "utf-8"), delimiter=",")
        data = list(reader)
        # print(data)
        cate_data = {}
        serializer = FunctionSerializer(data=data, many=True)
        # print(serializer)
        if serializer.is_valid():
            # print(data)
            return Response({
                "Status": status.HTTP_200_OK,
                "Message": "Validation Successful",
                "Data": data
            }
            )
        else:
            # print("failed")
            cate_data = serializer.errors
            return Response({
                "Status": status.HTTP_406_NOT_ACCEPTABLE,
                "Message": serializer.errors,
                "Data": cate_data
            }
            )

    @action(detail=False, methods=['POST'])
    def upload_function(self, request):
        """Upload data from CSV, with validation."""
        file = request.FILES.get("File")

        reader = csv.DictReader(codecs.iterdecode(file, "utf-8"), delimiter=",")
        data = list(reader)
        # print(data)
        cate_data = {}
        serializer = FunctionSerializer(data=data, many=True)
        # print(serializer)
        if serializer.is_valid():
            function_list = []
            for row in serializer.data:
                location_queryset = GeoLocation.objects.get(location=row["location_name"])
                # print(location_queryset)
                function_list.append(
                    Function(
                        function_name=row["function_name"],
                        location_id=location_queryset,
                    )
                )
            # print(function_list)
            Function.objects.bulk_create(function_list)

            return Response({
                "Status": status.HTTP_200_OK,
                "Message": "Successfully upload the data",
                "Data": data
            }
            )
        else:
            cate_data = serializer.errors
            print(cate_data)
            return Response({
                "Status": status.HTTP_406_NOT_ACCEPTABLE,
                "Message": serializer.errors,
                "Data": cate_data
            }
            )

    def functionlocationentity(self, request):
        try:
            id = request.query_params["id"]
            if id != None:
                queryset = FunctionService.get_queryset().select_related('location_id',
                                                                         'location_id__entity_id').filter(id=id)
                dataset = []
                for functions in queryset:
                    data = ({
                        "Function_id": functions.id,
                        "Function_name": functions.function_name,
                        "Location_id": functions.location_id.id,
                        "Location": functions.location_id.location,
                        "Entity_id": functions.location_id.entity_id.id,
                        "Entity": functions.location_id.entity_id.entityname,
                    })
                    dataset.append(data)
                return Response(
                    {
                        "Status": status.HTTP_200_OK,
                        "Data": dataset,
                    }
                )
            else:
                return Response(
                    {
                        "Status": status.HTTP_400_BAD_REQUEST,
                        "Message": "Please Provide an Id",
                    }
                )
        except:
            queryset = FunctionService.get_queryset().select_related('location_id', 'location_id__entity_id')
            dataset = []
            for functions in queryset:
                data = ({
                    "Function_id": functions.id,
                    "Function_name": functions.function_name,
                    "Location_id": functions.location_id.id,
                    "Location": functions.location_id.location,
                    "Entity_id": functions.location_id.entity_id.id,
                    "Entity": functions.location_id.entity_id.entityname,
                })
                dataset.append(data)
            return Response(
                {
                    "Status": status.HTTP_200_OK,
                    "Data": dataset,
                }
            )

    def function_asset(self, request):
        function_data = FunctionService.get_queryset()
        all_records = []
        function_asset = dict()
        for function in function_data.values():
            asset_data = AssetService.asset_filter(function.get('id'))
            for data in asset_data.values():
                function_asset[function.get('function_name')] = function_asset.get(function.get('function_name'), 0) + 1
        function_asset['Total asset'] = sum(function_asset.values())
        data = function_asset

        return Response(
            {
                "Status": status.HTTP_200_OK,
                "Data": data,
            }
        )

    def offence_function(self, request):
        queryset = FunctionService.get_queryset()
        function_offences = dict()
        for functions in queryset.values():
            asset_data = AssetService.asset_filter(functions.get('id'))
            for asset_name in asset_data.values():
                itsm_data = ITSMService.itsm_filter(asset_name.get('AssetName'))
                for itsm in itsm_data.values():
                    soar_data = SOARService.soar_filter(itsm.get('Affair'))
                    for soar in soar_data.values():
                        siem_data = SIEMService.siem_filter(soar.get('TicketIDs'))
                        for siem in siem_data.values():
                            function_offences[functions.get('function_name')] = function_offences.get(
                                functions.get('function_name'), 0) + 1
        function_offences['Total offence'] = sum(function_offences.values())
        data = function_offences
        return Response(
            {
                "Status": status.HTTP_200_OK,
                "Data": data,
            }
        )

    @action(detail=False, methods=["put"])
    def update_function(self, request, function_id):
        """
            Function to update asset queryset
        """
        serializer = FunctionSerializer(data=request.data)
        # print(request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        # print(validated_data)
        with transaction.atomic():
            location_queryset = GeoLocation.objects.get(location=request.data["location_name"])
            # print(category_queryset)
            valid_data = {
                "function_name": request.data["function_name"],
                "location_id": location_queryset,
            }

            Function_queryset = FunctionService.get_queryset().filter(id=function_id)
            for data in Function_queryset:
                # location_query = GeoLocation.objects.get(location = request.data["location_name"])

                function = FunctionService.update(data, **valid_data)
                data = {
                    "id": function.pk,
                    "Function Name": function.function_name,
                }
        return Response(data)

    def function_delete(self, request, function_id):
        queryset = FunctionService.get_queryset().filter(id=function_id)
        if queryset:
            queryset.delete()
            message = f"Record deleted for id {function_id}"
            Status = status.HTTP_200_OK
        else:
            message = f"Record not found for id {function_id}"
            Status = status.HTTP_404_NOT_FOUND
        return Response(
            {
                "Status": Status,
                "Message": message
            })

    @action(detail=False, methods=["post"])
    def addfunction(self, request, **kwargs):
        if request.method == 'POST':
            Serializer = self.serializer_class(data=request.data)
            data = {}
            if Serializer.is_valid():
                if not FunctionService.get_queryset().filter(function_name__iexact=request.data["function_name"]).exists():
                    location_queryset = GeoLocation.objects.get(location=request.data["location_name"])
                    function_list = Function(
                        function_name=request.data["function_name"],
                        location_id=location_queryset
                    )
                    function_list.save()
                    data["Id"] = function_list.id
                    data['Function'] = function_list.function_name
                    data['Location'] = function_list.location_id_id
                    return Response(
                        {
                            "Status": status.HTTP_200_OK,
                            "Message": "Function Successfully Added",
                            "Data": data
                        }
                    )
                else:
                    return Response(
                        {
                            "Status": status.HTTP_400_BAD_REQUEST,
                            "Message": "Function allready Exist",
                        }
                    )
            else:
                data = Serializer.errors
                return Response(
                    {
                        "Status": status.HTTP_204_NO_CONTENT,
                        "Message": "Fill required data",
                        "Function_Details": data
                    }
                )