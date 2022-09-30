import logging
from sita.models.source_data import Source

logger = logging.getLogger(__name__)


class SourceService:
    """Service class for Source model.
    """

    @staticmethod
    def get_queryset():
        return Source.objects.all()

    @staticmethod
    def create(**kwargs):
        """Function which create source from kwargs
        """
        logger.debug(f"Creating source with following kwargs {kwargs}")
        return Source.objects.create(**kwargs)

    @staticmethod
    def create_from_validated_data(user, validated_data):
        """Function which create source from validated data
        """
        logger.debug(f"Received validated data {validated_data}")

        modified_credentials = []
        for index, data in enumerate(validated_data["credentials"], start=1):
            credentials = {
                "filename": data["filename"],
                "path": data["path"],
            }
            modified_credentials.append(credentials)

        source_kwargs = {
            "name": validated_data["name"],
            "type": validated_data["type"],
            "credentials": modified_credentials,
        }
        logger.debug(f"Creating source from following kwargs {source_kwargs}")

        source = SourceService.create(**source_kwargs)
        logger.info(f"source with ID {source.pk} created successfully.")

        return source
