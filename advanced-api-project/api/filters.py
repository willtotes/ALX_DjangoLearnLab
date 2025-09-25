import django_filters
from django.db.models import Q
from .models import Book, Author
from django_filters.rest_framework import BaseInFilter, NumberFilter

class NumberInFilter(BaseInFilter, NumberFilter):
    pass

class BookFilter(django_filters.FilterSet):
    publication_year = django_filters.NumberFilter(field_name='publication_year', lookup_expr='exact')
    publication_year__gt = django_filters.NumberFilter(field_name='publication_year', lookup_expr='gt')
    publication_year__lt = django_filters.NumberFilter(field_name='publication_year', lookup_expr='lt')
    publication_year__gte = django_filters.NumberFilter(field_name='publication_year', lookup_expr='gte')
    publication_year__lte = django_filters.NumberFilter(field_name='publication_year', lookup_expr='lte')
    
    publication_year_range = django_filters.NumericRangeFilter(field_name='publication_year')
    
    author = django_filters.NumberFilter(field_name='author__id')
    author_name = django_filters.CharFilter(field_name='author__name', lookup_expr='icontains')
    author_ids = NumberInFilter(field_name='author__id', lookup_expr='in')

    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    title_exact = django_filters.CharFilter(field_name='title', lookup_expr='exact')
    title_startswith = django_filters.CharFilter(field_name='title', lookup_expr='istartswith')
    
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    updated_after = django_filters.DateTimeFilter(field_name='updated_at', lookup_expr='gte')
    updated_before = django_filters.DateTimeFilter(field_name='updated_at', lookup_expr='lte')
    
    search = django_filters.CharFilter(method='custom_search', label="Search across title and author name")
    
    class Meta:
        model = Book
        fields = {
            'publication_year': ['exact', 'gte', 'lte', 'gt', 'lt'],
            'author__name': ['exact', 'icontains'],
            'title': ['exact', 'icontains', 'istartswith'],
            'author__id': ['exact', 'in']
        }
    
    def custom_search(self, queryset, name, value):
        if not value or not value.strip():
            return queryset
        return queryset.filter(
            Q(title__icontains=value.strip()) | 
            Q(author__name__icontains=value.strip())
        )


class AuthorFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    name_exact = django_filters.CharFilter(field_name='name', lookup_expr='exact')
    has_books = django_filters.BooleanFilter(method='filter_has_books', label="Authors with books")
    
    class Meta:
        model = Author
        fields = ['name']
    
    def filter_has_books(self, queryset, name, value):
        if value is True:
            return queryset.filter(books__isnull=False).distinct()
        elif value is False:
            return queryset.filter(books__isnull=True)
        return queryset