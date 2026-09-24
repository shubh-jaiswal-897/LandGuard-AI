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
