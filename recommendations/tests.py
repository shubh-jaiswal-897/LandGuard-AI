from django.test import TestCase, Client
from django.urls import reverse
from dashboard.models import Project
from recommendations.models import Recommendation

class RecommendationsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.project = Project.objects.create(
            project_id='PRJ-REC-01',
            project_name='Amaravati Capital City Express Highway',
            project_type='Highway',
            state='Andhra Pradesh',
            district='Guntur',
            total_land_area=850.0,
            acquired_land_area=400.0,
            project_status='Delayed'
        )
        self.rec = Recommendation.objects.create(
            project=self.project,
            recommendation='Form emergency negotiated compensation panel under RFCTLARR Section 19.',
            priority='HIGH',
            reason='Acquisition progress is lagging behind scheduled possession target by 14 months.'
        )

    def test_recommendations_view(self):
        response = self.client.get(reverse('dashboard:recommendations'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Amaravati Capital City Express Highway')

    def test_generate_global_recommendations_api(self):
        response = self.client.get(reverse('dashboard:generate_global_recommendations'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('recommendations', data)
        self.assertTrue(len(data['recommendations']) >= 1)
