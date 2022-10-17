import logging

from django.db.models import Q

from hub.models.perspective import Perspective
from hub.models.process import Process

from hub.serializers.perspective_grid_data import PerspectiveSerializer

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
    def perspective_grid_data():
        """
        function fetches all data from the perspective model
        for perspective_gird_data
        """
        @staticmethod
        def get_tickets(response_obj: PerspectiveSerializer):
            filter_q = Q(**response_obj.filters)
            query_data = Perspective.objects.filter(filter_q).values(*response_obj.select_cols)
            return query_data
