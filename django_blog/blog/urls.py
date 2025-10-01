from django.urls import path
from .views import register_view, CustomLoginView, CustomLogoutView, profile_view
from .views import (
    PostListView, PostDetailView,
    PostCreateView, PostUpdateView, PostDeleteView
)
from .views import (
    CommentCreateView, post_detail,
    CommentUpdateView, CommentDeleteView
)
app_name = 'blog'

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/', profile_view, name='profile'),

    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path(
        'post/<int:pk>/',
        post_detail,
        name='post-detail'
    ),
    path(
        'post/<int:pk>/update/',
        PostUpdateView.as_view(),
        name='post-update'
    ),
    path(
        'post/<int:pk>/delete/',
        PostDeleteView.as_view(),
        name='post-delete'
    ),
    # Comment CRUD
    path(
      'posts/<int:post_pk>/comments/new/',
      CommentCreateView.as_view(),
      name='comment-create'
    ),
    path(
        'comments/<int:pk>/edit/',
        CommentUpdateView.as_view(),
        name='comment-update'
    ),
    path(
        'comments/<int:pk>/delete/',
        CommentDeleteView.as_view(),
        name='comment-delete'
    ),
]
