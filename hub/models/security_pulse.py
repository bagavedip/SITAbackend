from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _


class SecurityPulse(models.Model):
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
