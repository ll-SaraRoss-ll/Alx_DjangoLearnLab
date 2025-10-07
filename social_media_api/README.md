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

## Endpoints, required auth:
- Follow: POST /api/auth/follow/5/ Authorization: Token <token>

- Unfollow: POST /api/auth/unfollow/5/

- Followers list: GET /api/auth/5/followers/

- Feed: GET /api/feed/ (returns posts from users you follow, newest first)

Model change note: added self-referential ManyToMany field to User for follows; run migrations.

# API Documentation (examples)
Endpoint: POST /posts/<pk>/like/

- Auth: required (Token/Session)

- Request: none in body

- Success Response 201:

   { "id": 12, "user": 3, "post": 7, "created_at": "2025-10-07T12:00:00Z" }

- Error 400 if already liked:

   { "detail": "Already liked" }

Endpoint: POST /posts/<pk>/unlike/

- Auth: required

- Success Response 204 (empty)

- Error 400 if not liked:

   { "detail": "Like does not exist" }

Endpoint: GET /notifications/

- Auth: required

- Response 200:

   [ { "id": 5, "recipient": 2, "actor": { "id": 3, "username": "alice" }, "verb": "liked your post", "target": { "type": "post", "id": "7" }, "timestamp": "2025-10-07T12:01:00Z", "read": false }, ]

- Unread notifications are those with read == false. Clients can display unread first by checking the read field.

Endpoint: POST /notifications/<pk>/read/

- Auth: required

- Body: none

- Success 200:

   { "detail": "Marked as read" }