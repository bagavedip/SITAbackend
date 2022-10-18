import logging


logger = logging.getLogger(__name__)


class SecurityPulseService:
    @staticmethod
    def create_from_validated_data(login_user, validated_data):
        return "hii"

    @staticmethod
    def update_from_validated_data(login_user, validated_data):
        return "hello"

    @staticmethod
    def delete(security):
        """Function which delete security_pulse.

        Args:
            security ([security_pulse]): [Instance of security_pulse]
        """
        # End date in society
        security.delete()
        logger.info(f"Society with ID {security.pk} deleted successfully.")
