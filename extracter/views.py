from django.http import HttpResponse
from requests import Response
from rest_framework import viewsets
import logging
from extracter.services.itsm import ITSMServices
from extracter.services.soar import SoarService

logger = logging.getLogger(__name__)


class Extracter(viewsets.GenericViewSet):
    def itsm(self, request, *args, **kwargs):
        """
         Timeline view for insights
        """
        logger.info(f"request data is{request.data}")
        result = ITSMServices.itsm_dump()
        return HttpResponse({
                "Message": "Data Already Exist."}
        )

    def soar(self, request):
        result = SoarService.get_all_cases()
        return HttpResponse("hello")
