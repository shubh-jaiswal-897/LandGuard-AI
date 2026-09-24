from django.contrib import admin
from .models import Alert

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('alert_type', 'project', 'severity', 'status', 'created_at')
    list_filter = ('severity', 'status')
    search_fields = ('alert_type', 'project__project_name')
