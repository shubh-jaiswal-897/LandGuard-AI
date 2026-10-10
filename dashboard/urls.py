from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('prediction/', views.prediction_view, name='prediction'),
    path('map/', views.map_view, name='map'),
    path('alerts/', views.alerts_view, name='alerts'),
    path('alerts/<int:alert_id>/resolve/', views.resolve_alert, name='resolve_alert'),
    path('projects/', views.projects_view, name='projects'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<str:project_id>/edit/', views.project_edit, name='project_edit'),
    path('projects/<str:project_id>/delete/', views.project_delete, name='project_delete'),
    path('projects/<str:project_id>/detail/', views.project_detail_api, name='project_detail_api'),
    path('recommendations/', views.recommendations_view, name='recommendations'),
    path('documents/', views.documents_view, name='documents'),
    path('reports/', views.reports_view, name='reports'),
    path('settings/', views.settings_view, name='settings'),
    path('run-ai-predictions/', views.run_ai_predictions, name='run_ai_predictions'),
    path('alerts/<int:alert_id>/ai-resolve/', views.get_ai_resolution, name='get_ai_resolution'),
    path('ai-recommendations/', views.generate_global_recommendations, name='generate_global_recommendations'),
    path('sync-live-data/', views.sync_live_data, name='sync_live_data'),
    path('ai-copilot/', views.ai_copilot_api, name='ai_copilot_api'),
]
