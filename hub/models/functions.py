from django.db import models
from .geolocations import GeoLocation
from django.utils.translation import gettext_lazy as _


class Function(models.Model):
    id = models.BigAutoField(_("id"), primary_key=True)
    function_name = models.CharField(_("function_name"), max_length=50, null=True, help_text=_("Function Name"))
    location_id = models.ForeignKey(GeoLocation, verbose_name=_("localtion_id"), on_delete=models.CASCADE,
                                    related_name="+")
    
    def __str__(self):
        return self.function_name
