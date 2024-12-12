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

