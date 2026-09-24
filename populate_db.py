import os
import django
import random
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from dashboard.models import Project, LandAcquisition
from alerts.models import Alert
from prediction.models import Prediction, RiskFactor

def populate():
    # Clear existing data to avoid duplicates if run multiple times
    Project.objects.all().delete()
    
    projects_data = [
        {
            "id": "PROJ-IN-001", "name": "Navi Mumbai International Airport", "type": "Airport", 
            "state": "Maharashtra", "district": "Raigad", "lat": 18.993, "lon": 73.069,
            "total_area": 1160, "acquired_area": 1160, "status": "Active"
        },
        {
            "id": "PROJ-IN-002", "name": "Noida International Airport (Jewar)", "type": "Airport", 
            "state": "Uttar Pradesh", "district": "Gautam Buddha Nagar", "lat": 28.199, "lon": 77.558,
            "total_area": 5000, "acquired_area": 1334, "status": "Active"
        },
        {
            "id": "PROJ-IN-003", "name": "Mumbai-Ahmedabad High Speed Rail (Surat Segment)", "type": "Railway", 
            "state": "Gujarat", "district": "Surat", "lat": 21.170, "lon": 72.831,
            "total_area": 800, "acquired_area": 750, "status": "Active"
        },
        {
            "id": "PROJ-IN-004", "name": "Dholera Solar Park", "type": "Renewable Energy", 
            "state": "Gujarat", "district": "Ahmedabad", "lat": 22.253, "lon": 72.195,
            "total_area": 11000, "acquired_area": 11000, "status": "Active"
        },
        {
            "id": "PROJ-IN-005", "name": "Polavaram Irrigation Project", "type": "Irrigation", 
            "state": "Andhra Pradesh", "district": "Eluru", "lat": 17.247, "lon": 81.652,
            "total_area": 40000, "acquired_area": 35000, "status": "Delayed"
        },
        {
            "id": "PROJ-IN-006", "name": "Kaleshwaram Lift Irrigation", "type": "Irrigation", 
            "state": "Telangana", "district": "Jayashankar Bhupalpally", "lat": 18.746, "lon": 79.824,
            "total_area": 8000, "acquired_area": 7900, "status": "Completed"
        },
        {
            "id": "PROJ-IN-007", "name": "Delhi-Mumbai Expressway (Haryana Segment)", "type": "Highway", 
            "state": "Haryana", "district": "Gurugram", "lat": 28.459, "lon": 77.026,
            "total_area": 1200, "acquired_area": 1050, "status": "Active"
        },
        {
            "id": "PROJ-IN-008", "name": "Purvanchal Expressway", "type": "Highway", 
            "state": "Uttar Pradesh", "district": "Lucknow", "lat": 26.846, "lon": 80.946,
            "total_area": 2500, "acquired_area": 2500, "status": "Completed"
        },
        {
            "id": "PROJ-IN-009", "name": "Navalur IT Park Expansion", "type": "Infrastructure", 
            "state": "Tamil Nadu", "district": "Chennai", "lat": 12.845, "lon": 80.226,
            "total_area": 300, "acquired_area": 120, "status": "Planning"
        },
        {
            "id": "PROJ-IN-010", "name": "Kochi Metro Phase 2", "type": "Railway", 
            "state": "Kerala", "district": "Ernakulam", "lat": 9.981, "lon": 76.299,
            "total_area": 150, "acquired_area": 45, "status": "Planning"
        }
    ]

    for p_data in projects_data:
        proj = Project.objects.create(
            project_id=p_data["id"],
            project_name=p_data["name"],
            project_type=p_data["type"],
            state=p_data["state"],
            district=p_data["district"],
            latitude=p_data["lat"],
            longitude=p_data["lon"],
            total_land_area=p_data["total_area"],
            acquired_land_area=p_data["acquired_area"],
            project_status=p_data["status"]
        )

        # Create Land Acquisition
        LandAcquisition.objects.create(
            acquisition_id=f"ACQ-{p_data['id']}",
            project=proj,
            land_owner_count=random.randint(50, 500),
            acquired_area=p_data["acquired_area"],
            pending_area=p_data["total_area"] - p_data["acquired_area"],
            compensation_pending=proj.project_status != "Completed"
        )

        # Create Prediction
        delay_prob = random.uniform(5.0, 95.0)
        risk = 'LOW'
        if delay_prob > 75: risk = 'CRITICAL'
        elif delay_prob > 50: risk = 'HIGH'
        elif delay_prob > 25: risk = 'MEDIUM'

        pred = Prediction.objects.create(
            project=proj,
            delay_probability=round(delay_prob, 2),
            risk_level=risk
        )

        # Risk Factors
        RiskFactor.objects.create(prediction=pred, factor_name="Legal Disputes", impact_value=round(random.uniform(0.1, 0.9), 2), explanation="Ongoing land ownership disputes.")
        
        # Create Alerts
        if risk in ['HIGH', 'CRITICAL'] or p_data["status"] == "Delayed":
            Alert.objects.create(
                project=proj,
                alert_type="Legal Dispute Delay" if random.choice([True, False]) else "Compensation Protest",
                severity="CRITICAL" if risk == 'CRITICAL' else "WARNING",
                message=f"High risk of delay detected due to land acquisition protests in {p_data['district']}.",
                status="Open"
            )

    print("Successfully populated database with 10 real-world projects!")

if __name__ == '__main__':
    populate()
