from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('prediction/', views.prediction_view, name='prediction'),
    path('map/', views.map_view, name='map'),
    path('alerts/', views.alerts_view, name='alerts'),
    path('recommendations/', views.recommendations_view, name='recommendations'),
    path('documents/', views.documents_view, name='documents'),
    path('run-ai-predictions/', views.run_ai_predictions, name='run_ai_predictions'),
    path('alerts/<int:alert_id>/ai-resolve/', views.get_ai_resolution, name='get_ai_resolution'),
]
