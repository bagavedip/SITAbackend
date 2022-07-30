from django.db import transaction
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

    @action(detail=False, methods=["put"])
    def update_category(self, request, category_id):
        """
            Function to update asset queryset
        """
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        with transaction.atomic():
            categories = CategoryService.get_queryset().filter(id=category_id)
            for data in categories:
                category = CategoryService.update(data, **validated_data)
                data = {
                    "id": category.pk,
                    "Category Name": category.category,
                }
        return Response(data)


    def category_delete(self, request, category_id):
        queryset = CategoryService.get_queryset().filter(id=category_id)
        if queryset:
            queryset.delete()
            message = f"Record deleted for id {category_id}"
            Status = status.HTTP_200_OK
        else:
            message = f"Record not found for id {category_id}"
            Status = status.HTTP_404_NOT_FOUND
        return Response(
            {
                "Status": Status,
                "Message": message
            })