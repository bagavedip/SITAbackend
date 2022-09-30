from django.db import models
from django.utils.translation import gettext as _


class SOAR(models.Model):
    """
    Model to hold data for SOAR data
    """
    SOAR_ID = models.IntegerField( null= True,help_text="SOAR Id")
    AssignedUser = models.CharField(max_length=200, null= True, help_text="Assigned User")
    Title = models.CharField(max_length=200, null= True, help_text="Title")
    Time = models.DateTimeField(max_length=200, null= True, help_text="Time")
    Tags = models.CharField(max_length=200, null= True, help_text="Tags")
    Products = models.CharField(max_length=200, null= True, help_text="Product")
    Incident = models.BooleanField( null= True,help_text="Incident")
    Suspicious = models.BooleanField( null= True,help_text="Suspicious")
    Important = models.BooleanField( null= True,help_text="Important")
    Ports = models.IntegerField( null= True,help_text="Ports")
    Outcomes = models.CharField(max_length=200, null= True, help_text="Outcomes")
    Status = models.CharField(max_length=200, null= True, help_text="Status")
    Environment = models.CharField(max_length=200, null= True, help_text="Environment")
    Priority = models.CharField(max_length=200, null= True, help_text="Priority")
    Stage = models.CharField(max_length=200, null= True, help_text="Stage")
    TicketIDs = models.CharField(max_length=200, help_text="Ticket Ids")
    ClosingTime = models.DateTimeField(max_length=200, null= True, help_text="Closing Time")
    Sources = models.CharField(max_length=200, null= True, help_text="Sources")
    Reason = models.CharField(max_length=200, null= True, help_text="Reason")
    RootCause = models.CharField(max_length=200, null= True, help_text="Root Cause")
    Case_id = models.CharField(null = True, max_length=200, help_text="Case Id")

