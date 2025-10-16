from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'notifications', views.NotificationViewSet, basename='notification')

urlpatterns = [
    path('', views.notifications_view, name='notifications'),

    path('api/', include(router.urls)),
    path('api/stats/', views.notification_stats, name='notification_stats')
]
