# users/tests/test_views.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class UserRegistrationViewTestCase(TestCase):
    def test_user_registration(self):
        url = reverse('users:register')

        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)

        user_exists = User.objects.filter(username='testuser').exists()
        self.assertTrue(user_exists)

class UserLoginViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword123')

    def test_user_login(self):
        url = reverse('users:login')

        # Login with valid credentials
        data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }

        response = self.client.post(url, data)

        # Check if the user is redirected to the home page after successful login
        self.assertRedirects(response, '/')

        # Verify the user is logged in by checking the session
        response = self.client.get('/')
        self.assertContains(response, "Welcome, testuser!")
