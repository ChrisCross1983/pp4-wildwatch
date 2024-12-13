from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class UserRegistrationViewTestCase(TestCase):
    def test_user_registration(self):
        url = reverse('users:signup')

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

        data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }

        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('home'))

        response = self.client.get(reverse('home'))
        self.assertContains(response, "Welcome back, testuser!")

class LogoutViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_protected_view_after_logout(self):
        self.client.login(username='testuser', password='testpassword')
        self.client.get(reverse('users:logout'))

        response = self.client.get(reverse('reports:my_reports'))
        self.assertRedirects(response, f"{reverse('users:login')}?next=/reports/my-reports/")
