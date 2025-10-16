from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    title = models.CharField(max_length=300)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} by {self.author.username}'


    @property
    def comments_count(self):
        return self.comments.count()
    
    @property
    def likes_count(self):
        content_type = ContentType.objects.get_for_model(self)
        return Like.objects.filter(
            content_type=content_type,
            object_id=self.id
        ).count()

    def get_like(self, user):
        content_type = ContentType.objects.get_for_model(self)
        return Like.objects.filter(
            user = user,
            content_type = content_type,
            object_id = self.id
        ).first()

class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def likes_count(self):
        content_type = ContentType.objects.get_for_model(self)
        return Like.objects.filter(
            content_type=content_type,
            object_id=self.id
        ).count()

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Commented by {self.author.username} on {self.post.title}'

    
    def get_like(self, user):
        content_type = ContentType.objects.get_for_model(self)
        return Like.objects.filter(
            user = user,
            content_type = content_type,
            object_id = self.id
        ).first()

class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'content_type', 'object_id']
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} liked {self.content_object}'

