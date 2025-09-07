from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from .models import Book, Library
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Book
from .models import Author
from .models import Library
from .models import Librarian
from .forms import BookForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView


def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'relationship_app/book_detail.html', {'book':book})

@login_required
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully!')
            return redirect('list_books')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookForm

    return render(request, 'relationship_app/add_book.html', {'form': form})

@login_required
@permission_required('relationship.can_change_book', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        form = BookForm(request.POST, instance = book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('book_detail', pk = book.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookForm(instance = book)
    
    return render(request, 'relationship_app/edit_book.html', {
        'form': form,
        'book': book
    })

@login_required
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.success(request, f'Book "{book_title}" deleted successfully!')
        return redirect('list_books')
    return render(request, 'relationship_app/delete_book.html', {'book': book})

def library_detail(request, library_id):
    library = get_object_or_404(library, id=library_id)
    books = library.books.all()
    return render(request, 'relationship_app/library_detail.html', {
        'library': library,
        'books': books,
    })

@login_required
def librarian_view(request):
    try:
        librarian = Librarian.objects.get(name = request.user.username)
        return render(request, 'relationship_app/librarian_view.html', {'librarian': librarian
        })
    except Librarian.DoesNotExist:
        return HttpResponse("You are not authorized to view this page.", status=403)

@login_required
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

def admin_view(request):
    if request.user.is_staff:
        return render(request, 'relationship_app/admin_view.html')
    else:
        return HttpResponse("You are not authorized to view this page.", status = 403)

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'relationship/register.html'
    success_url = reverse_lazy('login')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})

class CustomLoginView(LoginView):
    template_name = "relationship_app/login.html"

    def get_success_url(self):
        return reverse_lazy('home')

class CustomLogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'