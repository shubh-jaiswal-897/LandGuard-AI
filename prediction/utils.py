import json
import google.generativeai as genai
from .models import Prediction, RiskFactor, AIModelConfiguration

def generate_prediction_for_project(project):
    # Get active AI configuration
    config = AIModelConfiguration.objects.filter(is_active=True, provider='GEMINI').first()
    
    if not config or not config.api_key:
        raise Exception("No active Gemini AI configuration found. Please add it in the Admin panel.")
    
    # Configure Gemini
    genai.configure(api_key=config.api_key)
    
    # Use the stable gemini-2.5-flash model
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # Construct the prompt
    prompt = f"""
    You are an expert AI for Land Acquisition predictive analytics.
    Analyze the following project and predict the likelihood of delays.
    
    Project Name: {project.project_name}
    State: {project.state}
    District: {project.district}
    Total Land Area: {project.total_land_area} hectares
    Acquired Area: {project.acquired_land_area} hectares
    Pending Area: {project.pending_land_area} hectares
    Compensation Status: {project.compensation_status}
    Legal Disputes: {project.legal_dispute_status}
    Approval Status: {project.approval_status}
    Possession Status: {project.possession_status}
    
    Based on this data, provide a structured JSON response with exactly this schema:
    {{
        "delay_probability": <number from 0 to 100>,
        "risk_level": "<one of: LOW, MEDIUM, HIGH, CRITICAL>",
        "risk_factors": [
            {{
                "factor_name": "<name of the factor, e.g., 'Legal Litigation', 'High Pending Area'>",
                "impact_value": <number from 0.0 to 1.0 representing how much this factor contributes to the risk>,
                "explanation": "<short explanation>"
            }},
            ... (provide 2 to 4 key risk factors)
        ]
    }}
    """
    
    response = model.generate_content(prompt)
    
    try:
        raw_text = response.text.strip()
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        elif raw_text.startswith("```"):
            raw_text = raw_text[3:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
        
        data = json.loads(raw_text.strip())
        
        # Save Prediction
        prediction, created = Prediction.objects.update_or_create(
            project=project,
            defaults={
                'delay_probability': data.get('delay_probability', 50),
                'risk_level': data.get('risk_level', 'MEDIUM'),
                'model_name': 'Gemini AI',
                'model_version': '1.0'
            }
        )
        
        # Clear old factors and save new ones
        prediction.risk_factors.all().delete()
        
        for factor in data.get('risk_factors', []):
            RiskFactor.objects.create(
                prediction=prediction,
                factor_name=factor.get('factor_name', 'Unknown'),
                impact_value=factor.get('impact_value', 0.5),
                explanation=factor.get('explanation', '')
            )
            
        return prediction
    except Exception as e:
        raise Exception(f"Failed to parse AI response: {str(e)}\nResponse was: {response.text}")
