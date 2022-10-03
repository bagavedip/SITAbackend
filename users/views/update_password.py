import logging
from django.db import transaction
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated

from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from users.models import User
from users.serializers.user import PasswordUpdateSerializer

logger = logging.getLogger(__name__)

class PasswordUpdate(mixins.CreateModelMixin, viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated]

    def update_password(self, request):
        request_user = request.data
        serializer = PasswordUpdateSerializer(data = request_user)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        with transaction.atomic():
            password = make_password(validated_data["password"])
            if serializer.is_valid():
                updated_user = User.objects.get(email = validated_data["email"])
                updated_user.password  = password
                updated_user.save()
                return Response(
                    {
                    "Data":serializer.data, 
                    "Status":status.HTTP_201_CREATED,
                    "Message": "User Added Successfully!!"
                    }
                )
            else:
                return Response(
                    {
                    "Data":serializer.data, 
                    "Status":status.HTTP_304_NOT_MODIFIED,
                    "Message": "Oops!!"
                    }
                )
        # updated_user.save()
        # return Response({
        #     "Message": "User Updated Successfully"})
