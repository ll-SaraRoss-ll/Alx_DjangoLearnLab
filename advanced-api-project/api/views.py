from django.shortcuts import render
from datetime import date
from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Book
from .serializers import BookSerializer

class BookListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/books/ → list all books (public + filtering/search/ordering)
    POST /api/books/ → create a new book (authenticated only + extra validation)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Allow anyone to read; only authenticated users to create
    permission_classes = [IsAuthenticatedOrReadOnly]

    # 1. Enable searching and ordering on list endpoint
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'author__name']
    ordering_fields = ['publication_year', 'title']
    ordering = ['title']

    def get_permissions(self):
        # Allow anyone to read, only logged‐in users to write
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        """
        Apply a simple “min_year” filter if provided:
        /api/books/?min_year=2000
        """
        qs = super().get_queryset()
        min_year = self.request.query_params.get('min_year')
        if min_year and min_year.isdigit():
            qs = qs.filter(publication_year__gte=int(min_year))
        return qs

    def create(self, request, *args, **kwargs):
        """
        Add a quick check: title must be at least 3 chars.
        If it fails, return a custom error response.
        """
        title = request.data.get('title', '')
        if len(title) < 3:
            return Response(
                {'title': 'Title must be at least 3 characters long.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Proceed with standard DRF create (includes serializer validation)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """
        Hook: this is where you could set a `created_by` field
        or emit a signal/notification.
        """
        serializer.save()


class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/books/<pk>/    → retrieve (public)
    PUT    /api/books/<pk>/    → full update (authenticated only)
    PATCH  /api/books/<pk>/    → partial update (authenticated only)
    DELETE /api/books/<pk>/    → delete (authenticated only)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Allow anyone to read; only authenticated users to update or delete
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE', 'POST']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def update(self, request, *args, **kwargs):
        """
        Override update to enforce:
        - publication_year must not be in the future—even on updates.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)

        # Custom check before saving
        new_year = serializer.validated_data.get('publication_year')
        if new_year and new_year > date.today().year:
            return Response(
                {'publication_year': 'Cannot update to a future year.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        """
        Hook for audit logging, notifications, etc.
        """
        serializer.save()

