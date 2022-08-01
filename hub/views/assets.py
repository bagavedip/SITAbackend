from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from hub.serializers.assets import AssetSerializer
from hub.services.assets import AssetService
from hub.services.itsm import ITSMService
from hub.services.soar import SOARService
from hub.services.siem import SIEMService


class AssetViewSet(viewsets.ModelViewSet):

    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    
    serializer_class = AssetSerializer

    def validated_data(self):
        """
        Function which return validated data
        """
        request_data = self.request.data
        serializer_args = list()
        serializer_kwargs = {"data": request_data}

        if self.action in ["update", "partial_update"]:
            serializer_args.append(self.get_object())

        if self.action in ["partial_update"]:
            serializer_kwargs["partial"] = True

        serializer = self.get_serializer(*serializer_args, **serializer_kwargs)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    def asset_types(self, requset):
        queryset = AssetService.get_queryset()

        Total_assets = []
        for asset in queryset.values():
            Total_assets.append(asset.get('AssetType'))
        asset_types = dict()  
        for types in Total_assets:
            asset_types[types] = asset_types.get(types, 0) + 1
        asset_types['Asset Total'] = sum(asset_types.values())
        data = asset_types
        return Response(
            {
                "Status": "Success",
                "Data": data,
            }
        )

    def asset(self, requset):
        queryset = AssetService.get_queryset().select_related('function_id','function_id__location_id',
                                                              'function_id__location_id__entity_id')
        Total_assets = []
        for asset in queryset:
            data = ({
                "Asset_Name": asset.AssetName,
                "Category": asset.category.category,
                "Criticality": asset.criticality,
                "Function_Name": asset.function_id.function_name,
                "Location": asset.function_id.location_id.location,
                "Entity": asset.function_id.location_id.entity_id.entityname,
                "Created_date": asset.created,
            })
                    
            Total_assets.append(data)
        return Response(
            {
                "Status": "Success",
                "Data": Total_assets,
            }
        )
    
    def offence_asset_types(self, requset):
        queryset = AssetService.get_queryset()

        asset_types = dict()
        for asset_name in queryset.values():
            itsm_data = ITSMService.itsm_filter(asset_name.get('AssetName'))
            for itsm in itsm_data.values():
                soar_data = SOARService.soar_filter(itsm.get('Affair'))
                for soar in soar_data.values():
                    siem_data = SIEMService.siem_filter(soar.get('TicketIDs'))
                    for siem in siem_data.values():
                        asset_types[asset_name.get('AssetType')] = asset_types.get(asset_name.get('AssetType'), 0) + 1
        asset_types['Asset Total'] = sum(asset_types.values())
        data = asset_types
        return Response(
            {
                "Status": "Success",
                "Data": data,
            }
        )

    @action(detail=False, methods=["put"])
    def update_asset(self, request, asset):
        """
            Function to update asset queryset
        """
        serializer = AssetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        with transaction.atomic():
            asset = AssetService.get_queryset().filter(id=asset)
            for asset in asset:
                assets = AssetService.update(asset, **validated_data)
                data = {
                    "id": assets.pk,
                    "Asset Name": assets.AssetName,
                }
        return Response(data)

    def asset_delete(self, request, asset_id):
        queryset = AssetService.get_queryset().filter(id=asset_id)
        if queryset:
            queryset.delete()
            message = f"Record deleted for id {asset_id}"
            Status = status.HTTP_200_OK
        else:
            message = f"Record not found for id {asset_id}"
            Status = status.HTTP_404_NOT_FOUND
        return Response(
            {
                "Status": Status,
                "Message": message
            })

    @action(detail=False, methods=["post"])
    def addasset(self, request, **kwargs):
        if request.method == 'POST':
            Serializer = AssetSerializer(data=request.data)
            data = {}
            if Serializer.is_valid():
                asset = Serializer.save()
                data['Asset_Name'] = asset.AssetName
                data['Category'] = asset.category_id
                data['Criticality'] = asset.criticality
                data['Function_Id'] = asset.function_id_id
                return Response(
                    {
                        "Status": status.HTTP_200_OK,
                        "Message": "Asset Successfully Added",
                        "Asset_Details": data,
                    }
                )
            else:
                data = Serializer.errors
                return Response(
                    {
                        "Status": status.HTTP_400_BAD_REQUEST,
                        "Message": "Fill required data",
                        "Asset_Details": data
                    }
                )
