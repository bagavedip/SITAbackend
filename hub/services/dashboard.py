import logging

from hub.models import SecurityPulse
from hub.serializers.security_pulse_grid import SecurityPulseGridSerializer

logger = logging.getLogger(__name__)


class DashboardService:
    @staticmethod
    def dashboard_grid_data(response_obj: SecurityPulseGridSerializer):
        query_data = SecurityPulse.objects.all().values(*response_obj.select_cols).order_by('-updated_at')[:3][::-1]
        return query_data
