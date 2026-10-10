import json
from django.test import TestCase, Client
from django.urls import reverse
from dashboard.models import Project, LandAcquisition
from prediction.models import Prediction

class DashboardAndProjectsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.project = Project.objects.create(
            project_id='PRJ-INIT-101',
            project_name='Mumbai Metro Line 4',
            project_type='Urban Rail',
            state='Maharashtra',
            district='Thane',
            total_land_area=500.0,
            acquired_land_area=350.0,
            project_status='Active'
        )
        Prediction.objects.create(
            project=self.project,
            delay_probability=42.50,
            risk_level='MEDIUM'
        )

    def test_dashboard_index_view(self):
        response = self.client.get(reverse('dashboard:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'LandGuard AI')
        self.assertIn('total_projects', response.context)
        self.assertEqual(response.context['total_projects'], 1)

    def test_projects_list_view(self):
        response = self.client.get(reverse('dashboard:projects'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mumbai Metro Line 4')

    def test_project_create_success(self):
        response = self.client.post(reverse('dashboard:project_create'), {
            'project_id': 'PRJ-NEW-202',
            'project_name': 'Dedicated Freight Corridor',
            'project_type': 'Railway',
            'state': 'Haryana',
            'district': 'Rewari',
            'total_land_area': '1200.0',
            'acquired_land_area': '400.0',
            'project_status': 'Planning'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Project.objects.filter(project_id='PRJ-NEW-202').exists())
        new_project = Project.objects.get(project_id='PRJ-NEW-202')
        self.assertTrue(hasattr(new_project, 'prediction'))

    def test_project_create_validation_error(self):
        # Attempt to create project with invalid negative land area
        response = self.client.post(reverse('dashboard:project_create'), {
            'project_id': 'PRJ-INVALID',
            'project_name': 'Invalid Project',
            'project_type': 'Highway',
            'state': 'State',
            'district': 'District',
            'total_land_area': '-100.0',
            'acquired_land_area': '50.0',
            'project_status': 'Planning'
        })
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Project.objects.filter(project_id='PRJ-INVALID').exists())

    def test_project_detail_api(self):
        response = self.client.get(reverse('dashboard:project_detail_api', kwargs={'project_id': self.project.project_id}))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['project']['name'], 'Mumbai Metro Line 4')

    def test_project_edit(self):
        response = self.client.post(reverse('dashboard:project_edit', kwargs={'project_id': self.project.project_id}), {
            'project_name': 'Mumbai Metro Line 4 Extended',
            'project_type': 'Urban Rail',
            'state': 'Maharashtra',
            'district': 'Thane',
            'total_land_area': '500.0',
            'acquired_land_area': '450.0',
            'project_status': 'Active'
        })
        self.assertEqual(response.status_code, 302)
        self.project.refresh_from_db()
        self.assertEqual(self.project.project_name, 'Mumbai Metro Line 4 Extended')

    def test_project_delete(self):
        response = self.client.post(reverse('dashboard:project_delete', kwargs={'project_id': self.project.project_id}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Project.objects.filter(project_id='PRJ-INIT-101').exists())

    def test_ai_copilot_api(self):
        response = self.client.post(
            reverse('dashboard:ai_copilot_api'),
            data=json.dumps({'query': 'Which projects have high risk?'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('answer', data)

    def test_sync_live_data(self):
        response = self.client.post(reverse('dashboard:sync_live_data'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
