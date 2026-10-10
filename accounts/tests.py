from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from accounts.models import UserProfile

class AccountsAuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testofficer',
            password='Password123!',
            email='officer@landguard.gov.in'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            role='AUTHORITY',
            department='Ministry of Infrastructure'
        )

    def test_user_profile_creation(self):
        self.assertEqual(self.profile.user.username, 'testofficer')
        self.assertEqual(self.profile.role, 'AUTHORITY')
        self.assertIn('Authority', str(self.profile))

    def test_login_success(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testofficer',
            'password': 'Password123!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard:index'))

    def test_login_invalid_password(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testofficer',
            'password': 'WrongPassword!'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid username or password")

    def test_logout(self):
        self.client.login(username='testofficer', password='Password123!')
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:login'))

    def test_user_profile_api(self):
        self.client.login(username='testofficer', password='Password123!')
        response = self.client.get(reverse('accounts:user_profile_api'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['authenticated'])
        self.assertEqual(data['username'], 'testofficer')
        self.assertEqual(data['role'], 'AUTHORITY')
