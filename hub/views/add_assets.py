from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from hub.serializers.assets import AssetSerializer


class AddAssetViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):

    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = AssetSerializer

    @action(detail=False, methods=["post"])
    def addasset(self, request, **kwargs):
        if request.method == 'POST':
            print(request.data)
            Serializer = AssetSerializer(data=request.data)
            data = {}
            if Serializer.is_valid():
                asset = Serializer.save()
                data['Asset_Name'] = asset.AssetName
                data['Asset_Type'] = asset.AssetType
                data['Function_Id'] = asset.function_id_id
                return Response(
                    {
                        "Status": status.HTTP_200_OK,
                        "Message": "Asset Successfully Added",
                        "Asset_Details": data
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
