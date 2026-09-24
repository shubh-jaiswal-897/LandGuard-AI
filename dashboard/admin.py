from django.contrib import admin
from .models import Project, LandAcquisition

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_id', 'project_name', 'state', 'district', 'project_status')
    search_fields = ('project_id', 'project_name', 'state', 'district')
    list_filter = ('project_status', 'state')

@admin.register(LandAcquisition)
class LandAcquisitionAdmin(admin.ModelAdmin):
    list_display = ('acquisition_id', 'project', 'acquired_area', 'pending_area', 'compensation_pending')
    search_fields = ('acquisition_id', 'project__project_name')
