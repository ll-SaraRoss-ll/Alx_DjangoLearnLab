"""
api/test_views.py

Contains APITestCase tests for:
- Book list, detail, create, update, delete endpoints
- Filtering, searching, and ordering functionality
- Permission enforcement for unauthenticated vs. authenticated requests
"""

from datetime import date, timedelta
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Author, Book


class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a user for authenticated requests
        self.user = User.objects.create_user(username='tester', password='pass1234')

        # Create two authors
        self.author1 = Author.objects.create(name='Author One')
        self.author2 = Author.objects.create(name='Second Author')

        # Create books for filtering, search, ordering
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

    def test_list_books(self):
        """GET /api/books/ should return all books."""
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertCountEqual(titles, ['Alpha Book', 'Beta Book', 'Gamma Guide'])

    def test_filter_by_title_exact(self):
        """Filtering with ?title=Beta Book returns only that book."""
        url = reverse('book-list') + '?title=Beta Book'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Beta Book')

    def test_filter_by_publication_year_range(self):
        """Filtering with ?publication_year__gte=2005&publication_year__lte=2015."""
        url = reverse('book-list') + '?publication_year__gte=2005&publication_year__lte=2015'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertTrue(all(2005 <= y <= 2015 for y in years))

    def test_search_books(self):
        """Searching with ?search=Guide finds 'Gamma Guide'."""
        url = reverse('book-list') + '?search=Guide'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Gamma Guide')

    def test_ordering_books(self):
        """Ordering with ?ordering=-publication_year returns newest first."""
        url = reverse('book-list') + '?ordering=-publication_year'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))

    def test_retrieve_book(self):
        """GET /api/books/<pk>/ returns the correct book data."""
        url = reverse('book-detail', args=[self.book_b.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Beta Book')

    def test_create_book_unauthenticated(self):
        """POST /api/books/create/ without auth must return 401."""
        url = reverse('book-create')
        data = {
            'title': 'New Book',
            'publication_year': 2021,
            'author': self.author1.pk
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_authenticated(self):
        """Authenticated POST /api/books/create/ creates a book."""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-create')
        data = {
            'title': 'New Book',
            'publication_year': 2021,
            'author': self.author1.pk
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.filter(title='New Book').count(), 1)

    def test_create_future_publication_year(self):
        """Creating with a future publication_year returns 400."""
        self.client.force_authenticate(user=self.user)
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

    def test_update_book_unauthenticated(self):
        """Unauthenticated PUT must return 401."""
        url = reverse('book-update', args=[self.book_a.pk])
        data = {'title': 'Updated Alpha'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book_authenticated(self):
        """Authenticated PATCH updates the book title."""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-update', args=[self.book_a.pk])
        data = {'title': 'Updated Alpha'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book_a.refresh_from_db()
        self.assertEqual(self.book_a.title, 'Updated Alpha')

    def test_delete_book_unauthenticated(self):
        """Unauthenticated DELETE must return 401."""
        url = reverse('book-delete', args=[self.book_c.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_book_authenticated(self):
        """Authenticated DELETE removes the book."""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-delete', args=[self.book_c.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book_c.pk).exists())
