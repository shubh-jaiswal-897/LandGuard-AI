from django.contrib import admin
from .models import Project, LandAcquisition, GovernmentAPIConfig

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_id', 'project_name', 'state', 'district', 'project_status')
    search_fields = ('project_id', 'project_name', 'state', 'district')
    list_filter = ('project_status', 'state')

@admin.register(LandAcquisition)
class LandAcquisitionAdmin(admin.ModelAdmin):
    list_display = ('acquisition_id', 'project', 'acquired_area', 'pending_area', 'compensation_pending')
    search_fields = ('acquisition_id', 'project__project_name')

@admin.register(GovernmentAPIConfig)
class GovernmentAPIConfigAdmin(admin.ModelAdmin):
    list_display = ('api_name', 'base_url', 'is_active', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('api_name', 'base_url')
