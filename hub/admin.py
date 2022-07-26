from django.contrib import admin
from .models.siem_data import SIEM


@admin.register(SIEM)
class SiemAdmin(admin.ModelAdmin):
    pass
