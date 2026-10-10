from django.test import TestCase
from dashboard.models import Project
from prediction.models import Prediction, RiskFactor
from prediction.utils import calculate_analytical_risk, generate_prediction_for_project

class PredictionEngineTestCase(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            project_id='TEST-PRJ-001',
            project_name='Delhi Eastern Peripheral Expressway',
            project_type='Highway',
            state='Delhi',
            district='East Delhi',
            total_land_area=1000.0,
            acquired_land_area=400.0,
            project_status='Delayed',
            compensation_status='Pending',
            legal_dispute_status='High'
        )

    def test_analytical_risk_calculation(self):
        result = calculate_analytical_risk(self.project)
        self.assertIn('delay_probability', result)
        self.assertIn('risk_level', result)
        self.assertIn('risk_factors', result)
        
        prob = result['delay_probability']
        self.assertGreaterEqual(prob, 0.0)
        self.assertLessEqual(prob, 100.0)
        self.assertIn(result['risk_level'], ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'])

    def test_generate_prediction_for_project(self):
        pred = generate_prediction_for_project(self.project)
        self.assertEqual(pred.project, self.project)
        self.assertGreaterEqual(float(pred.delay_probability), 0.0)
        self.assertLessEqual(float(pred.delay_probability), 100.0)
        self.assertTrue(pred.risk_factors.exists())

    def test_prediction_recalculation_on_land_update(self):
        # Update project land acquisition to 950/1000 (95% complete)
        self.project.acquired_land_area = 950.0
        self.project.compensation_status = 'Completed'
        self.project.legal_dispute_status = 'No Disputes'
        self.project.save()

        updated_pred = generate_prediction_for_project(self.project)
        # Delay probability should drop significantly
        self.assertLess(float(updated_pred.delay_probability), 60.0)
