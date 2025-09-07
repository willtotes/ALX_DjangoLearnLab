import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_models.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def create_sample_data():
    author1 = Author.objects.create(name="J.K Rowling")
    author2 = Author.objects.create(name='George R.R. Martin')

    book1 = Book.objects.create(title="Harry Potter and the Philosopher's Stone", author=author1)
    book2 = Book.objects.create(title="Harry Potter and the Chamber of Secrets", author=author1)
    book3 = Book.objects.create(title="A Game of Thrones", author=author2)

    library1 = Library.objects.create(name="Central Public Library")
    library2 = Library.objects.create(name="City Library")
    library1.books.add(book1, book2)
    library2.books.add(book3)

    librarian1 = Librarian.objects.create(name="Alice Doe", library=library1)
    librarian2 = Librarian.objects.create(name="Bob Smith", library=library2)

    return author1, author2, library1, library2

def query_all_books_by_author():
    print("Query: All books by J.K Rowling")
    try:
        author = Author.objects.get(name="J.K Rowling")
        books = Book.objects.filter(author=author)
        for book in books:
            print(f"_ {book.title}")
        return books
    except Author.DoesNotExist:
        print("Author not found")
        return []

def list_all_books_in_library():
    print("Query: All books in Central Public Library")
    try:
        library = Library.objects.get(name="Central Public Library")
        books = library.books.all()
        for book in books:
            print(f"_ {book.title} (by {book.author.name})")
        return books
    except Library.DoesNotExist:
        print("Library not found")
        return []

def retrieve_librarian_for_library():
    print("Query: Librarian for Central Public Library")
    try:
        library = Library.objects.get(name="Central Public Library")
        librarian = Librarian.objects.get(library=library)
        print(f"Librarian: {librarian.name}")
        return librarian
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        print("Library or Librarian not found")
        return None

if __name__ == "__main__":
    print("Creating sample data...")
    create_sample_data()

    query_all_books_by_author()
    list_all_books_in_library()
    retrieve_librarian_for_library()
