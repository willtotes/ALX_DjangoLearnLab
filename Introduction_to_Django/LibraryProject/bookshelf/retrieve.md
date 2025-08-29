from bookshelf.models import Book

view_books = Book.objects.all()
print(f"Book list: {view_books}")

for books in view_books:
    print(f"Title: {book.title}")
    print(f"Author: {book.author}")
    print(f"Publication year: {book.publication_year}")
