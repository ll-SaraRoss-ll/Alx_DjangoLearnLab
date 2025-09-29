from django.db import models

class Author(models.Model):
    # Stores the author’s full name
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Book(models.Model):
    # Title of the book
    title = models.CharField(max_length=255)
    # Year the book was published
    publication_year = models.IntegerField()
    # Links each book to one Author; Author.books will return all related Book instances
    author = models.ForeignKey(
        Author,
        related_name='books',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
