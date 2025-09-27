from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('authors/', views.AuthorListCreateView.as_view(), name='author-list-create'),
    path('authors/<int:pk>/', views.AuthorRetrieveUpdateDestroyView.as_view(), name='author-detail'),
    
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    
    path('books/update/', views.BookUpdateView.as_view(), name='book-update-simple'),
    path('book/delete/', views.BookDeleteView.as_view(), name='book-delete-simple'),

    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), 
    name='book-delete'),

    path('books-combined/', views.BookListCreateView.as_view(), name='book-list-create'),
    path('books-combined/<int:pk>/', views.BookRetrieveUpdateDestroyView.as_view(), name='book-retrieve-update-destroy'),

    path('author-combined/', views.AuthorListCreateView.as_view(), name='author-list-create'),
    path('authors-combined/<int:pk>/', views.AuthorRetrieveUpdateDestroyView.as_view(), name='author-retrieve-update-destroy'),
]