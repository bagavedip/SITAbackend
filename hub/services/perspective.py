import logging
from django.utils import timezone

from hub.models.perspective import Perspective


logger = logging.getLogger(__name__)


class PerspectiveService:
    """
     Services for perspective models
    """

    @staticmethod
    def get_queryset():
        """Function to return all Entity"""
        return Perspective.objects.all()

    @staticmethod
    def perspective_dropdown_data():
        """
         function fetch all required data from
         Perspective model for perspective_dropdown_data.
        """
        # fetch perspective_type list in models
        perspective_type = Perspective.objects.values_list('perspective_type').distinct()
        perspective_dropdown = [{
            "label": "Prospective Type",
            "value": "Select"
        }]

        # fetch action_type list in models
        action_type = Perspective.objects.values_list('action_type').distinct()
        action_dropdown = [{
            "label": "Action Taken",
            "value": "Select",
        }]

        # fetch status list in models
        status = Perspective.objects.values_list('status_type').distinct()
        status_dropdown = [{
            "value": "Select",
            "label": "Status"
        }]
        for perspective_type in perspective_type:
            new_asset = {
                "value": perspective_type,
                "label": perspective_type
            }

            perspective_dropdown.append(new_asset)
        for action in action_type:
            new_geo = {
                "value": action,
                "label": action
            }
            action_dropdown.append(new_geo)
        for status in status:
            new_entity = {
                "value": status,
                "label": status
            }
            status_dropdown.append(new_entity)

        # final response which gives actual dropdown_data
        response = [
            {
                "id": "PerspectiveType",
                "dropdownoption": perspective_dropdown
            },
            {
                "id": "ActionTaken",
                "dropdownoption": action_dropdown
            },
            {
                "id": "Status",
                "dropdownoption": status_dropdown
            }
        ]
        return response

    @staticmethod
    def create_from_validated_data(user, validated_data):
        perspective_kwargs = {
            "perspective_type": validated_data.get("perspective_type"),
            "action_type": validated_data.get("action_type"),
            "status_type": validated_data.get("status_type"),
            "criticality_type": validated_data.get("criticality_type"),
            "incident_id": validated_data.get("incident_id"),
            "perspective_title": validated_data.get("perspective_title"),
            "perspective": validated_data.get("perspective"),
            "recommendation": validated_data.get("recommendation"),
            "tags": validated_data.get("tags"),
            "donut_left_graph": validated_data.get("donut_left_graph"),
            "donut_right_graph": validated_data.get("donut_right_graph"),
            "comparative_left_graph": validated_data.get("comparative_left_graph"),
            "comparative_right_graph": validated_data.get("comparative_right_graph"),
            "incident_start_date_time": validated_data.get("incident_start_date_time"),
            "incident_end_date_time": validated_data.get("incident_end_date_time"),
            "created_by": user,
            "created_at": timezone.now()
        }
        response = Perspective.objects.create(**perspective_kwargs)
        return response

    @staticmethod
    def update_from_validated_data(perspective, user, validated_data):
        perspective_kwargs = {
            "perspective_type": validated_data.get("perspective_type"),
            "action_type": validated_data.get("action_type"),
            "status_type": validated_data.get("status_type"),
            "criticality_type": validated_data.get("criticality_type"),
            "incident_id": validated_data.get("incident_id"),
            "perspective_title": validated_data.get("perspective_title"),
            "perspective": validated_data.get("perspective"),
            "recommendation": validated_data.get("recommendation"),
            "tags": validated_data.get("tags"),
            "donut_left_graph": validated_data.get("donut_left_graph"),
            'donut_right_graph': validated_data.get("donut_right_graph"),
            "comparative_left_graph": validated_data.get("comparative_left_graph"),
            "comparative_right_graph": validated_data.get("comparative_right_graph"),
            "incident_start_date_time": validated_data.get("incident_start_date_time"),
            "incident_end_date_time": validated_data.get("incident_end_date_time"),
            "created_by": user,
            "created_at": timezone.now()
        }
        logger.debug(f"Updating asset with following kwargs {perspective_kwargs}")
        perspective = Perspective.objects.update(perspective, **perspective_kwargs)
        return perspective

    @staticmethod
    def perspective_details_data(perspective_id):
        """
         function to show perspective_details_data
         using given id
        """
        queryset = Perspective.objects.get(id=perspective_id)
        perspective_title = queryset.perspective_title
        selected_id = queryset.incident_id
        selected_assets = queryset.selected_assets
        selected_entities = queryset.selected_entities
        created_at = queryset.created_at
        created_date = str(created_at)[:10]
        created_time = str(created_at)[11:19]
        updated_at = queryset.updated_at
        updated_date = str(updated_at)[:10]
        updated_time = str(updated_at)[11:19]
        response_data = {
            "perspectiveFormData": {
                "perspectiveTitle": perspective_title,
                "selectedIds": selected_id,
                "selectedAssets": selected_assets,
                "selectedEntities": selected_entities,
                "imageData1": None
            },
            "footerData": {
                "lastUpdateInformation": {
                    "user": queryset.updated_by,
                    "date": created_date,
                    "time": created_time
                },
                "originallyCreatedBy": {
                    "user": queryset.created_by,
                    "date": updated_date,
                    "time": updated_time
                }
            }
        }
        return response_data

    @staticmethod
    def delete(perspective):
        """Function which delete perspective.

        Args:
            perspective ([perspective]): [Instance of perspective]
        """
        # End date in society
        perspective.delete()
        logger.info(f"Society with ID {perspective.pk} deleted successfully.")
