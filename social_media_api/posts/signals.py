from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Like
from notifications.utils import create_notification_for_like

@receiver(post_save, sender=Like)
def like_created(sender, instance, created, **kwargs):
    if created:
        create_notification_for_like(actor=instance.user, recipient=instance.post.author, post=instance.post)
