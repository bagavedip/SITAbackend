import logging

from hub.models import SecurityPulse
from hub.serializers.dashboard_grid import DashboardGridGridSerializer

logger = logging.getLogger(__name__)


class DashboardService:
    @staticmethod
    def dashboard_grid_data(response_obj: DashboardGridGridSerializer):
        query_data = SecurityPulse.objects.all().values(*response_obj.select_cols).order_by('-updated_at')[:3]
        return query_data
