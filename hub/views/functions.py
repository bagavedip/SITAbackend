from rest_framework import status, viewsets
from rest_framework.response import Response
from hub.serializers.functions import FuctionSerializer
from hub.services.functions import FunctionService
from hub.services.assets import AssetService
from hub.services.itsm import ITSMService
from hub.services.soar import SOARService
from hub.services.siem import SIEMService


class FunctionViewSet(viewsets.ModelViewSet):

    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    
    serializer_class = FuctionSerializer

    def function(self, request):
        try:
            id = request.query_params["id"]
            if id != None:
                data = FunctionService.get_queryset().filter(id=id)
                if data:
                    serializer = self.serializer_class(data, many = True)
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
                        "Function_id":functions.id,
                        "Function_name":functions.function_name,
                        "Location_id":functions.location_id.id,
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
