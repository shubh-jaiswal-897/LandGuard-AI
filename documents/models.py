from django.db import models
from dashboard.models import Project

class Document(models.Model):
    DOCUMENT_TYPES = (
        ('GAZETTE', 'Gazette Notification (Sec 11/19)'),
        ('LEGAL', 'High Court / Revenue Order'),
        ('COMPENSATION', 'Compensation Disbursement Record'),
        ('ENVIRONMENTAL', 'Forest & CRZ Clearance'),
        ('SURVEY', 'Cadastral Map & Boundary Survey'),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=255)
    doc_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    file_size = models.CharField(max_length=20, default='1.2 MB')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, default='Verified')

    def __str__(self):
        return f"{self.title} ({self.project.project_name})"

