import logging
from hub.models.itsm_data import ITSM
from django.shortcuts import get_object_or_404

logger = logging.getLogger(__name__)


class ITSMService:
    
    @staticmethod
    def get_queryset():
        """Function to return all ITSM data"""
        return ITSM.objects.all()

    @staticmethod
    def get_object_or_404(start_datetime):
        """
        Function which find ITSM by id else raise 404 exception
        """
        logger.info(f"Received ITSM start datetime {start_datetime}")
        return get_object_or_404(ITSMService.get_queryset(), pk=start_datetime)

    @staticmethod
    def itsm_filter(asset):

        filtered_data = ITSMService.get_queryset().filter(Asset_Name=asset)
        return filtered_data
