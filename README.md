# LandGuard AI

LandGuard AI is a comprehensive Django-based infrastructure project management and risk prediction system. It leverages real-world data and Artificial Intelligence (AI) to track land acquisition progress, predict potential delays (due to legal, compensation, or rehabilitation issues), and visualize project scopes interactively.

## Features

- **Dashboard:** At-a-glance metrics of total land area, acquired land, active alerts, and overall on-time probability for infrastructure projects.
- **AI Prediction Engine:** Machine Learning prediction records mapping out the risk level (Low, Medium, High, Critical) and probabilities of delays.
- **Interactive GIS Map:** (Mocked/Static layout ready for Leaflet/Folium integration) Spatial overview of active projects in India.
- **Smart Alerts:** Automated tracking and severity coding for risks such as "Legal Dispute Delay" or "Compensation Protest".
- **AI Model Configuration:** Admin interface to dynamically switch between AI providers (OpenAI, Google Gemini, Custom REST API) for generating predictions.
- **Recommendations Engine:** Suggested actions for clearing bottlenecks (Legal Dispute Resolution, Compensation Disbursement, Rehabilitation Planning).

## Tech Stack

- **Backend:** Python, Django 6.1
- **Frontend:** HTML, Vanilla CSS (Glassmorphism design, Custom CSS tokens, Animations)
- **Database:** SQLite (default)

## Setup Instructions

### 1. Prerequisites
- Python 3.9+
- Virtual Environment (`venv`)

### 2. Installation
Clone the repository and navigate to the project folder:
```bash
cd LandGuard-AI/AI_Land_Prediction
```

Activate the virtual environment:
```bash
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Database Setup
Apply migrations to set up the SQLite database:
```bash
python manage.py makemigrations
python manage.py migrate
```

Create a superuser to access the Django Admin panel:
```bash
python manage.py createsuperuser
```

### 4. Populating Real-World Data
You can populate the database with 10 real-world massive infrastructure projects across India (e.g., Jewar Airport, Dholera Solar Park) along with generated AI predictions and alerts:
```bash
python populate_db.py
```

### 5. Running the Application
Start the development server:
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` to view the Dashboard.
Visit `http://127.0.0.1:8000/admin/` to manage Projects, AI Models, and Alerts.

## AI Model Automation
In the Django Admin (`/admin`), navigate to **Prediction > AI Model Configurations**. You can add your API keys for models like Google Gemini or OpenAI GPT. The `is_active` flag ensures only one model is used globally for automation tasks.

## Next Steps / Roadmap
- Implement Leaflet.js for dynamic geo-spatial plotting on the GIS Map.
- Connect the `AIModelConfiguration` to real API endpoints for live delay predictions.
- Build OCR pipeline for the Document Vault.
