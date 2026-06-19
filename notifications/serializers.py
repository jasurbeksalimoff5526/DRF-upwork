from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    actor_name = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            "id",
            "receiver",
            "actor",
            "actor_name",
            "notification_type",
            "title",
            "message",
            "project",
            "contract",
            "is_read",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "receiver",
            "actor",
            "actor_name",
            "notification_type",
            "title",
            "message",
            "project",
            "contract",
            "created_at",
        ]

    def get_actor_name(self, obj):
        if obj.actor:
            return obj.actor.get_full_name() or obj.actor.username
        return None
    

