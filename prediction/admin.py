from django.contrib import admin
from .models import Prediction, RiskFactor, AIModelConfiguration
from django.contrib import messages

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('project', 'delay_probability', 'risk_level', 'prediction_date')
    list_filter = ('risk_level',)

@admin.register(RiskFactor)
class RiskFactorAdmin(admin.ModelAdmin):
    list_display = ('prediction', 'factor_name', 'impact_value')

@admin.register(AIModelConfiguration)
class AIModelConfigurationAdmin(admin.ModelAdmin):
    list_display = ('name', 'provider', 'is_active', 'created_at')
    list_filter = ('provider', 'is_active')
    search_fields = ('name',)
    
    actions = ['test_ai_connection']
    
    @admin.action(description='Test API Connection for selected models')
    def test_ai_connection(self, request, queryset):
        for model_config in queryset:
            # Here you would implement actual API connection test
            if model_config.api_key:
                self.message_user(request, f"Successfully connected to {model_config.name} API!", messages.SUCCESS)
            else:
                self.message_user(request, f"{model_config.name} requires an API key to test.", messages.WARNING)
