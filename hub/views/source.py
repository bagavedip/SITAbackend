import os
import logging
import pandas as pd
from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.response import Response
from hub.serializers.siem import SIEMSerializer
from hub.serializers.source import SourceSerializer
from hub.models.source_data import Source
from hub.services.source import SourceService
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


logger = logging.getLogger(__name__)


class SourceViewSet(viewsets.GenericViewSet):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    """Viewset class for source model.

    Args:
        viewsets ([viewsets.GenericViewSet]): [Generic ViewSet]
    """

    queryset = SourceService.get_queryset()
    serializer_class = SourceSerializer
    
    def create(self, request):
        """Function which create source record.
        """
        logger.debug(f"Receieved request body {request.data}")
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        logger.debug(f"Validated data {validated_data}")
        with transaction.atomic():
            source = SourceService.create_from_validated_data(request.user, validated_data)
            file_path = os.path.join(source.credentials[0]['path'], source.credentials[0]['filename'])
            if source.type == 'EXCEL':
                df = pd.read_excel(file_path)
                if source.name == 'SIEM':
                    serializer_class = SIEMSerializer(data=df)
                    serializer_class.is_valid()
                    serializer_class.save()

            logger.info(f"Source with ID {source.pk} created successfully.")
            return Response({"id": source.pk}, status=status.HTTP_201_CREATED)
    
    def source_data(self):
        source_data = Source.objects.all()

        return source_data
