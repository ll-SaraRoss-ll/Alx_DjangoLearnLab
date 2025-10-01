
from django.urls import path
from .views import (
    register_view,
    CustomLoginView,
    CustomLogoutView,
    profile_view,
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CommentCreateView,
    post_detail,
    CommentUpdateView,
    CommentDeleteView,
    PostByTagListView,
    SearchResultsView,
)

app_name = 'blog'

urlpatterns = [
    # Authentication & Profile
    path('register/', register_view, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/', profile_view, name='profile'),

    # Post CRUD
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),

    # Comment CRUD (singular paths)
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='comment-create'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),

    # Tag filtering & Search
    path('tags/<slug:tag_slug>/', PostByTagListView.as_view(), name='tag-posts'),
    path('search/', SearchResultsView.as_view(), name='search'),
]
