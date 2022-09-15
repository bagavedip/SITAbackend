from django.shortcuts import render
from requests import Response
from rest_framework import status, viewsets

from extracter.services.itsm import ITSMServices


class Extracter(viewsets.GenericViewSet):
    def itsm(self, request):
        """
         Timeline view for insights
        """
        result = ITSMServices.itsm_dump()
        return Response("hello")
