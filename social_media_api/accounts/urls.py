from django.urls import path
from .views import RegisterView, LoginView, ProfileView
from .views import FollowUserView, FollowersListView, UnfollowUserView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),

    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow'),
    path('<int:user_id>/followers/', FollowersListView.as_view(), name='followers-list'),
]