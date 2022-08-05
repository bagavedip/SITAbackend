from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from hub.serializers.functions import FunctionSerializer
from hub.services.functions import FunctionService
from hub.services.assets import AssetService
from hub.services.itsm import ITSMService
from hub.services.soar import SOARService
from hub.services.siem import SIEMService


class FunctionViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    
    serializer_class = FunctionSerializer
    queryset = FunctionService.get_queryset()

    def function(self, request):
        try:
            id = request.query_params["id"]
            if id != None:
                data = FunctionService.get_queryset().filter(id=id)
                if data:
                    serializer = self.serializer_class(data, many=True)
                    return Response(
                        {
                            "Status": status.HTTP_200_OK,
                            "Data": serializer.data,
                        }
                    )
                else:
                    return Response(
                        {
                            "Status": status.HTTP_404_NOT_FOUND,
                            "Message": "No Function found for this id"
                        }
                    )
            else:
                return Response(
                    {
                        "Status": status.HTTP_400_BAD_REQUEST,
                        "Message": "Please provide an Id"
                    }
                )
        except:
            data = FunctionService.get_queryset()
            if data:
                dataset = []
                for functions in data:
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
            else:
                return Response(
                    {
                        "Status":status.HTTP_404_NOT_FOUND,
                        "Message":"You don't have any Function"
                    }
                )

    def functionlocationentity(self, request):
        try:
            id = request.query_params["id"]
            if id != None:
                queryset = FunctionService.get_queryset().select_related('location_id','location_id__entity_id').filter(id=id)
                dataset=[]
                for functions in queryset:
                    data = ({
                        "Function_id":functions.id,
                        "Function_name":functions.function_name,
                        "Location_id":functions.location_id.id,
                        "Location":functions.location_id.location,
                        "Entity_id":functions.location_id.entity_id.id,
                        "Entity":functions.location_id.entity_id.entityname,
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
            queryset = FunctionService.get_queryset().select_related('location_id','location_id__entity_id')
            dataset=[]
            for functions in queryset:
                data = ({
                    "Function_id":functions.id,
                    "Function_name":functions.function_name,
                    "Location_id":functions.location_id.id,
                    "Location":functions.location_id.location,
                    "Entity_id":functions.location_id.entity_id.id,
                    "Entity":functions.location_id.entity_id.entityname,
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
        all_records =[]
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
                            function_offences[functions.get('function_name')] = function_offences.get(functions.get('function_name'), 0) + 1
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
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        with transaction.atomic():
            Function_queryset = FunctionService.get_queryset().filter(id=function_id)
            for data in Function_queryset:
                function = FunctionService.update(data, **validated_data)
                data = {
                    "id": function.pk,
                    "Function Name":function.function_name,
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
            Serializer = self.serializer_class(data = request.data)
            data = {}
            if Serializer.is_valid():
                if not self.queryset.filter(function_name=request.data["function_name"]).exists():
                    function = Serializer.save()
                    data["Id"]= function.id
                    data['Function'] = function.function_name
                    data['Location'] = function.location_id_id
                    print(data)
                    return Response (
                        {
                            "Status": status.HTTP_200_OK,
                            "Message": "Function Successfully Added",
                            "Process_details" : data
                        }
                    )
                else:
                    return Response (
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
