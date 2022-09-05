from django.db import models
from django.utils.translation import gettext as _


class AssignTask(models.Model):

    selectedIncidents = models.CharField(_("assign_user"), max_length=200, unique=True, help_text=_("assigned user"))
    userName = models.CharField(_("assign_user"), max_length=200, help_text=_("assigned user"))
