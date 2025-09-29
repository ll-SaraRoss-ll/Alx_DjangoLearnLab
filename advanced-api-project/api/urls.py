from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    BookListCreateView,
    BookRetrieveUpdateDestroyView,
)

urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookRetrieveUpdateDestroyView.as_view(), name='book-detail'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
