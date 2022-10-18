from rest_framework import serializers
from hub.models.perspective import Perspective


class PerspectiveSerializer(serializers.ModelSerializer):
    """
    Model serializer for Process information
    """
    # tags = serializers.ListField(allow_empty=False, child=serializers.ListField(allow_empty=True, allow_null=True, child=serializers.CharField(label='Tags', max_length=255), help_text='Email Ids', label='Emails', required=False))

    class Meta:
        model = Perspective
        fields = (
            "perspective_type",
            "action_type",
            "status_type",
            "criticality_type",
            "incident_id",
            "perspective_title",
            "perspective",
            "recommendation",
            "selected_assets",
            "selected_entities",
            "imageData1",
            "imageData2",
            "imageData3",
            "comparative_right_graph",
            "incident_start_date_time",
            "incident_end_date_time",
        )


class PerspectiveUpdateSerializer(serializers.ModelSerializer):
    """
     Model serializer for Process information
     """
    class Meta:
        model = Perspective
        fields = (
            "perspective_type",
            "action_type",
            "status_type",
            "criticality_type",
            "incident_id",
            "perspective_title",
            "perspective",
            "recommendation",
            "selected_assets",
            "selected_entities",
            "donut_left_graph",
            "donut_right_graph",
            "comparative_left_graph",
            "comparative_right_graph",
            "incident_start_date_time",
            "incident_end_date_time",
        )

