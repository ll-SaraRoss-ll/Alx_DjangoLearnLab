from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Comment

class CommentTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='u1', password='pw')
        self.post = Post.objects.create(
            title='P', content='C', author=self.user
        )
        self.comment = Comment.objects.create(
            post=self.post, author=self.user, content='First'
        )

    def test_comments_show_on_detail(self):
        resp = self.client.get(reverse('blog:post-detail', args=[self.post.pk]))
        self.assertContains(resp, self.comment.content)

    def test_unauth_cannot_comment(self):
        resp = self.client.post(
            reverse('blog:comment-create', args=[self.post.pk]),
            {'content': 'New'}
        )
        self.assertRedirects(resp, reverse('blog:login') + '?next=' +
                             reverse('blog:comment-create', args=[self.post.pk]))

    def test_authenticated_can_comment(self):
        self.client.login(username='u1', password='pw')
        resp = self.client.post(
            reverse('blog:comment-create', args=[self.post.pk]),
            {'content': 'Nice'}
        )
        self.assertEqual(self.post.comments.count(), 2)

    def test_only_author_can_edit(self):
        other = User.objects.create_user(username='u2', password='pw2')
        self.client.login(username='u2', password='pw2')
        resp = self.client.get(
            reverse('blog:comment-update', args=[self.comment.pk])
        )
        self.assertEqual(resp.status_code, 403)

    def test_author_can_edit(self):
        self.client.login(username='u1', password='pw')
        resp = self.client.post(
            reverse('blog:comment-update', args=[self.comment.pk]),
            {'content': 'Edited'}
        )
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, 'Edited')

    def test_only_author_can_delete(self):
        other = User.objects.create_user(username='u2', password='pw2')
        self.client.login(username='u2', password='pw2')
        resp = self.client.post(
            reverse('blog:comment-delete', args=[self.comment.pk])
        )
        self.assertEqual(Comment.objects.count(), 1)

    def test_author_can_delete(self):
        self.client.login(username='u1', password='pw')
        resp = self.client.post(
            reverse('blog:comment-delete', args=[self.comment.pk])
        )
        self.assertEqual(Comment.objects.count(), 0)
