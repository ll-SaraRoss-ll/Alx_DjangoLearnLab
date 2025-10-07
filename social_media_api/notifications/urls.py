from django.urls import path
from .views import NotificationListView, mark_as_read

urlpatterns = [
    path('', NotificationListView.as_view(), name='notifications-list'),
    path('<int:pk>/read/', mark_as_read, name='notification-mark-read'),
]
