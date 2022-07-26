from django.db import models
from django.utils.translation import gettext as _
from colorfield.fields import ColorField


class Hub(models.Model):

    class Criticality(models.TextChoices):
        HIGH = "HIGH", _("High"),
        MEDIUM = "MEDIUM", _("Medium"),
        LOW = "LOW", _("Low")

    entity_id = models.CharField(_("entity_id"), max_length=20000, help_text=_("entity id"), null=True)
    entity_name = models.CharField(_("entity_name"), max_length=200, help_text=_("entity name"))
    entity_color = ColorField(_("entity_color"), format='hexa', help_text=_("entity color"))
    location_id = models.CharField(_("location_id"), max_length=20000, help_text=_("location id"), null=True)
    location_name = models.CharField(_("location_name"), max_length=200, help_text=_("location name"))
    function_id = models.CharField(_("function_id"), max_length=20000, help_text=_("function id"), null=True)
    function_name = models.CharField(_("function_name"), max_length=200, help_text=_("function name"))
    asset_id = models.CharField(_("asset_id"), max_length=20000, help_text=_("asset id"), null=True)
    asset_name = models.CharField(_("asset_name"), max_length=200, help_text=_("asset name"))
    asset_type = models.CharField(_("asset_type"), max_length=200, help_text=_("asset type"))
    asset_color = ColorField(_("asset_color"), format='hexa', help_text=_("asset color"))
    usecase_id = models.CharField(_("usecase_id"), max_length=20000, help_text=_("use_case id"), null=True)
    use_case = models.CharField(_("use_case"), max_length=200, help_text=_("use case"))
    rule_id = models.CharField(_("rule_id"), max_length=20000, help_text=_("rule id"), null=True)
    rule_name = models.CharField(_("rule_name"), max_length=200, help_text=_("rule name"))
    seim_id = models.CharField(_("seim_id"), max_length=20000, help_text=_("seim id"), null=True)
    severity = models.IntegerField(_("severity"), null=True, help_text=_("Severity"))
    events = models.IntegerField(_("events"), null=True, help_text=_("events"))
    starttime = models.DateTimeField(_("event start time"), null=True, help_text=_("event start time"))
    endtime = models.DateTimeField(_("event end date"), null=True, help_text=_("event end time"))
    magnitude = models.IntegerField(_("magnitude"), null=True, help_text=_("Magnitude"))
    criticality = models.CharField(_("criticality"), max_length=256, null=True, choices=Criticality.choices,
                                   help_text=_("criticality"))
    criticality_color = ColorField(_("criticality_color"), null=True, help_text=_("criticality color"))
    description = models.CharField(_("description"), max_length=200, help_text=_("description"), null=True)
    itsm_id = models.CharField(_("itsm_id"), max_length=20000, help_text=_("itsm id"), null=True)
    request_status = models.CharField(_("request_status"), max_length=200, help_text=_("request status"), null=True)
    priority = models.CharField(_("priority"), max_length=200, help_text=_("priority"), null=True)
    group = models.CharField(_("group"), max_length=200, help_text=_("group"), null=True)
    category = models.CharField(_("category"), max_length=200, help_text=_("category"), null=True)
    soar_id = models.CharField(_("soar_id"), max_length=20000, help_text=_("soar id"), null=True)
    ticket_id = models.CharField(_("ticket_id"), max_length=20000, help_text=_("ticket id"), null=True)
    last_update_time = models.DateTimeField(_("last update time"), null=True, help_text=_("Last_update_time"))
    created_time = models.DateTimeField(_("created time"), null=True, help_text=_("created time"))
    level = models.CharField(_("level"), max_length=200, null=True, help_text=_("Ticket Level"))
    ticket_status = models.CharField(_("ticket_status"), max_length=200, help_text=_("ticket status"), null=True)
    ticket_details = models.CharField(_("ticket_details"), max_length=256, help_text=_("ticket_details"), null=True)
