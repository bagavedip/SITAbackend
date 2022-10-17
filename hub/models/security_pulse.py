from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _


class SecurityPulse:
    id = models.BigAutoField(_("security_pullse_id"), primary=True)
    security_pulse_title = models.CharField(_("security_pulse_title"), null=True, max_length=400,
                                            help_text=_("security_pulse_title"))
    # ArrayFields
    incident_id = ArrayField(
        models.SmallIntegerField(),
        default=list,
        help_text=_("incident_id"),
        verbose_name=_("incident_id"),
    )
    selected_assets = ArrayField(models.CharField(max_length=255), verbose_name=_("selected_assets"), default=list,
                                 help_text=_("selected assets"))
    selected_entities = ArrayField(models.CharField(max_length=255), verbose_name=_("selected_entities"), default=list,
                                   help_text=_("selected entities"))
