from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'doc_type', 'reference_number', 'uploaded_at', 'status')
    list_filter = ('doc_type', 'status')
    search_fields = ('title', 'reference_number', 'project__project_name')

