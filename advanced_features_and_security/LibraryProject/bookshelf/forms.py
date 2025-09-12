# advanced_features_and_security/LibraryProject/bookshelf/forms.py
from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']

class BookSearchForm(forms.Form):
    q = forms.CharField(max_length=100, required=False)

class ExampleForm(forms.Form):
    """
    Simple example form to demonstrate CSRF protection.
    """
    sample_text = forms.CharField(
        max_length=100,
        label="Sample Text",
        help_text="Enter any text."
    )