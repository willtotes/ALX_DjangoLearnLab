from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import PostListView, PostDetailView, PostDeleteView, PostCreateView, PostUpdateView, CommentCreateView, CommentUpdateView, CommentDeleteView, SearchResultsView, TaggedPostsView

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),

    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('logout/', views.custom_logout, name='logout'),
    path('profile/', views.profile, name='profile'),

    path('posts/<int:post_id>/comment/', CommentCreateView.as_view(), name='add-comment'),
    path('comments/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment-update'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),

    path('search/', SearchResultsView.as_view(), name='search'),
    path('tags/<str:tag>/', TaggedPostsView.as_view(), name='tagged-posts'),
    path('tags/', views.popular_tags, name='popular-tags'),

]