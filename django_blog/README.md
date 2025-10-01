markdown
# django_blog

A simple Django-based blog platform with user authentication, CRUD for posts, comments, tagging, and search.

---

## Features

- User registration, login, logout, and profile management  
- Create, view, update, and delete blog posts  
- Comment on posts (CRUD)  
- Tag posts and browse by tag  
- Search posts by title, content, or tags  
- Secure forms with CSRF protection  

---

## Prerequisites

- Python 3.8+  
- pip  
- (Optional) PostgreSQL for production  

---

## Installation

1. Clone the repository:  
   ```bash
   git clone https://github.com/YourUsername/Alx_DjangoLearnLab.git
   cd Alx_DjangoLearnLab/django_blog
Create and activate a virtual environment:

bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
Install dependencies:

bash
pip install -r requirements.txt
Copy environment variables:

bash
cp .env.example .env
# Edit .env to configure SECRET_KEY, DEBUG, DATABASE_URL, etc.
Database Setup
SQLite (default) No extra setup needed. Migrations will create db.sqlite3.

PostgreSQL

Install psycopg2-binary:

bash
pip install psycopg2-binary
Update DATABASES in django_blog/settings.py with your credentials (port 5432).

Run migrations:

bash
python manage.py makemigrations
python manage.py migrate
Running the Development Server
bash
python manage.py runserver
Visit http://127.0.0.1:8000/ in your browser.

URL Endpoints
/register/ – User signup

/login/ – User login

/logout/ – User logout

/profile/ – View/update profile

/posts/ – List all posts

/posts/new/ – Create a post

/posts/<pk>/ – Post details

/posts/<pk>/edit/ – Edit a post

/posts/<pk>/delete/ – Delete a post

/search/?q=keyword – Search posts

/tags/<tag>/ – Posts by tag

Testing
Run the full test suite:

bash
python manage.py test
Tests cover authentication flows, post CRUD, and comments.

## Blog Post Features

- CRUD operations for posts:
  - List all posts: `/posts/`
  - View single post: `/posts/<pk>/`
  - Create post (auth only): `/posts/new/`
  - Edit post (author only): `/posts/<pk>/edit/`
  - Delete post (author only): `/posts/<pk>/delete/`

### Permissions

- Anyone can browse and read posts.
- Only authenticated users can create posts.
- Only the author of a post can edit or delete it.

## Comment System

- Model: `Comment` links to `Post` and `User`, with timestamps.  
- Views:
  - Inline creation on post detail (`posts/<pk>/comments/new/`).  
  - Edit (`comments/<pk>/edit/`) and delete (`comments/<pk>/delete/`) via mixins.  
- Templates:
  - Comments shown on `post_detail.html`, with edit/delete links.  
  - `comment_form.html` for editing.  
  - `comment_confirm_delete.html` for deletion confirmation.  
- Permissions:
  - Only authenticated users can post comments.  
  - Only comment authors can edit or delete their comments.  

## Features: Tagging & Search

- Assign comma-separated tags to posts via the post form.  
- Browse posts by tag at `/tags/<tag_name>/`.  
- Search title, content, or tag names via `/search/?q=keyword`.

## URL Endpoints

- `/tags/<tag_name>/` – View all posts with the given tag.  
- `/search/?q=<keyword>` – Search posts by keyword or tag.
