from django.db import models
from dashboard.models import Project

class Alert(models.Model):
    SEVERITY_CHOICES = (
        ('INFO', 'Information'),
        ('WARNING', 'Warning'),
        ('CRITICAL', 'Critical'),
    )
    STATUS_CHOICES = (
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='alerts')
    alert_type = models.CharField(max_length=100)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    message = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Open')
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.severity} Alert for {self.project.project_name}: {self.alert_type}"
