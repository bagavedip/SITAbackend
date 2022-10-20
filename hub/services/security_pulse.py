import logging

from django.core.files.base import ContentFile
from django.utils import timezone

from hub.models import SecurityPulse,SecurityPulseImage
from hub.serializers.security_pulse_grid import SecurityPulseGridSerializer

logger = logging.getLogger(__name__)


class SecurityPulseService:

    @staticmethod
    def update(asset, **kwargs):
        """
        Function update an asset from kwargs
        """
        for key, value in kwargs.items():
            setattr(asset, key, value)
        asset.save()

        return asset

    @staticmethod
    def create_from_validated_data(user, validated_data):
        sections = validated_data.get("sections")
        security_pulse_kwargs = {
            "criticality_type": validated_data.get("criticality"),
            "security_pulse_title": validated_data.get("securityPulseTitle"),
            "main_title": validated_data.get("mainTitle"),
            "links": validated_data.get("links"),
            "recommendations": validated_data.get("recommendations"),
            "selected_assets": validated_data.get("selectedAssets"),
            "selected_entities": validated_data.get("selectedEntities"),
            "is_published": validated_data.get("isPublished"),
            "created_by": user,
            "updated_by": user,
            "created_at": timezone.now(),
            "updated_at": timezone.now()
        }
        response = SecurityPulse.objects.create(**security_pulse_kwargs)
        for section in sections:
            image_data = section.get("imageData")
            image_data_name = validated_data.get("imageDataName")
            image = ContentFile(image_data, name=image_data_name)
            info = section.get("info")
            security_pulse_image_kwargs = {
                "image_data": image,
                "info": info,
                "security_pulse": response

            }
            security_pulse_image = SecurityPulseImage.objects.create(**security_pulse_image_kwargs)
        return response

    @staticmethod
    def security_pulse_grid(response_obj: SecurityPulseGridSerializer):
        # filter_q = Q(**response_obj.filters)
        query_data = SecurityPulse.objects.all().values(*response_obj.select_cols)
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

    @staticmethod
    def update_from_validated_data(user, validated_data):
        securityPulseId = int(validated_data.get("securityPulseId"))
        queryset = SecurityPulse.objects.get(id=securityPulseId)
        sections = validated_data.get("sections")
        security_pulse_kwargs = {
            "criticality_type": validated_data.get("criticality"),
            "security_pulse_title": validated_data.get("securityPulseTitle"),
            "main_title": validated_data.get("mainTitle"),
            "links": validated_data.get("links"),
            "recommendations": validated_data.get("recommendations"),
            "selected_assets": validated_data.get("selectedAssets"),
            "selected_entities": validated_data.get("selectedEntities"),
            "is_published": validated_data.get("isPublished"),
            "created_by": user,
            "updated_by": user,
            "created_at": timezone.now(),
            "updated_at": timezone.now()
        }
        response = SecurityPulseService.update(queryset, **security_pulse_kwargs)
        for section in sections:
            image_data = section.get("imageData", None)
            image_data_name = validated_data.get("imageDataName", None)
            image = ContentFile(image_data, name=image_data_name)
            info = section.get("info", None)
            security_pulse_image_kwargs = {
                "image_data": image,
                "info": info,
                "security_pulse": response

            }
            queryset = SecurityPulseImage.objects.filter(security_pulse=securityPulseId)
            for query in queryset:
                security_pulse_image = SecurityPulseService.update(query, **security_pulse_image_kwargs)
        return security_pulse_image

    @staticmethod
    def edit_security_pulse_record_fetch(security_id):
        """
          function to show edit_perspective_record_fetch
          using given id
         """
        queryset = SecurityPulse.objects.get(id=security_id)
        selected_id = queryset.incident_id
        selected_assets = queryset.selected_assets
        selected_entities = queryset.selected_entities
        query = SecurityPulseImage.objects.filter(security_pulse=security_id)
        section = []
        for query in query:
            image = query.image_data.read()
            info = query.info
            image_name = str(queryset.image_data).split('/')[2],
            image_kwargs = {
                "imageData": image,
                "imageDataName": image_name,
                "info": info
            }
            section.append(image_kwargs)
        response_data = {
            "perspectiveFormData": {
                "securityPulseTitle": queryset.security_pulse_title,
                "mainTitle": queryset.main_title,
                "criticality": queryset.perspective,
                "sections": section,
                "recommendations": queryset.criticality_type,
                "links": queryset.action_type,
                "selectedIds": selected_id,
                "selectedAssets": selected_assets,
                "selectedEntities": selected_entities,
                "securityPulseId": security_id,
                "isPublished": queryset.is_published
            },
        }
        return response_data
