import csv
import codecs
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from hub.models.process import Process
from hub.serializers.process import ProcessSerializer
from hub.services.process import ProcessService


class ProcessViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = ProcessSerializer

    # queryset = ProcessService.get_queryset()

    @action(detail=False, methods=["put"])
    def update_process(self, request, process_id):
        """
            Function to update asset queryset
        """
        serializer = ProcessSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        with transaction.atomic():
            process_queryset = ProcessService.get_queryset().filter(id=process_id)
            for data in process_queryset:
                process = ProcessService.update(data, **validated_data)
                data = {
                    "id": process.pk,
                    "Process Name": process.process,
                }
        return Response(data)

    def process_delete(self, request, process_id):
        queryset = ProcessService.get_queryset().filter(id=process_id)
        if queryset:
            queryset.delete()
            message = f"Record deleted for id {process_id}"
            Status = status.HTTP_200_OK
        else:
            message = f"Record not found for id {process_id}"
            Status = status.HTTP_404_NOT_FOUND
        return Response(
            {
                "Status": Status,
                "Message": message
            })

    @action(detail=False, methods=["post"])
    def addprocess(self, request, **kwargs):
        if request.method == 'POST':
            Serializer = ProcessSerializer(data=request.data)
            data = {}
            if Serializer.is_valid():
                if not ProcessService.get_queryset().filter(process=request.data["process"]).exists():
                    process = Serializer.save()
                    data["Id"] = process.id
                    data['Process'] = process.process
                    return Response(
                        {
                            "Status": status.HTTP_200_OK,
                            "Message": "Process Successfully Added",
                            "Process_details": data
                        }
                    )
                else:
                    return Response(
                        {
                            "Status": status.HTTP_400_BAD_REQUEST,
                            "Message": "Process allready Exist",
                        }
                    )
            else:
                data = Serializer.errors
                return Response(
                    {
                        "Status": status.HTTP_204_NO_CONTENT,
                        "Message": "Fill required data",
                        "Process_Details": data
                    }
                )

    @action(detail=False, methods=['POST'])
    def validate_process(self, request):
        # """Upload data from CSV, with validation."""
        file = request.FILES.get("File")

        reader = csv.DictReader(codecs.iterdecode(file, "utf-8"), delimiter=",")
        data = list(reader)
        # print(data)
        cate_data = {}
        serializer = ProcessSerializer(data=data, many=True)
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
            process_err = serializer.errors
            return Response({
                "Status": status.HTTP_406_NOT_ACCEPTABLE,
                "Message": serializer.errors,
                "Data": process_err
            }
            )

    @action(detail=False, methods=['POST'])
    def upload_process(self, request):
        """Upload data from CSV, with validation."""
        file = request.FILES.get("File")

        reader = csv.DictReader(codecs.iterdecode(file, "utf-8"), delimiter=",")
        data = list(reader)
        # print(data)
        serializer = ProcessSerializer(data=data, many=True)
        # print(serializer)
        if serializer.is_valid():
            process_list = []
            for row in serializer.data:
                process_list.append(
                    Process(
                        process=row["process"],
                    )
                )
            # print(asset_list)
            Process.objects.bulk_create(process_list)

            return Response({
                "Status": status.HTTP_200_OK,
                "Message": "Successfully upload the data",
                "Data": data
            }
            )
        else:
            process_err = serializer.errors
            # print(asset_err)
            return Response({
                "Status": status.HTTP_406_NOT_ACCEPTABLE,
                "Message": serializer.errors,
                "Data": process_err
            }
            )

    def process_details(self, request, **kwargs):
        queryset = ProcessService.get_queryset()
        queryset_details = []
        for data in queryset:
            query_data = ({
                "Id": data.id,
                "Process": data.process
            })
            queryset_details.append(query_data)

        return Response(
            {
                "Status": status.HTTP_200_OK,
                "Data": queryset_details
            }
        )

    def single_process_details(self, request, process_id):
        queryset = ProcessService.get_queryset().filter(id=process_id)
        if queryset:
            queryset_details = []
            for data in queryset:
                query_data = ({
                    "Id": data.id,
                    "Process": data.process
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
