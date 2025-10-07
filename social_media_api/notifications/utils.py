from .models import Notification
from django.contrib.contenttypes.models import ContentType

def create_notification(recipient, actor, verb, target=None):
    ct = None
    obj_id = None
    if target is not None:
        ct = ContentType.objects.get_for_model(target)
        obj_id = getattr(target, 'pk', None)
    Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb=verb,
        target_content_type=ct,
        target_object_id=str(obj_id) if obj_id is not None else None
    )

def create_notification_for_like(actor, recipient, post):
    if actor == recipient:
        return
    create_notification(recipient=recipient, actor=actor, verb='liked your post', target=post)
