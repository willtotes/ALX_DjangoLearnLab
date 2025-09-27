from django.shortcuts import render
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q
from .filters import BookFilter, AuthorFilter

# Create your views here.
class AuthorListCreateView(generics.ListCreateAPIView):
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AuthorFilter
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [rest_framework.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookFilter
    filterset_fields = ['publication_year', 'author__id']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year', 'created_at']
    ordering = ['title']

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    #def get_queryset(self):
    #    queryset = super().get_queryset()
        #min_year = self.request.query_params.get('min_year')
        #max_year = self.request.query_params.get('max_year')

        #if min_year:
        #    queryset = queryset.filter(publication_year__gte=min_year)
        #if max_year:
        #    queryset = queryset.filter(publication_year__lte=max_year)

        #author_ids = self.request.query_params.get('author_ids')
        #if author_ids:
        #    try:
        #        ids_list = [int(id.strip()) for id in author_ids.split(',')]
        #        queryset = queryset.filter(author__id__in=ids_list)
        #    except (ValueError, TypeError):
        #        pass

        #return queryset
    
    def perform_create(self, serializer):
        book_title = serializer.validated_data.get('title')
        author = serializer.validated_data.get('author')
        print(f"Creating new book: '{book_title}' by {author.name}")
        super().perform_create(serializer)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {
            'message': 'Book created successfully',
            'data': response.data
        }
        return response
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        queryset = self.filter_queryset(self.get_queryset())
        response.data['filter_metadata'] = {
            'total_count': queryset.count(),
            'available_filters': {
                'publication_year': 'Exact year or range (gte, lte, gt, lt)',
                'author_name': 'Partial author name search',
                'title': 'Partial title search',
                'search': 'Search across title and author name',
                'ordering': f'Available fields: {", ".join(self.ordering_fields)}'
            },
            'current_filters': dict(request.query_params)
        }
        return response

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [rest_framework.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookFilter
    filterset_fields = ['publication_year', 'author__id']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year', 'created_at']
    ordering = ['title']

class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'

class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {
            'message': 'Book created successfully',
            'data': response.data
        }
        return response
    
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data = {
            'message': 'Book updated successfully',
            'data': response.data
        }
        return response
    
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        book_title = instance.title
        self.perform_destroy(instance)
        return Response(
            {
                'message': f'Book "{book_title}" deleted successfully',
                'deleted_id': kwargs['pk']
            },
            status=status.HTTP_204_NO_CONTENT
        )

class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    lookup_field = 'pk'

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data = {
            'message': 'Book updated successfully',
            'data': response.data
        }
        return response

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        book_title = instance.title
        self.perform_destroy(instance)
        return Response(
            {
                'message': f"Book '{book_title}' deleted successfully",
                'deleted_id': kwargs['pk']
            },
            status=status.HTTP_204_NO_CONTENT
        )
    
class AuthorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    lookup_field = 'pk'

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]