```markdown
# Advanced API Project

A Django REST Framework project demonstrating custom serializers with nested relationships and data validation for `Author` and `Book` models.

---

## Table of Contents

- [Overview](#overview)  
- [Setup & Installation](#setup--installation)  
- [Database & Migrations](#database--migrations)  
- [Models](#models)  
- [Serializers](#serializers)  
- [Running the Server](#running-the-server)  
- [Testing & Validation](#testing--validation)  

---

## Overview

This project initializes a Django application named `advanced_api_project` with an `api` app.  
It defines two models—`Author` and `Book`—and provides custom serializers to:  
- Serialize all `Book` fields  
- Embed nested `Book` data inside each `Author`  
- Enforce that `publication_year` is not in the future  

---

## Setup & Installation

### Prerequisites

- Python 3.8 or higher  
- pip  
- (Optional) virtualenv  

### Steps

1. Clone the repository and navigate into the folder:  
   ```bash
   git clone <repo_url> advanced-api-project
   cd advanced-api-project
   ```
2. Create and activate a virtual environment:  
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:  
   ```bash
   pip install django djangorestframework
   ```

---

## Database & Migrations

1. Generate migrations for the `api` models:  
   ```bash
   python manage.py makemigrations api
   ```
2. Apply migrations to create tables in SQLite:  
   ```bash
   python manage.py migrate
   ```

---

## Models

- **Author**  
  - `name` (CharField): full name of the author  
- **Book**  
  - `title` (CharField): title of the book  
  - `publication_year` (IntegerField): year published  
  - `author` (ForeignKey → Author): links each book to its author  

The `ForeignKey` uses `related_name='books'`, so accessing `author.books.all()` returns all books by that author.

---

## Serializers

- **BookSerializer**  
  - Serializes `id`, `title`, `publication_year`, and `author`  
  - Custom validator `validate_publication_year` prevents years in the future  
- **AuthorSerializer**  
  - Serializes `id` and `name`  
  - Nested `books = BookSerializer(many=True, read_only=True)` to include all related books  

Comments in `api/serializers.py` explain how nested serialization and validation work.

---

## Running the Server

Create a superuser and start the development server:

```bash
python manage.py createsuperuser
python manage.py runserver
```

Visit the browsable API (once you add viewsets or views) at `http://localhost:8000/`.

---

## Testing & Validation

### Django Shell

Manually test creation and serialization:

```bash
python manage.py shell
```

```python
from api.models import Author
from api.serializers import BookSerializer, AuthorSerializer

# Create author
author = Author.objects.create(name='Jane Austen')

# Test future-year validation
invalid = {'title': 'Future Book', 'publication_year': 3000, 'author': author.id}
serializer = BookSerializer(data=invalid)
assert not serializer.is_valid()

# Create valid book and serialize author with nested books
valid = {'title': 'Pride and Prejudice', 'publication_year': 1813, 'author': author.id}
book = BookSerializer(data=valid); book.is_valid(raise_exception=True); book.save()
print(AuthorSerializer(author).data)
```

### Django Admin

Register models in `api/admin.py`, then use the admin UI at `http://localhost:8000/admin/` to add and inspect `Author` and `Book` instances.

---

```json
{
  "Note": "For next steps, implement views, URL routing, filtering, searching, ordering, and comprehensive unit tests."
}
```
```