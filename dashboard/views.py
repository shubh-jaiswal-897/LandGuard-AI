from django.shortcuts import render
from django.db.models import Sum, Avg
from dashboard.models import Project
from alerts.models import Alert
from prediction.models import Prediction

def index(request):
    # Calculate real data metrics
    total_area_qs = Project.objects.aggregate(total=Sum('total_land_area'))
    total_area = total_area_qs['total'] or 0
    
    acquired_area_qs = Project.objects.aggregate(total=Sum('acquired_land_area'))
    acquired_area = acquired_area_qs['total'] or 0

    active_alerts = Alert.objects.filter(status='Open')
    active_alerts_count = active_alerts.count()
    
    recent_alerts = active_alerts.order_by('-created_at')[:5]

    avg_delay_qs = Prediction.objects.aggregate(avg=Avg('delay_probability'))
    avg_delay = avg_delay_qs['avg'] or 0
    # Inverting delay probability to show 'On-Time Probability' as a positive metric
    on_time_probability = 100 - float(avg_delay) if avg_delay else 100

    context = {
        'total_area': round(float(total_area), 2),
        'acquired_area': round(float(acquired_area), 2),
        'active_alerts_count': active_alerts_count,
        'recent_alerts': recent_alerts,
        'on_time_probability': round(on_time_probability, 1),
    }

    return render(request, 'dashboard/index.html', context)

def prediction_view(request):
    predictions = Prediction.objects.all()
    return render(request, 'dashboard/prediction.html', {'predictions': predictions})

def map_view(request):
    projects = Project.objects.all()
    return render(request, 'dashboard/map.html', {'projects': projects})

def alerts_view(request):
    alerts = Alert.objects.all().order_by('-created_at')
    return render(request, 'dashboard/alerts.html', {'alerts': alerts})

def recommendations_view(request):
    return render(request, 'dashboard/recommendations.html', {})

def documents_view(request):
    return render(request, 'dashboard/documents.html', {})
