from django.db import models

class Project(models.Model):
    PROJECT_STATUS_CHOICES = (
        ('Planning', 'Planning'),
        ('Active', 'Active'),
        ('Delayed', 'Delayed'),
        ('Completed', 'Completed'),
    )

    project_id = models.CharField(max_length=100, unique=True)
    project_name = models.CharField(max_length=255)
    project_type = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    total_land_area = models.DecimalField(max_digits=12, decimal_places=2, help_text="In Hectares")
    acquired_land_area = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    pending_land_area = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    
    compensation_status = models.CharField(max_length=50, default='Pending')
    legal_dispute_status = models.CharField(max_length=50, default='No Disputes')
    approval_status = models.CharField(max_length=50, default='Pending')
    possession_status = models.CharField(max_length=50, default='Pending')
    rehabilitation_status = models.CharField(max_length=50, default='Not Required')
    
    project_status = models.CharField(max_length=50, choices=PROJECT_STATUS_CHOICES, default='Planning')
    expected_completion_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.pending_land_area = float(self.total_land_area) - float(self.acquired_land_area)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.project_id} - {self.project_name}"


class LandAcquisition(models.Model):
    acquisition_id = models.CharField(max_length=100, unique=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='land_acquisitions')
    land_owner_count = models.IntegerField(default=0)
    acquired_area = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    pending_area = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    
    compensation_pending = models.BooleanField(default=True)
    legal_cases = models.IntegerField(default=0)
    possession_status = models.CharField(max_length=50, default='Pending')
    rehabilitation_status = models.CharField(max_length=50, default='Pending')
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Acq: {self.acquisition_id} for {self.project.project_name}"
