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

def query_all_books_by_author(author_name="J.K Rowling"):
    print(f"Query: All books by {author_name}}")
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        for book in books:
            print(f"_ {book.title}")
        return books
    except Author.DoesNotExist:
        print("Author not found")
        return []

def list_all_books_in_library(library_name="Central Public Library"):
    print(f"Query: All books in {library_name}")
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        for book in books:
            print(f"_ {book.title} (by {book.author.name})")
        return books
    except Library.DoesNotExist:
        print("Library not found")
        return []

def retrieve_librarian_for_library(library_name="Central Public Library"):
    print(f"Query: Librarian for {library_name}")
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
