from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AuthenticationTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user_credentials = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'secretpass123'
        }
        User.objects.create_user(**self.user_credentials)

    def test_login_view(self):
        # Attempt login with valid credentials
        response = self.client.post(
            reverse('blog:login'),
            {'username': self.user_credentials['username'], 
             'password': self.user_credentials['password']}
        )
        # Should redirect to profile
        self.assertRedirects(response, reverse('blog:profile'))

    def test_logout_view(self):
        # Log in first
        self.client.login(
            username=self.user_credentials['username'], 
            password=self.user_credentials['password']
        )
        response = self.client.get(reverse('blog:logout'))
        # After logout, redirect to login page
        self.assertRedirects(response, reverse('blog:login'))

    def test_register_view(self):
        # Register a new user
        response = self.client.post(
            reverse('blog:register'),
            {
                'username': 'newuser',
                'email': 'new@example.com',
                'password1': 'newsecret123',
                'password2': 'newsecret123'
            }
        )
        # After successful signup, new user is logged in and redirected
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertRedirects(response, reverse('blog:profile'))

    def test_profile_view_requires_login(self):
        # Unauthenticated users should be redirected to login
        response = self.client.get(reverse('blog:profile'))
        login_url = reverse('blog:login') + '?next=' + reverse('blog:profile')
        self.assertRedirects(response, login_url)

    def test_profile_update(self):
        # Log in as existing user
        self.client.login(
            username=self.user_credentials['username'],
            password=self.user_credentials['password']
        )
        # Update email via profile form
        response = self.client.post(
            reverse('blog:profile'),
            {'username': 'testuser', 'email': 'updated@example.com'}
        )
        self.assertRedirects(response, reverse('blog:profile'))
        user = User.objects.get(username='testuser')
        self.assertEqual(user.email, 'updated@example.com')
