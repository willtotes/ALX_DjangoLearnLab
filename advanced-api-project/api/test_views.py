from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from .models import Author, Book
from .serializers import BookSerializer, AuthorSerializer

# Create your tests here.
class BaseTestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username='admin',
            password='adminpass123',
            email='admin@example.com'
        )
        self.regular_user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='user@example.com'
        )
        self.author1 = Author.objects.create(name='J.K. Rowling')
        self.author2 = Author.objects.create(name='George Orwell')
        self.author3 = Author.objects.create(name='J.R.R. Tolkien')

        self.book1 = Book.objects.create(
            title="Harry Potter and the Philosopher's Stone",
            publication_year=1997,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title="1984",
            publication_year=1949,
            author=self.author2
        )
        self.book3 = Book.objects.create(
            title="Animal Farm",
            publication_year=1945,
            author=self.author2
        )
        self.book4 = Book.objects.create(
            title="The Hobbit",
            publication_year=1937,
            author=self.author3
        )
        
        self.client = APIClient()
        self.book_list_url = reverse('book-list')
        self.book_detail_url = lambda pk: reverse('book-retrieve-update-destroy', kwargs={'pk': pk})
        self.book_create_url = reverse('book-create')
        self.book_combined_url = reverse('book-list-create')
        
        self.author_list_url = reverse('author-list-create')
        self.author_detail_url = lambda pk: reverse('author-detail', kwargs={'pk': pk})

    def authenticate_user(self, user):
        self.client.force_authenticate(user=user)

    def remove_authentication(self):
        self.client.force_authenticate(user=None)

class BookCRUDTest(BaseTestCase):
    def test_list_books_unauthenticated(self):
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 4)
        self.assertIn('title', response.data['results'][0])
        self.assertIn('author', response.data['results'][0])

    def test_retrieve_book_unauthenticated(self):
        url = self.book_detail_url(self.book1.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
        self.assertEqual(response.data['publication_year'], self.book1.publication_year)

    def test_create_book_authenticated(self):
        self.authenticate_user(self.regular_user)

        book_data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post(self.book_list_url, book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['title'], book_data['title'])
        self.assertEqual(Book.objects.count(), 5)

    def test_create_book_unauthenticated(self):
        book_data = {
            'title': 'Unauthorized Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post(self.book_list_url, book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book_authenticated(self):
        self.authenticate_user(self.regular_user)

        update_data = {
            'title': 'Updated Book Title',
            'publication_year': 1998,
            'author': self.author1.id
        }
        url = self.book_detail_url(self.book1.id)
        response = self.client.put(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Book Title')
        self.assertEqual(self.book1.publication_year, 1998)

    def test_partial_update_book_authenticated(self):
        self.authenticate_user(self.regular_user)

        update_data = {
            'title': 'Partially Updated Title'
        }
        url = self.book_detail_url(self.book1.id)
        response = self.client.patch(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Partially Updated Title')
        self.assertEqual(self.book1.publication_year, 1997)

    def test_delete_book_authenticated(self):
        self.authenticate_user(self.regular_user)

        url = self.book_detail_url(self.book1.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 3)
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())
    
    def test_delete_book_unauthenticated(self):
        url = self.book_detail_url(self.book1.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Book.objects.count(), 4)

class BookFilteringTests(BaseTestCase):
    def test_publication_year_validation_future_year(self):
        self.authenticate_user(self.regular_user)

        from django.utils import timezone
        future_year = timezone.now().year + 1
        book_data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author1.id
        }
        response = self.client.post(self.book_list_url, book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)

    def test_publication_year_validation_past_year(self):
        self.authenticate_user(self.regular_user)
        book_data = {
            'title': 'Historical Book',
            'publication_year': 1901,
            'author': self.author1.id
        }
        response = self.client.post(self.book_list_url, book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_unique_together_validation(self):
        self.authenticate_user(self.regular_user)
        book_data = {
            'title': self.book1.title,
            'publication_year': 2000,
            'author': self.book1.author.id
        }
        response = self.client.post(self.book_list_url, book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_required_fields_validation(self):
        self.authenticate_user(self.regular_user)
        book_data = {
            'publication_year': 2000,
            'author': self.author1.id
        }
        response = self.client.post(self.book_list_url, book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)

class AuthorCRUDTests(BaseTestCase):
    def test_list_authors_unauthenticated(self):
        response = self.client.get(self.author_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)

    def test_retrieve_author_unauthenticated(self):
        url = self.author_detail_url(self.author1.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.author1.name)
        self.assertIn('books', response.data)

    def test_create_author_authenticated(self):
        self.authenticate_user(self.regular_user)
        author_data = {
            'name': 'New Test Author'
        }
        response = self.client.post(self.author_list_url, author_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 4)

    def test_update_author_authenticated(self):
        self.authenticate_user(self.regular_user)
        update_data = {
            'name': 'Updated Author Name'
        }
        url = self.author_detail_url(self.author1.id)
        response = self.client.put(url,update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.author1.refresh_from_db()
        self.assertEqual(self.author1.name, 'Updated Author Name')

    def test_delete_author_authenticated(self):
        self.authenticate_user(self.regular_user)
        url = self.author_detail_url(self.author3.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Author.objects.count(), 2)

    def test_author_name_required(self):
        self.authenticate_user(self.regular_user)
        response = self.client.post(self.author_list_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    def test_publication_year_min_value(self):
        self.authenticate_user(self.regular_user)
        book_data = {
            'title': 'Test Book',
            'publication_year': 0,
            'author': self.author1.id
        }
        response = self.client.post(self.book_list_url, book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)

class PaginationTests(BaseTestCase):
    def test_books_pagination(self):
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('results', response.data)

    def test_authors_pagination(self):
        response = self.client.get(self.author_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('results', response.data)

class ErrorHandlingTests(BaseTestCase):
    def test_nonexistent_book_retriever(self):
        url = self.book_detail_url(9999)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_nonexistent_book(self):
        self.authenticate_user(self.regular_user)
        url = self.book_detail_url(9999)
        response = self.client.put(url, {'title': 'Test'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_nonexistent_book(self):
        self.authenticate_user(self.regular_user)
        url = self.book_detail_url(9999)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_nonexistent_author_retrieve(self):
        url = self.author_detail_url(9999)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_book_data(self):
        self.authenticate_user(self.regular_user)
        invalid_data = {
            'title': '',
            'publication_year': 'not-a-number',
            'author': 9999
        }
        response = self.client.post(self.book_list_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
