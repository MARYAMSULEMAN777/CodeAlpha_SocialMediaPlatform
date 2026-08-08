from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Profile


class ProfileSignalTests(TestCase):
    def test_profile_created_automatically(self):
        user = User.objects.create_user(username='amina', password='testpass123')
        self.assertTrue(Profile.objects.filter(user=user).exists())


class RegisterViewTests(TestCase):
    def test_register_creates_user_and_logs_in(self):
        response = self.client.post(reverse('users:register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'StrongPass123',
            'password2': 'StrongPass123',
        })
        self.assertEqual(User.objects.filter(username='newuser').count(), 1)
        self.assertRedirects(response, reverse('posts:home'))


class ProfileViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='hina', password='testpass123')

    def test_profile_page_loads(self):
        response = self.client.get(reverse('users:profile', kwargs={'username': 'hina'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'hina')
