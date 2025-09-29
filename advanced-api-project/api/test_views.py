
"""
api/test_views.py

APITestCase suite covering:
- CRUD endpoints using BookListView, BookDetailView,
  BookCreateView, BookUpdateView, BookDeleteView
- Filtering, searching, ordering on ListView
- Permission enforcement via self.client.login() and self.client.logout()
"""

from datetime import date
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Author, Book

class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create and log in a test user (uses separate test database)
        self.user = User.objects.create_user(username='tester', password='pass1234')
        self.client.login(username='tester', password='pass1234')

        # Create authors
        self.author1 = Author.objects.create(name='Author One')
        self.author2 = Author.objects.create(name='Author Two')

        # Create books for list, filter, search, ordering
        self.book_a = Book.objects.create(
            title='Alpha Book',
            publication_year=2000,
            author=self.author1
        )
        self.book_b = Book.objects.create(
            title='Beta Book',
            publication_year=2010,
            author=self.author2
        )
        self.book_c = Book.objects.create(
            title='Gamma Guide',
            publication_year=2020,
            author=self.author1
        )

    def test_list_books_public(self):
        """ListView GET /api/books/ should be public."""
        self.client.logout()
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [item['title'] for item in response.data]
        self.assertCountEqual(titles, ['Alpha Book', 'Beta Book', 'Gamma Guide'])

    def test_filter_books_by_title(self):
        """ListView filter by exact title."""
        url = reverse('book-list') + '?title=Beta Book'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Beta Book')

    def test_search_books(self):
        """ListView search finds partial matches."""
        url = reverse('book-list') + '?search=Guide'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Gamma Guide')

    def test_order_books(self):
        """ListView ordering returns correct order."""
        url = reverse('book-list') + '?ordering=-publication_year'
        response = self.client.get(url)
        years = [item['publication_year'] for item in response.data]
        self.assertEqual(years, sorted(years, reverse=True))

    def test_retrieve_book_public(self):
        """DetailView GET /api/books/<pk>/ should be public."""
        self.client.logout()
        url = reverse('book-detail', args=[self.book_b.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Beta Book')

    def test_create_book_authenticated(self):
        """CreateView POST /api/books/create/ with login should succeed."""
        url = reverse('book-create')
        data = {
            'title': 'New Book',
            'publication_year': 2021,
            'author': self.author1.pk
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Book.objects.filter(title='New Book').exists())

    def test_create_book_unauthenticated(self):
        """CreateView without login returns 401."""
        self.client.logout()
        url = reverse('book-create')
        data = {
            'title': 'Unauthorized Create',
            'publication_year': 2021,
            'author': self.author1.pk
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_future_publication_year(self):
        """CreateView rejects future publication_year."""
        future_year = date.today().year + 5
        url = reverse('book-create')
        data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author2.pk
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)

    def test_update_book_authenticated(self):
        """UpdateView PATCH /api/books/update/<pk>/ with login updates book."""
        url = reverse('book-update', args=[self.book_a.pk])
        response = self.client.patch(url, {'title': 'Updated Alpha'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book_a.refresh_from_db()
        self.assertEqual(self.book_a.title, 'Updated Alpha')

    def test_update_book_unauthenticated(self):
        """UpdateView without login returns 401."""
        self.client.logout()
        url = reverse('book-update', args=[self.book_a.pk])
        response = self.client.patch(url, {'title': 'No Change'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_book_authenticated(self):
        """DeleteView DELETE /api/books/delete/<pk>/ with login removes book."""
        url = reverse('book-delete', args=[self.book_c.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book_c.pk).exists())

    def test_delete_book_unauthenticated(self):
        """DeleteView without login returns 401."""
        self.client.logout()
        url = reverse('book-delete', args=[self.book_c.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
