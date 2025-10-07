from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FeedListView

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')  # <— must exist

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', FeedListView.as_view(), name='feed'),
]
