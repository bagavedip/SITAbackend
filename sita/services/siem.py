import logging
from sita.models.siem_data import SIEM
from django.shortcuts import get_object_or_404

logger = logging.getLogger(__name__)


class SIEMService:
    """
     Services for SIEM models
    """
    
    @staticmethod
    def get_queryset():
        """Function to return all assets"""
        return SIEM.objects.all()

    @staticmethod
    def get_object_or_404(start_datetime):
        """
        Function which find asset by id else raise 404 exception
        """
        logger.info(f"Received SIEM start datetime {start_datetime}")
        return get_object_or_404(SIEMService.get_queryset(), pk=start_datetime)

    @staticmethod
    def siem_filter(ticket_id):
        filtered_data = SIEMService.get_queryset().filter(seim_id=ticket_id)
        return filtered_data
