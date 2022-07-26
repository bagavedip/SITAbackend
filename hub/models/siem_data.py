from django.db import models
from django.utils.translation import gettext as _


class SIEM(models.Model):
    """
    Model to hold data for SIEM data
    """

    offense_source = models.CharField(max_length=200, null= True, help_text="Offense Source")
    rule_name = models.CharField(max_length=200, null= True, help_text="Rule Name")
    seim_id = models.IntegerField(help_text="SIEM Id")
    description = models.CharField(max_length=200, null= True, help_text="Description")
    last_updated_datetime = models.DateTimeField(max_length=200, null= True, help_text="Last Updated Date Time")
    start_datetime = models.DateTimeField(max_length=200, null= True, help_text="Start Date Time")
    destination_networks = models.CharField(max_length=200, null= True, help_text="Destination Network")
    policy_category_count = models.IntegerField( null= True,help_text="Policy category Count")
    category_count = models.IntegerField( null= True,help_text="Category Count")
    inactive = models.BooleanField( null= True,help_text="Inactive")
    flow_count = models.IntegerField( null= True,help_text="Flow Count")
    follow_up = models.BooleanField( null= True,help_text="Follow Up")
    close_time = models.DateTimeField(max_length=200, null= True, help_text="Close Time")
    severity = models.IntegerField( null= True,help_text="Severity")
    credibility = models.IntegerField( null= True,help_text="Credibility")
    closing_reason_id = models.IntegerField( null= True,help_text="Closing Reason id")
    device_count = models.IntegerField( null= True,help_text="Device Count")
    domain_id = models.IntegerField(null= True, help_text="Domain Id")
    username_count = models.IntegerField( null= True,help_text="Username Count")
    protected = models.BooleanField( null= True,help_text="Protected")
    relevance = models.IntegerField( null= True,help_text="Relevance")
    source_network = models.CharField(max_length=200, null= True, help_text="Source Network")
    status = models.CharField(max_length=200, null= True, help_text="Status")
    source_count = models.IntegerField( null= True,help_text="Source Count")
    rules = models.CharField(max_length=200, null= True, help_text="Rules")
    assigned_to = models.IntegerField( null= True,help_text="Assigned To")
    offense_type = models.IntegerField( null= True,help_text="Offense Type")
    security_category_count = models.IntegerField( null= True,help_text="Security Category Count")
    remote_destination_count = models.IntegerField( null= True,help_text="Remote Destination Count")
    categories = models.CharField(max_length=200, null= True, help_text="Categories")
    event_count = models.IntegerField( null= True,help_text="Event Count")
    local_destination_count = models.IntegerField( null= True,help_text="Local Destination Count")
    log_sources = models.CharField(max_length=200, null= True, help_text="Log Sources")
    magnitude = models.IntegerField(null= True, help_text="Magnitude")
    closing_user = models.IntegerField(null= True, help_text="Closing User")
    source_address_ids = models.CharField(max_length=200, null= True, help_text="Source address ids")
    local_destination_address_ids = models.CharField(max_length=200, null= True,
                                                     help_text="Local destination address ids")

