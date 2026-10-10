from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('ADMINISTRATOR', 'Administrator (Full Access)'),
        ('AUTHORITY', 'Authority / Officer (Manage & Predict)'),
        ('VIEWER', 'Viewer (Read-Only)'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='AUTHORITY')
    department = models.CharField(max_length=150, default='Ministry of Infrastructure')
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"
