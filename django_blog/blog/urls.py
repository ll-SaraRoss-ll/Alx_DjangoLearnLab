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
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),

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

   # 1) Create comment on a specific post (singular 'post/')
    path(
      'post/<int:pk>/comments/new/',
      CommentCreateView.as_view(),
      name='comment-create'
    ),

    # 2) Edit a comment (singular 'comment/')
    path(
      'comment/<int:pk>/update/',
      CommentUpdateView.as_view(),
      name='comment-update'
    ),

    # 3) Delete a comment (singular 'comment/')
    path(
      'comment/<int:pk>/delete/',
      CommentDeleteView.as_view(),
      name='comment-delete'
    ),
]
