
from django.db import models


class Process(models.Model):
    id = models.BigAutoField(primary_key=True)
    process = models.CharField(max_length=50, null=True, help_text="Process Name")
    
    def __str__(self):
        return self.process
