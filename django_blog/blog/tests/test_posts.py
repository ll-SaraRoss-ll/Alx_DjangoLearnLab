from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post

class PostCRUDTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='author', password='pass1234')
        self.other = User.objects.create_user(username='other', password='pass1234')
        self.post = Post.objects.create(
            title='Test Post',
            content='Content here',
            author=self.user
        )

    def test_list_view(self):
        resp = self.client.get(reverse('blog:post-list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.post.title)

    def test_detail_view(self):
        resp = self.client.get(reverse('blog:post-detail', args=[self.post.pk]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.post.content)

    def test_create_requires_login(self):
        resp = self.client.get(reverse('blog:post-create'))
        self.assertRedirects(resp, '/login/?next=' + reverse('blog:post-create'))

    def test_logged_in_can_create(self):
        self.client.login(username='author', password='pass1234')
        resp = self.client.post(reverse('blog:post-create'), {
            'title': 'New',
            'content': 'More content'
        })
        self.assertEqual(Post.objects.count(), 2)
        new = Post.objects.latest('published_date')
        self.assertEqual(new.author, self.user)

    def test_update_only_author(self):
        self.client.login(username='other', password='pass1234')
        resp = self.client.get(reverse('blog:post-update', args=[self.post.pk]))
        self.assertEqual(resp.status_code, 403)

    def test_author_can_update(self):
        self.client.login(username='author', password='pass1234')
        resp = self.client.post(reverse('blog:post-update', args=[self.post.pk]), {
            'title': 'Changed',
            'content': 'Edited'
        })
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Changed')

    def test_delete_only_author(self):
        self.client.login(username='other', password='pass1234')
        resp = self.client.post(reverse('blog:post-delete', args=[self.post.pk]))
        self.assertEqual(Post.objects.count(), 1)

    def test_author_can_delete(self):
        self.client.login(username='author', password='pass1234')
        resp = self.client.post(reverse('blog:post-delete', args=[self.post.pk]))
        self.assertEqual(Post.objects.count(), 0)
