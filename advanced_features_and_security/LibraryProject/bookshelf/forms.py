from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Book, Author
import re

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'date_of_birth')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'date_of_birth', 'profile_photo')

class BookForm(forms.ModelForm):
    model = Book
    fields = [
        'title',
        'author',
        'published_date',
        'isbn',
        'description'
    ]
    widgets = {
        'published_date': forms.DateInput(attrs={'type': 'date'}),
        'description': forms.Textarea(attrs={'rows': 4}),
    }

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'bio', 'date_of_birth', 'death_date']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'death_date': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'row': 4}),
        }

class SecureBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year', 'isbn', 'description']
        widgets = {
            'description': forms.Textarea({'rows': 4}),
        }

        def clean_title(self):
            title = self.cleaned_data['title']
            title = re.sub(r'<script.*?>.*?</script>', '', title, flags=re.IGNORECASE)
            return title.strip()

        def clean_description(self):
            description = self.cleaned_data['description']
            if description:
                description = re.sub(r'on\w+=\s*["\']', '', description)
            return description
        
        def clean_publication_year(self):
            year = self.cleaned_data['publication_year']
            if year < 1000 or year > 2030:
                raise forms.ValidationError("Invalid publication year.")
            return year
        
        def clean_isbn(self):
            isbn = self.cleaned_data['isbn']
            if isbn and not re.match(r'^[0-9-]{10,17}$', isbn):
                raise forms.ValidationError("Invalid ISBN format")
            return isbn