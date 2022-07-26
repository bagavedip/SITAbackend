from django.db import models
from django.utils.translation import gettext_lazy as _


class Entity(models.Model):
    id = models.BigAutoField(_("id"), primary_key=True)
    entityname = models.CharField(_("entityname"), max_length=50, null=True, help_text=_("Entity Name"))
    
    def __str__(self):
        return self.entityname
