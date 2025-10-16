from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile_view, name='user-profile'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('api/register/', views.register_user, name='register_api'),
    path('api/login/', views.login_user, name='login_api'),
    path('api/profile/', views.user_profile, name='profile_api'),
    path('api/logout/', views.logout_user, name='logout_api'),

    path('follow/<int:user_id>/', views.follow_user, name='follow'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow'),

    path('api/follow/', views.follow_user, name='follow_api'),
    path('api/unfollow/', views.unfollow_user, name='unfollow_api'),
    path('api/followers/', views.get_followers, name='followers_api'),
    path('api/following/', views.get_following, name='following_api'),
    path('api/user/<int:user_id>/', views.user_detail, name='user_detail_api'),
    path('api/search/', views.user_search, name='user_search_api'),
]