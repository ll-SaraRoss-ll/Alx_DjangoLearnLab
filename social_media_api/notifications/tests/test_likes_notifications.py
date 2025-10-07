from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from posts.models import Post, Like
from notifications.models import Notification

User = get_user_model()

class LikeNotificationTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='u1', password='pass')
        self.user2 = User.objects.create_user(username='u2', password='pass')
        self.post = Post.objects.create(author=self.user2, title='t', content='c')

    def test_like_creates_notification(self):
        self.client.login(username='u1', password='pass')
        url = reverse('post-like', kwargs={'pk': self.post.pk})
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(Like.objects.filter(user=self.user1, post=self.post).exists())
        self.assertTrue(Notification.objects.filter(recipient=self.user2, actor=self.user1, verb__icontains='liked').exists())

    def test_unlike_removes_like(self):
        self.client.login(username='u1', password='pass')
        self.client.post(reverse('post-like', kwargs={'pk': self.post.pk}))
        resp = self.client.post(reverse('post-unlike', kwargs={'pk': self.post.pk}))
        self.assertEqual(resp.status_code, 204)
        self.assertFalse(Like.objects.filter(user=self.user1, post=self.post).exists())
