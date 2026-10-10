from django.test import TestCase, Client
from django.urls import reverse
from dashboard.models import Project
from alerts.models import Alert

class AlertsSystemTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.project = Project.objects.create(
            project_id='PRJ-ALERT-01',
            project_name='Navi Mumbai International Airport',
            project_type='Airport',
            state='Maharashtra',
            district='Raigad',
            total_land_area=1160.0,
            acquired_land_area=900.0,
            project_status='Delayed'
        )
        self.alert = Alert.objects.create(
            project=self.project,
            alert_type='High Court Litigation',
            severity='CRITICAL',
            message='Stay order issued by High Court regarding papad makers land allotment compensation.',
            status='Open'
        )

    def test_alerts_view(self):
        response = self.client.get(reverse('dashboard:alerts'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'High Court Litigation')
        self.assertEqual(response.context['critical_alerts'], 1)

    def test_resolve_alert(self):
        response = self.client.post(reverse('dashboard:resolve_alert', kwargs={'alert_id': self.alert.id}))
        self.assertEqual(response.status_code, 302)
        self.alert.refresh_from_db()
        self.assertEqual(self.alert.status, 'Resolved')
        self.assertIsNotNone(self.alert.resolved_at)

    def test_get_ai_resolution(self):
        response = self.client.get(reverse('dashboard:get_ai_resolution', kwargs={'alert_id': self.alert.id}))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('steps', data)
        self.assertTrue(len(data['steps']) >= 3)
