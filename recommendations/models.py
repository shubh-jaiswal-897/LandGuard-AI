from django.db import models
from dashboard.models import Project

class Recommendation(models.Model):
    PRIORITY_CHOICES = (
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='recommendations')
    recommendation = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.priority} Recommendation for {self.project.project_name}"
