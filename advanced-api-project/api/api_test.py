import os
import django
from django.contrib.auth.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')
django.setup()

from api.models import Author, Book
from api.serializers import BookSerializer, AuthorSerializer
from django.utils import timezone

def test_models_and_serializers():
    print("<=== Testing Models and Serializers ===>")

    author, created = Author.objects.get_or_create(name='George Orwell')
    if created:
        print(f'Created author: {author}')
    
    book, created = Book.objects.get_or_create(
        title = "1984",
        publication_year = 1949,
        author = author
    )
    if created:
        print(f'Created book: {book}')

    serializer = BookSerializer(book)
    print('Serialized book data:')
    print(serializer.data)
    print()

def test_permissions():
    print("<=== Testing Permission Scenarios ===>")

    user, created = User.objects.get_or_create(
        username = 'testuser',
        defaults = {'email': 'test@example.com'}
    )
    if created:
        user.set_password('passtest123')
        user.save()
        print(f'Created test user: {user}')
    else:
        print(f"Using existing test user: {user}")

    print('Permission scenarios:')
    print('-- Unauthenticated users can READ books (GET requests)')
    print('-- Authenticated users can CREATE, UPDATE, DELETE books')
    print('-- Custom permissions enforce these rules')
    print()

def test_view_urls():
    print("<=== Available API Endpoints ===>")
    endpoints = [
        "GET    /api/books/                 - List all books",
        "POST   /api/books/create/          - Create new book (auth required)",
        "GET    /api/books/<id>/            - Get book details",
        "PUT    /api/books/<id>/update/     - Update book (auth required)",
        "DELETE /api/books/<id>/delete/     - Delete book (auth required)",
        "GET    /api/books-combined/        - List books (public)",
        "POST   /api/books-combined/        - Create book (auth required)",
        "GET    /api/books-combined/<id>/   - Get book details",
        "PUT    /api/books-combined/<id>/   - Update book (auth required)",
        "DELETE /api/books-combined/<id>/   - Delete book (auth required)",
        "GET    /api/authors/               - List authors",
        "POST   /api/authors/               - Create author (auth required)",
        "GET    /api/authors/<id>/          - Get author details",
        "PUT    /api/authors/<id>/          - Update author (auth required)",
        "DELETE /api/authors/<id>/          - Delete author (auth required)",
    ]
    for endpoint in endpoints:
        print(endpoint)
    print()

def test_serializer_validation():
    print("<=== Testing Serializer Validation ===>")
    author, _ = Author.objects.get_or_create(name="Test Author")

    future_year = timezone.now().year + 1
    invalid_book_data = {
        'title': 'Future Book',
        'publication_year': future_year,
        'author': author.id
    }
    serializer = BookSerializer(data=invalid_book_data)
    is_valid = serializer.is_valid()

    print(f'Testing future publication year ({future_year}):')
    print(f'Validation passed: {is_valid}')
    if not is_valid:
        print(f'Validation errors: {serializer.errors}')

    valid_book_data = {
        'title': 'Past Book',
        'publication_year': 2020,
        'author': author.id
    }
    serializer = BookSerializer(data=valid_book_data)
    is_valid = serializer.is_valid()
    print(f'\nTesting past publication year (2020):')
    print(f'Validation passed: {is_valid}')
    print()

if __name__ == "__main__":
    test_models_and_serializers()
    test_serializer_validation()
    test_permissions()
    test_view_urls()
    print('<=== Testing Complete ===>')
