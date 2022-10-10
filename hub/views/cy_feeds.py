import logging
import re
from urllib import response
from rest_framework import viewsets, status
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import json
from collections import defaultdict as dd

from hub.models.cy_feeds import CyFeeds
from hub.services.cy_feeds import Cy_FeedsService

logger = logging.getLogger(__name__)


class CyFeeds(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    def all_feeds(self, request):
        """View Function to extract feeds"""

        # calling services for CY data
        cy_response = Cy_FeedsService.get_cy_feeds()
        return cy_response
