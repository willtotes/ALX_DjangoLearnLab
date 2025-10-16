"""
URL configuration for social_media_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from . import health_checks
from accounts.views import register_view, login_view, profile_view, logout_view
from notifications.views import notifications_view
from posts.views import home_view, feed_view, post_list_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('accounts.urls')),
    path('api/', include('posts.urls')),
    path('notifications/', include('notifications.urls')),
    path('health/', health_checks.health_check, name='health-check'),

    path('', home_view, name='home'),
    path('feed/', feed_view, name='feed'),
    path('posts/', post_list_view, name='post_list'),
    path('notifications/', notifications_view, name='notifications'),

    path('login/', TemplateView.as_view(template_name='accounts/login.html'), name='login'),
    path('register/', TemplateView.as_view(template_name='accounts/register.html'), name='register'),
    path('profile/', TemplateView.as_view(template_name='accounts/profile.html'), name='profile'),


    path('feed/', TemplateView.as_view(template_name='posts/feed.html'), name='feed'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    

