from django.db import models
from django.utils.translation import gettext as _


class SIEM(models.Model):
    """
    Model to hold data for SIEM data
    """

    offense_source = models.CharField(_("offense_source"), max_length=200, null=True, help_text="Offense Source")
    rule_name = models.CharField(_("rule_name"), max_length=200, null=True, help_text="Rule Name")
    seim_id = models.IntegerField(_("seim_id"), help_text="SIEM Id")
    description = models.CharField(_("description"), max_length=200, null=True, help_text="Description")
    last_updated_datetime = models.DateTimeField(_("last_updated_datetime"), max_length=200, null=True, help_text="Last Updated Date Time")
    start_datetime = models.DateTimeField(_("start_datetime"), max_length=200, null=True, help_text="Start Date Time")
    destination_networks = models.CharField(_("destination_networks"), max_length=200, null=True, help_text="Destination Network")
    policy_category_count = models.IntegerField(_("policy_category_count"), null=True, help_text="Policy category Count")
    category_count = models.IntegerField(_("category_count"), null=True, help_text="Category Count")
    inactive = models.BooleanField(_("inactive"), null=True, help_text="Inactive")
    flow_count = models.IntegerField(_("flow_count"), null=True, help_text="Flow Count")
    follow_up = models.BooleanField(_("follow_up"), null=True, help_text="Follow Up")
    close_time = models.DateTimeField(_("close_time"), max_length=200, null=True, help_text="Close Time")
    severity = models.IntegerField(_("severity"), null=True, help_text="Severity")
    credibility = models.IntegerField(_("credibility"), null=True, help_text="Credibility")
    closing_reason_id = models.IntegerField(_("closing_reason_id"), null=True, help_text="Closing Reason id")
    device_count = models.IntegerField(_("device_count"), null=True, help_text="Device Count")
    domain_id = models.IntegerField(_("domain_id"), null=True, help_text="Domain Id")
    username_count = models.IntegerField(_("username_count"), null=True, help_text="Username Count")
    protected = models.BooleanField(_("protected"), null=True, help_text="Protected")
    relevance = models.IntegerField(_("relevance"), null=True, help_text="Relevance")
    source_network = models.CharField(_("source_network"), max_length=200, null=True, help_text="Source Network")
    status = models.CharField(_("status"), max_length=200, null=True, help_text="Status")
    source_count = models.IntegerField(_("source_count"), null=True, help_text="Source Count")
    rules = models.CharField(_("rules"), max_length=200, null=True, help_text="Rules")
    assigned_to = models.IntegerField(_("assigned_to"), null=True, help_text="Assigned To")
    offense_type = models.IntegerField(_("offense_type"), null=True, help_text="Offense Type")
    security_category_count = models.IntegerField(_("security_category_count"), null=True, help_text="Security Category Count")
    remote_destination_count = models.IntegerField(_("remote_destination_count"), null=True, help_text="Remote Destination Count")
    categories = models.CharField(_("categories"), max_length=200, null=True, help_text="Categories")
    event_count = models.IntegerField(_("event_count"), null=True, help_text="Event Count")
    local_destination_count = models.IntegerField(_("local_destination_count"), null=True, help_text="Local Destination Count")
    log_sources = models.CharField(_("log_sources"), max_length=200, null=True, help_text="Log Sources")
    magnitude = models.IntegerField(_("magnitude"), null=True, help_text="Magnitude")
    closing_user = models.IntegerField(_("closing_user"), null=True, help_text="Closing User")
    source_address_ids = models.CharField(_("source_address_ids"), max_length=200, null=True, help_text="Source address ids")
    local_destination_address_ids = models.CharField(_("local_destination_address_ids"), max_length=200, null=True,
                                                     help_text="Local destination address ids")
