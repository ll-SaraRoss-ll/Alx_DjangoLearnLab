from django_filters import rest_framework
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

class BookListView(generics.ListAPIView):
    """
    GET /api/books/ → list all books (public)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    # 1. Enable backends
    filter_backends = [
        DjangoFilterBackend,      # exact / range filters
        filters.SearchFilter,     # text search
        filters.OrderingFilter,   # result ordering
    ]

    # 2. Configure filter fields
    filterset_fields = {
        'title': ['exact', 'icontains'],
        'publication_year': ['exact', 'gte', 'lte'],
        'author__name': ['exact', 'icontains'],
    }

    # 3. Configure search fields
    search_fields = [
        'title',
        'author__name',
    ]

    # 4. Configure ordering
    ordering_fields = [
        'title',
        'publication_year',
        'author__name',
    ]
    ordering = ['title']

class BookDetailView(generics.RetrieveAPIView):
    """
    GET /api/books/<pk>/ → retrieve a single book (public)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookCreateView(generics.CreateAPIView):
    """
    POST /api/books/ → create a new book (authenticated only)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH /api/books/<pk>/ → update a book (authenticated only)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE /api/books/<pk>/ → delete a book (authenticated only)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
