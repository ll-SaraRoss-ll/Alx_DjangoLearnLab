import os
import sys
from pathlib import Path

# --- Setup Django environment ---
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')

import django
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# ---- 1) Query all books by a specific author ----
author_name = 'J.K. Rowling'
try:
    author = Author.objects.get(name=author_name)
    books_by_author = Book.objects.filter(author=author)
    print(f"Books by {author_name}:")
    for book in books_by_author:
        print(f" - {book.title}")
except Author.DoesNotExist:
    print(f"No author found with name '{author_name}'")

# ---- 2) List all books in a library ----
library_name = 'Central Library'
try:
    library = Library.objects.get(name=library_name)
    print(f"\nBooks in {library_name}:")
    for book in library.books.all():
        print(f" - {book.title} (Author: {book.author.name})")
except Library.DoesNotExist:
    print(f"No library found with name '{library_name}'")

# ---- 3) Retrieve the librarian for a library ----
try:
    librarian = Librarian.objects.get(library=library)
    print(f"\nLibrarian at {library_name}: {librarian.name}")
except (Librarian.DoesNotExist, NameError):
    print(f"No librarian assigned to '{library_name}'")
