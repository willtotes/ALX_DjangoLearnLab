from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db import models
from django.http import HttpResponseForbidden, JsonResponse
from .models import Book, Author
from .forms import AuthorForm, BookForm
import re

# Create your views here.
@login_required
@permission_required('bookshelf.can_view_book', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@login_required
@permission_required('bookshelf.can_view_book', raise_exception=True)
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'bookshelf/book_detail.html', {'book': book})

@login_required
@permission_required('bookshelf.can_create_book', raise_exception=True)
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" created successfully!')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm()
    return render(request, 'bookshelf/book_form.html', {'form': form, 'action': 'Create'})

@login_required
@permission_required('bookshelf.can_edit_book', raise_exception=True)
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" updated successfully!')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(request, 'bookshelf/book_form.html', {'form': form, 'action': 'Edit'})

@login_required
@permission_required('bookshelf.can_delete_book', raise_exception=True)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.success(request, f'Book "{book_title}" deleted successfully!')
        return redirect('book_list')
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})

@login_required
@permission_required('bookshelf.can_view_author', raise_exception=True)
def author_list(request):
    authors = Author.objects.all()
    return render(request, 'bookshelf/author_list.html', {'authors': authors})

@login_required
@permission_required('bookshelf.can_create_author', raise_exception=True)
def author_create(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = form.save()
            messages.success(request, f'Author "{author.name}" created successfully!')
            return redirect('author_list')
    else:
        form = AuthorForm()
    return render(request, 'bookshelf/author_form.html', {'form': form, 'action': 'Create'})

@login_required
@permission_required('bookshelf.can_edit_author', raise_exception=True)
def author_edit(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            author = form.save()
            messages.success(request, f'Author "{author.name}" updated successfully!')
            return redirect('author_list')
    else:
        form = AuthorForm(instance=author)
    return render(request, 'bookshelf/author_form.html', {'form': form, 'action': 'Edit'})

@login_required
def secure_search(request):
    query = request.GET.get('q', '').strip()

    if not re.match(r'^[a-zA-z0-9\s\.,!?-]*$', query):
        messages.error(request, 'Invalid search characters.')
        return render(request, 'bookshelf/search.html', {'book': []})

    books = Book.objects.filter(
        models.Q(title__icontains=query) |
        models.Q(author__icontains=query) |
        models.Q(description__icontains=query)
    )[:50]

    return render(request, 'bookshelf/search.html', {'books': books, 'query': query})

@login_required
@permission_required('bookshelf.can_create_book', raise_exception=True)
def book_create_secure(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book_data = form.cleaned_data
            if book_data['publication_year'] < 1000 or book_data['publication_year'] > 2030:
                messages.error(request, 'Invalid publication year.')
                return render(request, 'bookshelf/form_example.html', {'form': form, 'title': 'Create Book'})

            if book_data['isbn'] and not re.match(r'^[0-9-]{10,17}$', book_data['isbn']):
                messages.error(request, 'Invalid ISBN format.')
                return render(request, 'bookshelf/form_example.html', {'form': form, 'title': 'Create Book'})

            if book_data['description']:
                book_data['description'] = re.sub(r'<script.*?>.*?</script>', '', book_data['description'], flags=re.IGNORECASE)

            book = form.save()
            messages.success(request, f'Book "{book.title}" created successfully!')

            return redirect('book_detail', pk=book.pk)
        else:
            form = BookForm()

        return render(request, 'bookshelf/form_example.html', {'form': form, 'title': 'Create Book'})

@login_required
def safe_redirect(request):
    next_url = request.Get.get('next', '/')

    if not next_url.startswith(('/books/', '/authors/', '/', '')):
        next_url = '/'

    return redirect(next_url)