# api/urls.py

from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
)

urlpatterns = [
    # LIST all books
    path('books/',                         BookListView.as_view(),   name='book-list'),
    # DETAIL of a single book
    path('books/<int:pk>/',                BookDetailView.as_view(), name='book-detail'),
    # CREATE a new book
    path('books/create/',                  BookCreateView.as_view(), name='book-create'),
    # UPDATE an existing book
    path('books/update/<int:pk>/',         BookUpdateView.as_view(), name='book-update'),
    # DELETE a book
    path('books/delete/<int:pk>/',         BookDeleteView.as_view(), name='book-delete'),
]
