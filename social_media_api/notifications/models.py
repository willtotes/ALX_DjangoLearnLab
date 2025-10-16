from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.
class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('follow', 'Follow'),
        ('like_post', 'Like Post'),
        #('like_comment', 'Like Comment'),
        ('comment', 'Comment'),
        #('mention', 'Mention'),
    )
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='actions')
    verb = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    target_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')
    data = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'read', 'created_at']),
        ]

    def __str__(self):
        return f'{self.actor.username} {self.get_verb_display()} for {self.recipient.username}'

    def mark_as_read(self):
        self.read = True
        self.save()

    def get_message(self):
        messages = {
            'follow': f'{self.actor.username} started following you',
            'like_post': f'{self.actor.username} liked your post',
            'like_comment': f'{self.actor.username} liked your comment',
            'comment': f'{self.actor.username} commented on your post',
            'mention': f'{self.actor.username} mentioned you in a post'
        }
        return messages.get(self.verb, 'New notification')

    @classmethod
    def create_notification(cls, recipient, actor, verb, target=None, data=None):
        notification = cls(
            recipient = recipient,
            actor = actor,
            verb = verb,
            data= data or {}
        )
        if target:
            notification.target_content_type = ContentType.objects.get_for_model(target)
            notification.target_object_id = target.id
        notification.save()
        return notification

