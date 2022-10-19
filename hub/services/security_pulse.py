import logging

from django.db.models import Q

from hub.models import SecurityPulse
from hub.serializers.security_pulse_grid import SecurityPulseGridSerializer

logger = logging.getLogger(__name__)


class SecurityPulseService:
    @staticmethod
    def security_pulse_grid(response_obj: SecurityPulseGridSerializer):
        filter_q = Q(**response_obj.filters)
        query_data = SecurityPulse.objects.filter(filter_q).values(*response_obj.select_cols)
        return query_data

    @staticmethod
    def delete(security):
        """Function which delete security_pulse.

        Args:
            security ([security_pulse]): [Instance of security_pulse]
        """
        # End date in society
        security.delete()
        logger.info(f"Society with ID {security.pk} deleted successfully.")
