
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
        donut_left_graph = str(queryset.donut_left_graph)
        image_donut = open(donut_left_graph, "rb")
        response_data = {
            "perspectiveFormData": {
                "perspectiveTitle": perspective_title,
                "selectedIds": selected_id,
                "selectedAssets": selected_assets,
                "selectedEntities": selected_entities,
                "imageData1": image_donut,
                "imageData2": queryset.donut_right_graph.seek(0),
                "imageData3": queryset.comparative_left_graph.seek(0),
                "imageData4": queryset.comparative_right_graph.seek(0),
                "imageData1Name": queryset.donut_left_graph.seek(1),
                "imageData2Name": queryset.donut_right_graph.seek(1),
                "imageData3Name": queryset.comparative_left_graph.seek(1),
                "imageData4Name": queryset.comparative_right_graph.seek(1),
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
