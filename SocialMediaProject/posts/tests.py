from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Post, Like, Comment


class PostModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='sara', password='testpass123')

    def test_post_str(self):
        post = Post.objects.create(user=self.user, caption='Hello world')
        self.assertIn('sara', str(post))

    def test_like_toggle_counts(self):
        post = Post.objects.create(user=self.user, caption='Testing likes')
        Like.objects.create(post=post, user=self.user)
        self.assertEqual(post.like_count, 1)


class FeedViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='bilal', password='testpass123')
        Post.objects.create(user=self.user, caption='First post')

    def test_home_shows_posts(self):
        response = self.client.get(reverse('posts:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'First post')


class LikeViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='zara', password='testpass123')
        self.post = Post.objects.create(user=self.user, caption='Like me')

    def test_like_requires_login(self):
        response = self.client.post(reverse('posts:like_post', kwargs={'pk': self.post.pk}))
        self.assertNotEqual(response.status_code, 200)

    def test_authenticated_like_toggles(self):
        self.client.login(username='zara', password='testpass123')
        response = self.client.post(reverse('posts:like_post', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['liked'])
        self.assertEqual(Like.objects.filter(post=self.post).count(), 1)


class CommentViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='usman', password='testpass123')
        self.post = Post.objects.create(user=self.user, caption='Comment on this')

    def test_add_comment(self):
        self.client.login(username='usman', password='testpass123')
        response = self.client.post(
            reverse('posts:add_comment', kwargs={'pk': self.post.pk}),
            {'text': 'Nice post!'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.filter(post=self.post).count(), 1)
