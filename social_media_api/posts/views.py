#from django.shortcuts import render
from rest_framework import generics, permissions, status
from django.contrib.auth import  get_user_model
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import LikeSerializer
from notifications.utils import create_notification_for_like
from django.contrib.contenttypes.models import ContentType
from notifications.models import Notification

CustomUser = get_user_model()

# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class FeedListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer
    pagination_class = None  # or use global pagination

    def get_queryset(self):
        user = self.request.user
        following_users = self.request.user.following.all()
        return Post.objects.filter(author__in=following_users).order_by('-created_at')
    
class PostLikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)
        user = request.user

        like, created = Like.objects.get_or_create(user=user, post=post)
        if not created:
            return Response({'detail': 'Already liked'}, status=status.HTTP_400_BAD_REQUEST)

        # create notification for the post author (do not notify self)
        if post.author != user:
            Notification.objects.create(
                recipient=post.author,
                actor=user,
                verb='liked your post',
                target_content_type=ContentType.objects.get_for_model(post),
                target_object_id=str(post.pk)
            )

        serializer = LikeSerializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class PostUnlikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        like = Like.objects.filter(user=user, post=post).first()
        if not like:
            return Response({'detail': 'Like does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)