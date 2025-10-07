# Social Media API

## Overview
A Django REST Framework–based API providing user authentication with token support.

## Setup
1. Clone repository  
2. Install dependencies: `pip install -r requirements.txt`  
3. Apply migrations:  
   ```bash
   python manage.py makemigrations
   python manage.py migrate
4. Create superuser: python manage.py createsuperuser

5. Run server: python manage.py runserver

## Authentication Endpoints
- Register: POST /api/auth/register/

- Login: POST /api/auth/login/

Request bodies must include username and password. Registration accepts optional email, bio, and profile_picture.

## User Model Fields
- username, email, password

- bio: Text field

- profile_picture: Image upload

- followers: Self-referential many-to-many