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
]
