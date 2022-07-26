import logging
from hub.models.functions import Function
from django.shortcuts import get_object_or_404

logger = logging.getLogger(__name__)


class FunctionService:
    
    @staticmethod
    def get_queryset():
        """Function to return all Functions"""
        return Function.objects.all()

    @staticmethod
    def get_object_or_404(start_datetime):
        """
        Function which find function by id else raise 404 exception
        """
        logger.info(f"Received Function start datetime {start_datetime}")
        return get_object_or_404(FunctionService.get_queryset(), pk=start_datetime)

    @staticmethod
    def function_filter(id):
        filtered_data = FunctionService.get_queryset().filter(location_id=id)
        return filtered_data
