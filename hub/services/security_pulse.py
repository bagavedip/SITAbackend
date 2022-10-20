import logging

from django.core.files.base import ContentFile
from django.utils import timezone

from django.db.models import Q

from hub.models import SecurityPulse ,SecurityPulseImage
from hub.serializers.security_pulse_grid import SecurityPulseGridSerializer

logger = logging.getLogger(__name__)


class SecurityPulseService:

    @staticmethod
    def create_from_validated_data(user, validated_data):
        # imageData1 = validated_data.get("imageData1")
        # imageData2 = validated_data.get("imageData2")
        # imageData3 = validated_data.get("imageData3")
        # imageData4 = validated_data.get("imageData4")
        #
        # imageData1Name = validated_data.get("imageData1Name")
        # imageData2Name = validated_data.get("imageData2Name")
        # imageData3Name = validated_data.get("imageData3Name")
        # imageData4Name = validated_data.get("imageData4Name")
        # donut_left_graph = ContentFile(imageData1, name=imageData1Name)
        # donut_right_graph = ContentFile(imageData2, name=imageData2Name)
        # comparative_left_graph = ContentFile(imageData3, name=imageData3Name)
        # comparative_right_graph = ContentFile(imageData4, name=imageData4Name)
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
            info = section.get("info")
            security_pulse_image_kwargs = {
                "image_data": image_data,
                "info": info,
                "security_pulse": response.pk

            }
            security_pulse_image = SecurityPulseImage.objects.create(**security_pulse_image_kwargs)
        return response

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
    @staticmethod
    def security_pulse_details_data(security_pulse_id):
        """
        this function return details of security_pulse_details_data
        """
        queryset = SecurityPulse.objects.get(id=security_pulse_id)
        security_pulse_title = queryset.security_pulse_title
        main_title = queryset.mainTitle,
        image_data = queryset.imageData,
        selected_entities = queryset.selected_entities,
        created_at = queryset.created_at
        created_date = str(created_at)[:10]
        user = queryset.created_by
        recommendations = queryset.recommendations
        selected_assets = queryset.selected_assets
        selected_incident = queryset.selected_incident
        links = queryset.links
        response_data = {
            "headerData": {
                "user": user,
                "designation": "Cyber Security Engineer",
                "createdDate": created_date
            },
            "securityPulseFormData": {
                "securityPulseTitle": security_pulse_title,
                "mainTitle": main_title,
                "sections": [
                    {
                        "imageData": image_data
                    },
                ],
                "recommendations": [
                    recommendations,
                ],
                "links": [
                    { links },
                ],
                "selectedIncidents": [
                    selected_incident,
                ],
                "selectedAssets": [
                    selected_assets,
                ],
                "selectedEntities": [
                    selected_entities,
                ]
            },
            "footerData": {
                "email": "info@etek.com",
                "contacts": [
                    {
                        "countryName": "Colombia",
                        "contactNo": "+57(1)2571520"
                    },
                    {
                        "countryName": "Peru'",
                        "contactNo": "+51(1)6124343"
                    },
                    {
                        "countryName": "India",
                        "contactNo": "+91-9873451221"
                    }
                ]
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)