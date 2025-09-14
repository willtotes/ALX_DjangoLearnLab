from bookshelf.models import Book

book.delete()
books_remaining = Book.objects.all()
print(f"Books remaining: {books_remaining.count()}")
