from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class FollowTests(TestCase):
    def setUp(self):
        self.a = User.objects.create_user(username='a', password='p')
        self.b = User.objects.create_user(username='b', password='p')
        token, _ = Token.objects.get_or_create(user=self.a)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_follow_unfollow_and_self_follow(self):
        res = self.client.post(f'/api/auth/follow/{self.b.id}/')
        self.assertEqual(res.status_code, 200)
        self.assertIn(self.b, self.a.following.all())
        res = self.client.post(f'/api/auth/follow/{self.a.id}/')
        self.assertEqual(res.status_code, 400)
        res = self.client.post(f'/api/auth/unfollow/{self.b.id}/')
        self.assertEqual(res.status_code, 200)
        self.assertNotIn(self.b, self.a.following.all())
