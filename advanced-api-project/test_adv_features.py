import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')

django.setup()

from django.test import RequestFactory
from django.contrib.auth.models import User
from api.models import Author, Book
from api.views import BookListCreateView, AuthorListCreateView

def setup_test_data():
    """Create test data for advanced filtering tests."""
    print("=== Setting Up Test Data ===")
    
    authors_data = [
        {"name": "J.K. Rowling"},
        {"name": "George Orwell"},
        {"name": "J.R.R. Tolkien"},
    ]
    
    authors = {}
    for author_data in authors_data:
        author, created = Author.objects.get_or_create(**author_data)
        authors[author.name] = author
        status = "Created" if created else "Using existing"
        print(f"   {status} author: {author.name}")
    
    books_data = [
        {"title": "Harry Potter and the Philosopher's Stone", "publication_year": 1997, "author": authors["J.K. Rowling"]},
        {"title": "Harry Potter and the Chamber of Secrets", "publication_year": 1998, "author": authors["J.K. Rowling"]},
        {"title": "1984", "publication_year": 1949, "author": authors["George Orwell"]},
        {"title": "Animal Farm", "publication_year": 1945, "author": authors["George Orwell"]},
        {"title": "The Hobbit", "publication_year": 1937, "author": authors["J.R.R. Tolkien"]},
    ]
    
    for book_data in books_data:
        book, created = Book.objects.get_or_create(
            title=book_data["title"],
            defaults={
                "publication_year": book_data["publication_year"],
                "author": book_data["author"]
            }
        )
        status = "Created" if created else "Using existing"
        print(f"   {status} book: {book.title} ({book.publication_year})")
    
    print(f"Total books in database: {Book.objects.count()}")
    print("=== Test Data Setup Complete ===\n")

def test_basic_models():
    print("=== TESTING BASIC MODELS ===")
    
    authors_count = Author.objects.count()
    print(f"Authors in database: {authors_count}")
    
    books_count = Book.objects.count()
    print(f"Books in database: {books_count}")
    
    if authors_count > 0:
        author = Author.objects.first()
        books_by_author = author.books.count()
        print(f"{author.name} has {books_by_author} books")
    return True

def test_filtering():
    """Test filtering capabilities."""
    print("\n=== TESTING FILTERING ===")
    
    factory = RequestFactory()
    view = BookListCreateView()
    
    try:
        print("1. Testing publication year filter:")
        request = factory.get('/api/books/?publication_year=1997')
        view.request = request
        queryset = view.filter_queryset(Book.objects.all())
        count = queryset.count()
        print(f"Found {count} books from 1997")
        
        print("2. Testing year range filter:")
        request = factory.get('/api/books/?publication_year__gte=1990&publication_year__lte=2000')
        view.request = request
        queryset = view.filter_queryset(Book.objects.all())
        count = queryset.count()
        print(f"Found {count} books from 1990-2000")
        return True
        
    except Exception as e:
        print(f"Filtering test failed: {e}")
        return False

def test_search():
    """Test search functionality."""
    print("\n=== TESTING SEARCH ===")
    
    factory = RequestFactory()
    view = BookListCreateView()
    
    try:
        print("1. Testing cross-field search:")
        request = factory.get('/api/books/?search=potter')
        view.request = request
        queryset = view.filter_queryset(Book.objects.all())
        count = queryset.count()
        print(f"Found {count} books matching 'potter'")
        
        print("2. Testing author search:")
        request = factory.get('/api/books/?search=orwell')
        view.request = request
        queryset = view.filter_queryset(Book.objects.all())
        count = queryset.count()
        print(f"Found {count} books matching 'orwell'")
        
        return True
        
    except Exception as e:
        print(f"Search test failed: {e}")
        return False

def test_ordering():
    """Test ordering functionality."""
    print("\n=== TESTING ORDERING ===")
    
    factory = RequestFactory()
    view = BookListCreateView()
    
    try:
        print("1. Testing ascending order by title:")
        request = factory.get('/api/books/?ordering=title')
        view.request = request
        queryset = view.filter_queryset(Book.objects.all())
        first_book = queryset.first()
        if first_book:
            print(f"First book by title: {first_book.title}")
        
        print("2. Testing descending order by year:")
        request = factory.get('/api/books/?ordering=-publication_year')
        view.request = request
        queryset = view.filter_queryset(Book.objects.all())
        first_book = queryset.first()
        if first_book:
            print(f"Newest book: {first_book.title} ({first_book.publication_year})")
        return True
        
    except Exception as e:
        print(f"Ordering test failed: {e}")
        return False

def test_author_endpoints():
    """Test author-specific endpoints."""
    print("\n=== TESTING AUTHOR ENDPOINTS ===")
    
    factory = RequestFactory()
    view = AuthorListCreateView()
    
    try:
        print("1. Testing author name filter:")
        request = factory.get('/api/authors/?name=rowling')
        view.request = request
        queryset = view.filter_queryset(Author.objects.all())
        count = queryset.count()
        print(f"Found {count} authors matching 'rowling'")
        
        print("2. Testing author ordering:")
        request = factory.get('/api/authors/?ordering=name')
        view.request = request
        queryset = view.filter_queryset(Author.objects.all())
        count = queryset.count()
        print(f"Found {count} authors for ordering test")
        
        return True
        
    except Exception as e:
        print(f"Author endpoints test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("ADVANCED API FEATURES TEST SUITE")
    print("="*50)
    
    try:
        setup_test_data()
        
        tests = [
            ("Basic Models", test_basic_models),
            ("Filtering", test_filtering),
            ("Search", test_search),
            ("Ordering", test_ordering),
            ("Author Endpoints", test_author_endpoints),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            if test_func():
                passed += 1
            print()
        
        # Print summary
        print("=" * 50)
        print(f"TEST SUMMARY: {passed}/{total} tests passed")
        
        if passed == total:
            print("LL TESTS PASSED! Your API features are working correctly.")
            print("\nYou can now test your API endpoints:")
            print("   Books: http://localhost:8000/api/books/")
            print("   Authors: http://localhost:8000/api/authors/")
            print("\nTry these example queries:")
            print("   /api/books/?publication_year=1997")
            print("   /api/books/?search=potter")
            print("   /api/books/?ordering=-publication_year")
        else:
            print("Some tests failed. Check the output above for details.")
            
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()