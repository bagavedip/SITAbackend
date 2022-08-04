from hub.models.hub import Hub
from django.db.models import Q
from hub.serializers.ticket_details import TicketDetailsSerializer

class TicketsService:

    @staticmethod
    def get_tickets(response_obj: TicketDetailsSerializer):
        filter_q = Q(**response_obj.filters)
        query_data = Hub.objects.filter(filter_q).values(*response_obj.select_cols)
        return query_data
