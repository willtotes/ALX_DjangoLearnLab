from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='post')
router.register(r'comments', views.CommentViewSet, basename='comment')
router.register(r'feed', views.FeedViewSet, basename='feed')
router.register(r'likes', views.LikeViewSet, basename='like')

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', views.user_feed, name='feed'),
    path('api/feed/', views.FeedViewSet.as_view({'get': 'list'}), name='api_feed'),

    path('posts/<int:pk>/like/', views.PostLikeView.as_view(), name='post_like'),
    path('posts/<int:pk>/unlike/', views.PostLikeView.as_view(), name='post_unlike'),
    
    #path('post/<int:pk>/like/', views.PostLikeAPIView.as_view(), name='post_like_alt')
]
