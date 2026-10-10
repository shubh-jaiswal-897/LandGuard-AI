import os
import django
import random
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from dashboard.models import Project, LandAcquisition
from alerts.models import Alert
from prediction.models import Prediction, RiskFactor

from documents.models import Document
from recommendations.models import Recommendation

def populate():
    # Clear existing data to avoid duplicates if run multiple times
    Project.objects.all().delete()
    Document.objects.all().delete()
    Recommendation.objects.all().delete()
    
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

        # Create Prediction & XAI Risk Factors via AI prediction engine
        from prediction.utils import generate_prediction_for_project
        pred = generate_prediction_for_project(proj)
        risk = pred.risk_level

        # Create Alerts
        if risk in ['HIGH', 'CRITICAL'] or p_data["status"] == "Delayed":
            Alert.objects.create(
                project=proj,
                alert_type="Legal Dispute Delay" if random.choice([True, False]) else "Compensation Protest",
                severity="CRITICAL" if risk == 'CRITICAL' else "WARNING",
                message=f"High risk of delay detected due to land acquisition disputes in {p_data['district']}.",
                status="Open"
            )

        # Create Official Documents
        Document.objects.create(
            project=proj,
            title=f"LARR Gazette Notification Sec 11 - {proj.project_name}",
            doc_type="GAZETTE",
            reference_number=f"GZ-{proj.project_id}-2024",
            file_size="2.4 MB",
            status="Verified"
        )
        Document.objects.create(
            project=proj,
            title=f"Environmental & Forest Clearance Certificate",
            doc_type="ENVIRONMENTAL",
            reference_number=f"ENV-{proj.project_id}-NOC",
            file_size="1.8 MB",
            status="Verified" if proj.project_status != "Delayed" else "Pending Review"
        )
        Document.objects.create(
            project=proj,
            title=f"Compensation Disbursement Ledger",
            doc_type="COMPENSATION",
            reference_number=f"CMP-{proj.project_id}-R4",
            file_size="3.1 MB",
            status="Verified"
        )

        # Create Strategic Recommendations
        if risk in ['HIGH', 'CRITICAL']:
            Recommendation.objects.create(
                project=proj,
                recommendation=f"Deploy Fast-Track Revenue Tribunal & Negotiated Compensation Committee in {proj.district}.",
                priority="HIGH",
                reason=f"Project is facing {pred.delay_probability}% delay probability due to {proj.total_land_area - proj.acquired_land_area} ha pending land."
            )
        else:
            Recommendation.objects.create(
                project=proj,
                recommendation=f"Finalize cadastral land mutation and pillar marking with Tehsildar office.",
                priority="MEDIUM",
                reason=f"Acquisition progress is on track at {round(proj.acquired_land_area/proj.total_land_area*100, 1)}%."
            )

    from django.contrib.auth.models import User
    from accounts.models import UserProfile

    user, created = User.objects.get_or_create(username='shubh1111', defaults={'email': 'shubh1111@landguard.gov.in', 'is_staff': True, 'is_superuser': True})
    user.set_password('shubh1111')
    user.is_staff = True
    user.is_superuser = True
    user.save()

    profile, _ = UserProfile.objects.get_or_create(user=user)
    profile.role = 'ADMINISTRATOR'
    profile.department = 'Ministry of Infrastructure'
    profile.save()

    print("Successfully populated database and configured superuser shubh1111!")

if __name__ == '__main__':
    populate()

