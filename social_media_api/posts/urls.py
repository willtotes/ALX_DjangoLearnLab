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
]
