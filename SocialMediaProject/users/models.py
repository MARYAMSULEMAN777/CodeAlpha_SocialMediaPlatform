from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Profile(models.Model):
    """Extra profile info attached 1-to-1 to Django's built-in User model."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.CharField(max_length=160, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def get_absolute_url(self):
        return reverse('users:profile', kwargs={'username': self.user.username})

    @property
    def follower_count(self):
        return self.user.followers.count()

    @property
    def following_count(self):
        return self.user.following.count()

    @property
    def post_count(self):
        return self.user.posts.count()
