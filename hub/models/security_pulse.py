from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User


class SecurityPulse(models.Model):

    class CriticalityType(models.TextChoices):
        High = "High", _("High")
        Medium = "Medium", _("Medium")
        Low = "Low", _("Low")

    id = models.BigAutoField(_("security_pulse_id"), primary_key=True)
    security_pulse_title = models.CharField(_("security_pulse_title"), null=True, max_length=400,
                                            help_text=_("security_pulse_title"))
    main_title = models.CharField(_("main_title"), null=True, max_length=400,
                                  help_text=_("main_title"))
    # ArrayFields
    recommendations = ArrayField(models.TextField(max_length=255), verbose_name=_("recommendations"), default=list,
                                 help_text=_("recommendations"))
    selected_incident = ArrayField(
        models.SmallIntegerField(),
        default=list,
        help_text=_("selected_incident"),
        verbose_name=_("selected_incident"),
    )
    selected_assets = ArrayField(models.CharField(max_length=255), verbose_name=_("selected_assets"), default=list,
                                 help_text=_("selected assets"))
    selected_entities = ArrayField(models.CharField(max_length=255), verbose_name=_("selected_entities"), default=list,
                                   help_text=_("selected entities"))
    criticality_type = models.CharField(
        _("perspective type"), max_length=100, choices=CriticalityType.choices, help_text=_("perspective type"),
        default="Low",)
    # links = ArrayField(models.JSONField(_("links"), default=dict, help_text=_("links")), null=True)
    links = models.JSONField(default=list, null=True, blank=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, null=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True, null=True)

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
