from django.db import models
from .usecase import UseCase


class Rule(models.Model):
    """
    Model to hold data for SOAR data
    """
    rule_name = models.CharField(max_length=200, help_text="Rule Name")
    description = models.CharField(max_length=200, help_text="Description")
    default = models.CharField(max_length=200, help_text="Default")
    usecase = models.ForeignKey(UseCase, on_delete = models.CASCADE, related_name="+")
    