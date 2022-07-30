from django.db import models
from django.utils.translation import gettext_lazy as _
from .functions import Function


class Assets(models.Model):
    """
        Model to hold data of Asset
    """
    
    class AssetType(models.TextChoices):
        Laptop = "Laptop", _("Laptop")
        Mobile = "Mobile", _("Mobile")
        Desktop = "Desktop", _("Desktop")
        Others = "Others", _("Others")

    class Category(models.TextChoices):
        Category1 = "Category1", _("Category1")
        Category2 = "Category2", _("Category2")
        Category3 = "Category3", _("Category3")
        Others = "Others", _("Others")

    class Criticalities(models.TextChoices):
        High = "High", _("High")
        Medium = "Medium", _("Medium")
        Critical = "Critical", _("Critical")

    id = models.BigAutoField(_("id"), primary_key=True)
    AssetName = models.CharField(_("AssetName"), max_length=50, null=True, help_text=_("Asset Name"))
    AssetType = models.CharField(_("AssetType"), max_length=50, choices=AssetType.choices, help_text=_("Asset Types"))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, help_text="Asset Category")
    criticality = models.CharField(_("criticality"), max_length=100, choices=Criticalities.choices,
                                   help_text=_("Criticality"))
    function_id = models.ForeignKey(Function, verbose_name=_("function_id"), on_delete=models.CASCADE,
                                    help_text=_("Function Name"))
    created = models.DateField(_("created"), null=True, auto_now_add=True, help_text=_("created"))
    
    def __str__(self):
        return self.AssetName
