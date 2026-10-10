from django.test import TestCase, Client
from django.urls import reverse
from dashboard.models import Project

class GISMapTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.project = Project.objects.create(
            project_id='PRJ-GIS-01',
            project_name='Gujarat Hybrid Renewable Energy Park',
            project_type='Solar/Wind',
            state='Gujarat',
            district='Kutch',
            latitude=23.7337,
            longitude=69.8597,
            total_land_area=72600.0,
            acquired_land_area=50000.0,
            project_status='Active'
        )

    def test_map_view(self):
        response = self.client.get(reverse('dashboard:map'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Gujarat Hybrid Renewable Energy Park')
        self.assertIn('projects_json', response.context)
