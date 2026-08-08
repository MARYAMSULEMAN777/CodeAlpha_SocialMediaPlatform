from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Follow


class FollowToggleTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username='alice', password='testpass123')
        self.bob = User.objects.create_user(username='bob', password='testpass123')

    def test_follow_and_unfollow_toggle(self):
        self.client.login(username='alice', password='testpass123')
        url = reverse('followers:toggle_follow', kwargs={'username': 'bob'})

        self.client.post(url)
        self.assertTrue(Follow.objects.filter(follower=self.alice, following=self.bob).exists())

        self.client.post(url)
        self.assertFalse(Follow.objects.filter(follower=self.alice, following=self.bob).exists())

    def test_cannot_follow_self(self):
        self.client.login(username='alice', password='testpass123')
        url = reverse('followers:toggle_follow', kwargs={'username': 'alice'})
        self.client.post(url)
        self.assertFalse(Follow.objects.filter(follower=self.alice, following=self.alice).exists())
