from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from hub.serializers.process import ProcessSerializer


class AddProcessViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):

    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]


    serializer_class = ProcessSerializer

    @action(detail=False, methods=["post"])
    def addprocess(self, request):
        if request.method == 'POST':
            Serializer = ProcessSerializer(data=request.data)
            data = {}
            if Serializer.is_valid():
                process = Serializer.save()
                data['Process'] = process.process
                return Response(
                    {
                        "Status": status.HTTP_200_OK,
                        "Message": "Process Successfully Added",
                        "Process_details" : data
                    }
                )
            else:
                data = Serializer.errors
                return Response(
                    {
                        "Status": status.HTTP_400_BAD_REQUEST,
                        "Message": "Fill required data",
                        "Process_Details": data
                    }
                )
