from django.shortcuts import render
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, CommentCreateSerializer, PostCreateSerializer, LikeSerializer
from .pagination import CustomPagination
from accounts.serializers import UserFollowSerializer
from accounts.models import CustomUser
from notifications.models import Notification


# Create your views here.
def home_view(request):
    return render(request, 'home.html')

@login_required
def feed_view(request):
    return render(request, 'posts/feed.html')

@login_required
def post_list_view(request):
    return render(request, 'posts/post_list.html')

class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content', 'author__username']
    ordering_fields = ['created_at', 'updated_at', 'likes_count', 'comments_count']
    ordering = ['-created_at']
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Post.objects.all().select_related('author').prefetch_related('likes', 'comments')
        author = self.request.query_params.get('author', None)
        if author:
            queryset = queryset.filter(author__username=author)
        liked = self.request.query_params.get('liked', None)
        if liked and self.request.user.is_authenticated:
            queryset = queryset.filter(likes=self.request.user)

        return queryset

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return PostCreateSerializer
        return PostSerializer
    
    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)


    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        content_type = ContentType.objects.get_for_model(Post)

        like, created = Like.objects.get_or_create(
            user = request.user,
            content_type = content_type,
            object_id = post.id
        )

        if created:
            liked = True
        else:
            like.delete()
            liked = False
        return Response({
            'liked': liked,
            'likes_count': post.likes_count
        })
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticatedOrReadOnly])
    def comments(self, request, pk=None):
        post = self.get_object()
        comments = post.comments.all().select_related('author')
        page = self.paginate_queryset(comments)

        if page is not None:
            serializer = CommentSerializer(page, many = True, context = {'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = CommentSerializer(comments, many = True, context = {'request': request})
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Comment.objects.all().select_related('author', 'post')
        post_id = self.request.query_params.get('post', None)
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        author = self.request.query_params.get('author', None)
        if author:
            queryset = queryset.filter(author__username=author)
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return CommentCreateSerializer
        return CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        comment = self.get_object()
        content_type = ContentType.objects.get_for_model(Comment)

        like, created = Like.objects.get_or_create(
            user = request.user,
            content_type = content_type,
            object_id = comment.id
        )

        if created:
            liked = True
        else:
            like.delete()
            liked = False
        return Response({
            'liked': liked,
            'likes_count': comment.likes_count
        })
    

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_feed(request):
    following_users = request.user.following.all()
    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
    posts = posts.select_related('author').prefetch_related('likes', 'comments')

    paginator = CustomPagination()
    paginated_posts = paginator.paginate_queryset(posts, request)
    serializer = PostSerializer(
        paginated_posts,
        many = True,
        context = {'request': request}
    )
    return paginator.get_paginated_response(serializer.data)

class FeedViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    def list(self, request):
        return user_feed(request)

    @action(detail=False, methods=['get'])
    def suggestions(self, request):
        users_to_suggest = CustomUser.objects.exclude(
            Q(id=request.user.id) |
            Q(id__in=request.user.following.values_list('id', flat=True))
        )[:10]

        serializer = UserFollowSerializer(
            users_to_suggest,
            many = True,
            context = {'request': request}
        )
        return Response(serializer.data)

                
class LikeViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='post/(?P<post_id>[^/.]+)')
    def like_post(self, request, post_id=None):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post Not Found'}, status=status.HTTP_404_NOT_FOUND)
        
        content_type = ContentType.objects.get_for_model(Post)
        like, created = Like.objects.get_or_create(
            user = request.user,
            content_type = content_type,
            object_id = post.id
        )
        if created:
            if post.author != request.user:
                Notification.create_notification(
                    recipient=post.author,
                    actor=request.user,
                    verb='like_post',
                    target=post
                )
            return Response({
                'liked': True,
                'likes_count': post.likes_count,
                'message': 'Post liked successfully!'
            }, status=status.HTTP_201_CREATED)
        else:
            like.delete()
            return Response({
                'liked': False,
                'likes_count': post.likes_count,
                'message': 'Post unliked successfully!'
            }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='comment/(?P<comment_id>[^/.]+)')
    def like_comment(self, request, comment_id=None):
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment Not Found'}, status=status.HTTP_404_NOT_FOUND)

        content_type = ContentType.objects.get_for_model(Comment)
        like, created = Like.objects.get_or_create(
            user = request.user,
            content_type = content_type,
            object_id = comment.id
        )
        if created:
            if comment.author != request.user:
                Notification.create_notification(
                    recipient=comment.author,
                    actor=request.user,
                    verb='like_comment',
                    target=comment
                )
            return Response({
                'liked':True,
                'likes_count': comment.likes_count,
                'message': 'Comment liked successfully!'
            }, status=status.HTTP_201_CREATED)
        else:
            like.delete()
            return Response({
                'liked': False,
                'likes_count': comment.likes_count,
                'message': 'Comment unliked Successfully!'
            }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], url_path='my-likes')
    def my_likes(self, request):
        post_content_type = ContentType.objects.get_for_model(Post)
        liked_posts = Post.objects.filter(
            id__in = Like.objects.filter(
                user = request.user,
                content_type = post_content_type
            ).values_list('object_id', flat=True)
        )

        comment_content_type = ContentType.objects.get_for_model(Comment)
        liked_comments = Comment.objects.filter(
            id__in = Like.objects.filter(
                user = request.user,
                content_type = comment_content_type
            ).values_list('object_id', flat=True)
        )

        post_serializer = PostSerializer(
            liked_posts,
            many = True,
            context= {'request': request}
        )
        comment_serializer = CommentSerializer(
            liked_comments,
            many = True,
            context = {'request': request}
        )
        return Response({
            'liked_posts': post_serializer.data,
            'liked_comments': comment_serializer.data
        })

class PostLikeView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)

        like, created = Like.objects.get_or_create(user = request.user, post = post
        )
        if created:
            if post.author != request.user:
                Notification.objects.create(
                    recipient = post.author,
                    actor = request.user,
                    verb = 'like_post',
                    target = post
                )
            return Response({
                'liked': True,
                'likes_count': post.likes_count,
                'message': 'Post liked successfully!'
            }, status=status.HTTP_201_CREATED)
        else:
            like.delete()
            return Response({
                'liked': False,
                'likes_count': post.likes_count,
                'message': 'Post unliked successfully!'
            }, status=status.HTTP_200_OK)