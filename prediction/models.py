from django.db import models
from dashboard.models import Project

class Prediction(models.Model):
    RISK_LEVELS = (
        ('LOW', 'Low Risk'),
        ('MEDIUM', 'Medium Risk'),
        ('HIGH', 'High Risk'),
        ('CRITICAL', 'Critical Risk'),
    )

    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='prediction')
    delay_probability = models.DecimalField(max_digits=5, decimal_places=2, help_text="Probability in percentage")
    risk_level = models.CharField(max_length=20, choices=RISK_LEVELS)
    prediction_date = models.DateTimeField(auto_now_add=True)
    model_name = models.CharField(max_length=100, default='RandomForest_v1')
    model_version = models.CharField(max_length=50, default='1.0')

    def __str__(self):
        return f"{self.project.project_name} - {self.risk_level} ({self.delay_probability}%)"


class RiskFactor(models.Model):
    prediction = models.ForeignKey(Prediction, on_delete=models.CASCADE, related_name='risk_factors')
    factor_name = models.CharField(max_length=255)
    impact_value = models.DecimalField(max_digits=8, decimal_places=4)
    explanation = models.TextField()

    def __str__(self):
        return f"{self.factor_name} ({self.impact_value}) for {self.prediction.project.project_name}"

class AIModelConfiguration(models.Model):
    PROVIDER_CHOICES = (
        ('OPENAI', 'OpenAI (GPT)'),
        ('GEMINI', 'Google Gemini'),
        ('CUSTOM', 'Custom REST API (Self-Hosted)'),
    )

    name = models.CharField(max_length=100, help_text="e.g., Gemini 1.5 Pro")
    provider = models.CharField(max_length=50, choices=PROVIDER_CHOICES)
    api_url = models.URLField(blank=True, null=True, help_text="Leave blank for standard providers (OpenAI/Gemini).")
    api_key = models.CharField(max_length=255, blank=True, null=True, help_text="Your API key for this model.")
    is_active = models.BooleanField(default=False, help_text="Set to True to use this model for automated predictions.")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.is_active:
            # Ensure only one model is active at a time
            AIModelConfiguration.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.get_provider_display()}) - {'ACTIVE' if self.is_active else 'Inactive'}"
