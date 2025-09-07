from django import forms
from .models import Book
from .models import Author

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year', 'isbn', 'pages', 'cover', 'language']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book title'
            }),
            'author': forms.Select(attrs={
                'class': 'form-control'
            }),
            'publication_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 2024'
            }),
            'isbn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 9781347583980'
            }),
            'pages': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Number of pages'
            }),
            'language': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., English'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].queryset = Author.objects.all()

    def clean_ibsn(self):
        isbn = self.cleaned_data.get('isbn')
        if isbn:
            isbn = isbn.replace(' ', '').replace('-', '')
            if not isbn.isdigit() or len(isbn) not in [10, 13]:
                raise forms.ValidationError('ISBN must be 10 or 13 digits long.')
        return isbn

    def clean_publication_year(self):
        year = self.cleaned_data.get('publication_year')
        if year:
            import datetime
            current_year = datetime.datetime.now().year
            if year < 1000 or year > current_year +1:
                raise forms.ValidationError(f"Publication year must between 1000 and {current_year + 1}.")
            return year
            