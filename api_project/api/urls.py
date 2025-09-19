from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet
from .views import index

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path('', index, name='index'),   # serves http://127.0.0.1:8000/api/ if included under api/
    path('books/', BookList.as_view(), name='book-list'),
    path('', include(router.urls)),
]
