from rest_framework import serializers
from datetime import date
from .models import Author, Book

class BookSerializer(serializers.ModelSerializer):
    """
    Serializes all fields of Book.
    Validates that publication_year is not in the future.
    """
    def validate_publication_year(self, value):
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                "Publication year cannot be in the future."
            )
        return value

    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializes Author.name and nests BookSerializer to include related books.
    The 'books' field is read-only and generated from Book.author via related_name.
    """
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
