import logging
from hub.models.soar_data import SOAR
from django.shortcuts import get_object_or_404

logger = logging.getLogger(__name__)


class SOARService:
    
    @staticmethod
    def get_queryset():
        """Function to return all soar"""
        return SOAR.objects.all()

    @staticmethod
    def get_object_or_404(start_datetime):
        """
        Function which find SOAR by id else raise 404 exception
        """
        logger.info(f"Received SOAR start datetime {start_datetime}")
        return get_object_or_404(SOARService.get_queryset(), pk=start_datetime)

    @staticmethod
    def soar_filter(affair):
        filtered_data = SOARService.get_queryset().filter(SOAR_ID=affair)
        return filtered_data
