from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Tag

class TagAndSearchTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('u', 'u@example.com', 'pw')
        # Create posts and tags
        self.post1 = Post.objects.create(title='Django Tips', content='Learn Django', author=self.user)
        self.post2 = Post.objects.create(title='Python Tricks', content='Learn Python', author=self.user)
        Tag.objects.create(name='django')
        self.post1.tags.add(Tag.objects.get(name='django'))

    def test_assign_new_tags_via_form(self):
        self.client.login(username='u', password='pw')
        response = self.client.post(
            reverse('blog:post-create'),
            {'title': 'New', 'content': 'C', 'tags': 'alpha, beta'}
        )
        post = Post.objects.latest('published_date')
        self.assertTrue(post.tags.filter(name='alpha').exists())
        self.assertTrue(post.tags.filter(name='beta').exists())

    def test_posts_by_tag(self):
        response = self.client.get(reverse('blog:tag-posts', args=['django']))
        self.assertContains(response, 'Django Tips')
        self.assertNotContains(response, 'Python Tricks')

    def test_search_by_title(self):
        response = self.client.get(reverse('blog:search') + '?q=Python')
        self.assertContains(response, 'Python Tricks')
        self.assertNotContains(response, 'Django Tips')

    def test_search_by_tag(self):
        response = self.client.get(reverse('blog:search') + '?q=django')
        self.assertContains(response, 'Django Tips')
