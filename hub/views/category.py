from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from hub.serializers.category import CategorySerializer


class AddCategoryViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):

    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer

    @action(detail=False, methods=["post"])
    def addcategory(self, request):
        if request.method == 'POST':
            Serializer = CategorySerializer(data=request.data)
            data = {}
            if Serializer.is_valid():
                category = Serializer.save()
                data['Category'] = category.category
                return Response(
                    {
                        "Status": status.HTTP_200_OK,
                        "Message": "Category Successfully Added",
                        "Category_details": data
                    }
                )
            else:
                data = Serializer.errors
                return Response(
                    {
                        "Status": status.HTTP_400_BAD_REQUEST,
                        "Message": "Fill required data",
                        "Category_Details": data
                    }
                )
