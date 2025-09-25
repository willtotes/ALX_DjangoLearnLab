from django.db import models
from django.db.models import Q

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author,
        on_delete=models.PROTECT,
        related_name='books'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
        unique_together = ['title', 'author']
        indexes = [
            models.Index(fields=['publication_year']),
            models.Index(fields=['author', 'publication_year']),
        ]
        constraints = [
            models.CheckConstraint(
                check= Q(publication_year__gte=1000),
                name='publication_year_min_value'
            )
        ]

    def __str__(self):
        return f"{self.title} by {self.author.name}"
