from bookshelf.models import Book

view_books = Book.objects.all()
print(f"Book list: {view_books}")
