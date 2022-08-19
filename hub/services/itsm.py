import logging
from django.db.models import Count, Q
from hub.models.itsm_data import ITSM
from hub.serializers.oei_serializers import OeiSerializer
from hub.serializers.oei_ticket_details import TicketDetailsSerializer

logger = logging.getLogger(__name__)


class ITSMService:
    
    @staticmethod
    def get_queryset():
        """Function to return all ITSM data"""
        return ITSM.objects.all()

    @staticmethod
    def itsm_filter(asset):

        filtered_data = ITSMService.get_queryset().filter(Asset_Name=asset)
        return filtered_data

    @staticmethod
    def get_oei(response_obj: OeiSerializer):
        query_data = ITSM.objects.filter(CreatedTime__lte=response_obj.start_date, Ending_time__lte=response_obj.end_date).values(*response_obj.model_group_map).order_by().annotate(events=Count('Itsm_id'))
        response_obj.set_request_queryset(query_data)
        return query_data

    @staticmethod
    def get_tickets(response_obj: TicketDetailsSerializer):
        filter_q = Q(**response_obj.filters)
        query_data = ITSM.objects.filter(filter_q).values(*response_obj.select_cols)
        return query_data