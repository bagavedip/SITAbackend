from rest_framework import serializers
from sita.models.siem_data import SIEM


class SIEMSerializer(serializers.ModelSerializer):
    """
    Model serializer for SIEM information
    """

    class Meta:
        model = SIEM
        fields = (
            "offense_source","rule_name","seim_id","description",
            "last_updated_datetime","start_datetime","destination_networks",
            "policy_category_count","category_count","inactive",
            "flow_count","follow_up","close_time","severity",
            "credibility","closing_reason_id","device_count",
            "domain_id","username_count","protected","relevance",
            "source_network","status","source_count","rules",
            "assigned_to","offense_type","security_category_count",
            "remote_destination_count","categories","event_count",
            "local_destination_count","log_sources","magnitude",
            "closing_user","source_address_ids","local_destination_address_ids",
        )
