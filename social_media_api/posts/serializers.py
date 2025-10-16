from rest_framework import serializers
from .models import Post, Comment, Like
from accounts.serializers import UserProfileSerializer
from django.contrib.contenttypes.models import ContentType

class LikeSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = Like
        fields = ['id', 'user', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer(read_only=True)
    likes_count = serializers.ReadOnlyField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id', 'post', 'author', 'content', 'created_at', 'updated_at',
            'likes_count', 'is_liked'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at', 'post']

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.get_like(request.user) is not None
        return False

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

class PostSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer(read_only=True)
    comments_count = serializers.ReadOnlyField()
    likes_count = serializers.ReadOnlyField()
    is_liked = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    likes = LikeSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'title', 'content', 'created_at', 'updated_at',
            'likes_count', 'comments_count', 'is_liked', 'comments', 'likes'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.get_like(request.user) is not None
        return False

    def get_comments(self, obj):
        """Get comments without circular imports"""
        comments = obj.comments.all()[:5]
        # Return basic comment data without using CommentSerializer
        comment_data = []
        for comment in comments:
            comment_data.append({
                'id': comment.id,
                'author': {
                    'id': comment.author.id,
                    'username': comment.author.username,
                    'first_name': comment.author.first_name,
                    'last_name': comment.author.last_name,
                    'profile_picture': comment.author.profile_picture.url if comment.author.profile_picture else None
                },
                'content': comment.content,
                'created_at': comment.created_at,
                'updated_at': comment.updated_at,
                'likes_count': comment.likes_count,
            })
        return comment_data

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content']

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content', 'post']

