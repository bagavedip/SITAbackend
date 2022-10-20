from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User


class DefaultDashboard(models.Model):
    """
    Model to hold the user's last used filters
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        db_index=False,
        verbose_name=_("User's Defaults"),
        help_text=_("User's Defaults"),
        related_name="+",
    )

    location_id = models.CharField(_("location_id"), max_length=20000, help_text=_("location id"), null=True)
    insight_filter = models.CharField(_("insight_filter"), max_length=20000, help_text=_("insight filter"), null=True)
    perspective_filter = models.CharField(_("perspective_filter"), max_length=20000, help_text=_("perspective filter"), null=True)
    oei_filter = models.CharField(_("oei_filter"), max_length=20000, help_text=_("oei filter"), null=True)

    def __str__(self):
        return self.user + "filters"
