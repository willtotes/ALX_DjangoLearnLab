from .models import Notification
from rest_framework import serializers
from accounts.serializers import UserProfileSerializer

class NotificationSerializer(serializers.ModelSerializer):
    actor = UserProfileSerializer(read_only=True)
    message = serializers.SerializerMethodField()
    target_type = serializers.SerializerMethodField()
    target_id = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id', 'actor', 'verb', 'message', 'target_type', 'target_id',
            'data', 'read', 'created_at'
        ]
        read_only_fields = fields

    def get_message(self, obj):
        return obj.get_message()

    def get_target_type(self, obj):
        if obj.target_content_type:
            return obj.target_content_type.model
        return None

    def get_target_id(self, obj):
        return obj.target_object_id

class NotificationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['read']

class NotificationCountSerializer(serializers.Serializer):
    unread_count = serializers.IntegerField()
    total_count = serializers.IntegerField()