from django.urls import path
from . import views
from .views import CustomLoginView, CustomLogoutView, RegisterView, LibraryDetailView, admin_view, librarian_view, member_view, add_book, edit_book, delete_book, list_books

urlpatterns = [
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('admin/', admin_view, name='admin_view'),
    path('member/', member_view, name='member_view'),
    path('librarian/', librarian_view, name='librarian_view'),
    path('book/delete/<int:book_id>/', delete_book, name='delete_book'),
    path('book/edit/<int:book_id>/', edit_book, name='edit_book'),
    path('book/add/', add_book, name='add_book'),

]