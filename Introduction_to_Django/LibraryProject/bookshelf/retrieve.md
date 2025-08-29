from bookshelf.models import Book

book = Book.objects.get(title="1984")
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")

all_books = Book.objects.all()
print(f"Total books: {all_books.count()}")
