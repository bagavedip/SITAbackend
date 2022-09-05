from django.db import models
from django.utils.translation import gettext_lazy as _


class Process(models.Model):
    """
    Model to hold Process data
    """
    id = models.BigAutoField(_("id"), primary_key=True)
    process = models.CharField(_("process"), max_length=50, null=True, help_text="Process Name")
    
    def __str__(self):
        return self.process
