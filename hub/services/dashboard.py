import logging

from hub.models import SecurityPulse
from hub.serializers.security_pulse_grid import SecurityPulseGridSerializer

logger = logging.getLogger(__name__)


class DashboardService:
    @staticmethod
    def dashboard_grid_data(response_obj: SecurityPulseGridSerializer):
        query_data = SecurityPulse.objects.all().values(*response_obj.select_cols).order_by('-updated_at')[:3]
        response_data = {
            "IsExternal": True,
            "Title": "",
            "index_id": "",
            "Links": ""
        }
        for query in query_data:
            response_data = {
                "IsExternal": False,
                "Title": query.main_title,
                "index_id": "",
                "Links": ""
            }
        return query_data
