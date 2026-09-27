from django.shortcuts import render, redirect
from django.contrib import messages
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

def run_ai_predictions(request):
    from prediction.utils import generate_prediction_for_project
    from dashboard.models import Project
    try:
        projects = Project.objects.all()[:3] # Limit to 3 for demo
        for p in projects:
            generate_prediction_for_project(p)
        messages.success(request, f"Successfully ran Gemini AI predictions for {projects.count()} projects.")
    except Exception as e:
        messages.error(request, f"AI Error: {str(e)}")
    return redirect('dashboard:prediction')

def get_ai_resolution(request, alert_id):
    from django.http import JsonResponse
    import google.generativeai as genai
    from dashboard.models import GovernmentAPIConfig
    import json
    
    try:
        alert = Alert.objects.get(id=alert_id)
        config = GovernmentAPIConfig.objects.filter(is_active=True, provider='GEMINI').first()
        
        if not config or not config.api_key:
            return JsonResponse({'error': 'No active Gemini AI configuration found. Please add it in the Admin panel.'}, status=400)
            
        genai.configure(api_key=config.api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""
        You are an expert government infrastructure and project management AI.
        A system alert has been triggered for a construction/land acquisition project.
        Project Name: {alert.project.project_name}
        Alert Type: {alert.alert_type}
        Alert Message: {alert.message}
        Severity: {alert.severity}
        
        Provide exactly 3 clear, concise, and actionable steps to resolve this issue.
        Return ONLY a JSON array of 3 strings. Example: ["Step 1 description", "Step 2 description", "Step 3 description"]
        """
        
        response = model.generate_content(prompt)
        raw_text = response.text.strip()
        
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        elif raw_text.startswith("```"):
            raw_text = raw_text[3:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
            
        steps = json.loads(raw_text.strip())
        
        # Ensure it's a list
        if not isinstance(steps, list):
            steps = ["Investigate the root cause immediately.", "Notify the relevant stakeholders.", "Update the project timeline to reflect any delays."]
            
        return JsonResponse({'steps': steps})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def generate_global_recommendations(request):
    from django.http import JsonResponse
    import google.generativeai as genai
    from dashboard.models import GovernmentAPIConfig, Project
    from alerts.models import Alert
    import json
    
    try:
        config = GovernmentAPIConfig.objects.filter(is_active=True, provider='GEMINI').first()
        if not config or not config.api_key:
            return JsonResponse({'error': 'No active Gemini AI configuration found.'}, status=400)
            
        # Gather context
        projects = Project.objects.all()[:5]
        active_alerts = Alert.objects.filter(status='Open')[:5]
        
        context_str = "Recent Projects:\n"
        for p in projects:
            context_str += f"- {p.project_name} (Land Acquired: {p.acquired_land_area}/{p.total_land_area} acres)\n"
            
        context_str += "\nActive Alerts:\n"
        for a in active_alerts:
            context_str += f"- {a.alert_type}: {a.message} (Severity: {a.severity})\n"
            
        genai.configure(api_key=config.api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""
        You are an expert government infrastructure AI advisor.
        Based on the following system state:
        
        {context_str}
        
        Provide exactly 3 strategic, high-level recommendations to improve project efficiency, reduce delays, or mitigate risks.
        Return the response ONLY as a valid JSON array of objects. Each object must have these exact keys:
        - "title" (Short string, e.g., "Legal Dispute Resolution")
        - "description" (Detailed action plan, 2 sentences max)
        - "icon" (A FontAwesome icon class, e.g., "fa-scale-balanced", "fa-money-bill-wave", "fa-house-chimney", "fa-gavel", "fa-handshake")
        - "color_theme" (Must be exactly one of these strings: "blue", "green", "purple")
        
        Make sure the output is pure JSON. Example:
        [{{ "title": "...", "description": "...", "icon": "fa-gavel", "color_theme": "blue" }}]
        """
        
        response = model.generate_content(prompt)
        raw_text = response.text.strip()
        
        if raw_text.startswith("```json"): raw_text = raw_text[7:]
        elif raw_text.startswith("```"): raw_text = raw_text[3:]
        if raw_text.endswith("```"): raw_text = raw_text[:-3]
            
        recommendations = json.loads(raw_text.strip())
        
        if not isinstance(recommendations, list):
            raise Exception("Invalid JSON structure returned by AI.")
            
        return JsonResponse({'recommendations': recommendations})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
