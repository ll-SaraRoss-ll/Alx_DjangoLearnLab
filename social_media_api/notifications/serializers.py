from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.SerializerMethodField()
    target = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'verb', 'target', 'timestamp', 'read']

    def get_actor(self, obj):
        if obj.actor:
            return {'id': obj.actor.id, 'username': getattr(obj.actor, 'username', None)}
        return None

    def get_target(self, obj):
        if obj.target:
            ct = obj.target_content_type
            return {'type': ct.model if ct else None, 'id': obj.target_object_id}
        return None
