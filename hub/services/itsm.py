import logging

from django.db.models import Sum

from hub.models.itsm_data import ITSM

from hub.serializers.masterdata import OeiMasterDataSerialiser
from hub.serializers.oei_serializers import OeiSerializer

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
    def get_oei(reesponse_obj: OeiSerializer):
        print(reesponse_obj.model_group_map)
        query_data = ITSM.objects.filter(CreatedTime__lte=reesponse_obj.start_date, Ending_time__lte=reesponse_obj.end_date).values(*reesponse_obj.model_group_map).order_by().annotate(events=Sum('events'))
        print(query_data)
        reesponse_obj.set_request_queryset(query_data)
        ticket = ITSM.objects.filter(CreatedTime__lte=reesponse_obj.start_date, Ending_time__lte=reesponse_obj.end_date).values('Subject').order_by().annotate(events=Sum('events'))
        for row in ticket:
            reesponse_obj.donut_center[row.get('Subject')] = row.get('events')
        print(f"ticket{ticket}")
        # query_data = ITSM.objects.filter(CreatedTime__lte=reesponse_obj.start_date, Ending_time__lte=reesponse_obj.end_date, sla_name='alta')
        # print(query_data)
        # reesponse_obj.set_request_queryset(query_data)
        return query_data
