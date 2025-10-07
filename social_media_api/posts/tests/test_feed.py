from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from posts.models import Post

User = get_user_model()

class FeedTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username='alice', password='p')
        self.bob = User.objects.create_user(username='bob', password='p')
        Post.objects.create(author=self.bob, title='t1', content='c1')
        token, _ = Token.objects.get_or_create(user=self.alice)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_feed_shows_only_followed(self):
        self.alice.following.add(self.bob)
        res = self.client.get('/api/feed/')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        results = data.get('results', data)
        self.assertTrue(any(p['title']=='t1' for p in results))
