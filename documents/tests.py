from django.test import TestCase, Client
from django.urls import reverse
from dashboard.models import Project
from documents.models import Document

class DocumentsVaultTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.project = Project.objects.create(
            project_id='PRJ-DOC-01',
            project_name='Ken-Betwa River Interlinking',
            project_type='Water',
            state='Madhya Pradesh',
            district='Panna',
            total_land_area=2000.0,
            acquired_land_area=800.0,
            project_status='Active'
        )

    def test_documents_view(self):
        response = self.client.get(reverse('dashboard:documents'))
        self.assertEqual(response.status_code, 200)

    def test_document_creation(self):
        response = self.client.post(reverse('dashboard:documents'), {
            'project_id': self.project.project_id,
            'title': 'Section 11 Gazette Notification',
            'doc_type': 'GAZETTE',
            'reference_number': 'GAZ-2026-99'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Document.objects.filter(title='Section 11 Gazette Notification').exists())
