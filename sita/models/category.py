from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    """
    Models to hold category data
    """
    id = models.BigAutoField(_("id"), primary_key=True)
    category = models.CharField(_("category"), max_length=50, null=True, help_text=_("Category Name"))
    
    def __str__(self):
        return self.category
