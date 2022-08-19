from hub.models.hub import Hub
from django.db.models import Sum

from hub.serializers.hub import InsightsSerializer


class HubService:

    @staticmethod
    def get_insights(reesponse_obj: InsightsSerializer):
        query_data = Hub.objects.filter(starttime__gte=reesponse_obj.start_date, endtime__lte=reesponse_obj.end_date).values(*reesponse_obj.model_group_map).order_by().annotate(events=Sum('events'))
        print(f"query_data{query_data}")
        reesponse_obj.set_requst_queryset(query_data)
        incidents = Hub.objects.filter(starttime__gte=reesponse_obj.start_date, endtime__lte=reesponse_obj.end_date).values('criticality').order_by().annotate(events=Sum('events'))
        for row in incidents:
            reesponse_obj.donut_center[row.get('criticality')] = row.get('events')
        return query_data
