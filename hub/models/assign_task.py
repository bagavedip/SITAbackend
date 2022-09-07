from django.db import models
from django.utils.translation import gettext as _


class AssignTask(models.Model):
    """
     Model for Assign Task
    """
    incident_id = models.CharField(_("incident_id"), max_length=200, unique=True, help_text="incident_id")
    assigned_user = models.CharField(_("assign_user"), max_length=200, null=True, help_text=_("assign_user"))
