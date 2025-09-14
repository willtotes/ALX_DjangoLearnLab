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
        
class ExampleForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'})
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "Enter your email"})
    )

    age = forms.IntegerField(
        required=True,
        min_value=0,
        max_value=150,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    agree_to_terms = forms.BooleanField(
        required=True,
        label="I agree to the terms and conditions"
    )
    
    MESSAGE_CHOICES = [
        ('general', 'General Inquiry'),
        ('support', 'Technical Support'),
        ('feedback', 'Feedback'),
        ('complaint', 'Complaint'),
    ]
    
    message_type = forms.ChoiceField(
        choices=MESSAGE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    message = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter your message'})
    )
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name.strip()) < 2:
            raise forms.ValidationError("Name must be at least 2 characters long.")
        return name.strip()
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise forms.ValidationError("Please enter a valid email address.")
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        message_type = cleaned_data.get('message_type')
        message = cleaned_data.get('message')
        
        if message_type in ['feedback', 'complaint'] and not message:
            raise forms.ValidationError({
                'message': "This message type requires a detailed message."
            })
        
        return cleaned_data