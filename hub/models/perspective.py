from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User




class Perspective(models.Model):
    """
     Models for Data holding for Perspective and Newsletters
    """
    class PerspectiveType(models.TextChoices):
        Incident = "Incident", _("Incident")
        Pattern = "Pattern", _("Pattern")

    class ActionType(models.TextChoices):
        notified = "notified", _("notified")
        under_investigation = "under_investigation", _("under_investigation")
        contained = "contained", _("contained")
        closed_by_etek = "closed_by_etek", _("closed_by_etek")
        closed_by_client = "closed_by_client", _("closed_by_client")
        no_action = "no_action", _("no_action")

    class StatusType(models.TextChoices):
        confirmed = "confirmed", _("confirmed")
        under_investigation = "under_investigation", _("under_investigation")
        false_positive = "false_positive", _("false_positive")

    class CriticalityType(models.TextChoices):
        High = "High", _("High")
        Medium = "Medium", _("Medium")
        Low = "Low", _("Low")

    perspective_type = models.CharField(
        _("perspective type"), max_length=100, choices=PerspectiveType.choices, help_text=_("perspective type")
    )
    action_type = models.CharField(
        _("action type"), max_length=100, choices=ActionType.choices, help_text=_("action type")
    )
    status_type = models.CharField(
        _("status type"), max_length=100, choices=StatusType.choices, help_text=_("status type")
    )
    criticality_type = models.CharField(
        _("perspective type"), max_length=100, choices=CriticalityType.choices, help_text=_("perspective type")
    )
    incident_id = ArrayField(
        models.SmallIntegerField(),
        default=list,
        help_text=_("incident_id"),
        verbose_name=_("incident_id"),
    )
    perspective_title = models.CharField(_("perspective_title"), max_length=100, null=True,
                                         help_text=_("perspective_title"))
    perspective = models.TextField(_("perspective"), null=True, help_text=_("perspective"))
    recommendation = models.TextField(_("recommendation"), null=True, help_text=_("recommendation"))
    publish = models.BooleanField(_("publish"), default=False, help_text=_("publish"))
    tags = ArrayField(ArrayField(models.CharField(max_length=255), verbose_name=_("emails"), default=list,
                                 help_text=_("Email Ids")), null=True,)

    # Image fields
    donut_left_graph = models.FileField(_("donut left graph"), upload_to="perspective/donut_graph", null=True,
                                        help_text=_("donut left graph"))
    donut_right_graph = models.ImageField(_("donut left graph"), upload_to="perspective/donut_graph", null=True,
                                          help_text=_("donut left graph"))
    comparative_left_graph = models.ImageField(_("donut left graph"), upload_to="perspective/comparative_graph",
                                               null=True, help_text=_("donut left graph"))
    comparative_right_graph = models.ImageField(_("donut left graph"), upload_to="perspective/comparative_graph",
                                                null=True, help_text=_("donut left graph"))

    # Datetime fields
    incident_start_date_time = models.DateTimeField(_("incident_start_date_time"), null=True,
                                                    help_text=_("incident_start_date_time"))
    incident_end_date_time = models.DateTimeField(_("incident_end_date_time"), null=True,
                                                  help_text=_("incident_end_date_time"))
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    # foreignkey fields
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        db_index=False,
        verbose_name=_("Created by"),
        help_text=_("Created by"),
        related_name="+",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        db_index=False,
        verbose_name=_("Updated by"),
        help_text=_("Updated by"),
        related_name="+",
    )
