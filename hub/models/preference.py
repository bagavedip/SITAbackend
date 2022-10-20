from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User


class Preference(models.Model):
    """
    Model to hold the user's last used preferences
    """
    graph = models.IntegerField(_("graph"), help_text=_("graph"), null=True)
    graph_name = models.CharField(_("graph_name"), max_length=20000, help_text=_("graph name"), null=True)
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        db_index=False,
        verbose_name=_("User's Defaults"),
        help_text=_("User's Defaults"),
        related_name="+",
    )
    value = models.IntegerField(_("value"), help_text=_("value"), null=True)

    def __str__(self):
        return self.user_id + "preference"
