# Deployment guide for social_media_api

## Purpose
This document lists required environment variables, exact commands I ran (or will run) to deploy, and where deployment config files live in the repo.

## Required environment variables
- DJANGO_SECRET_KEY
- DATABASE_URL
- ALLOWED_HOSTS
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_STORAGE_BUCKET_NAME
- EMAIL_HOST
- EMAIL_PORT
- EMAIL_HOST_USER
- EMAIL_HOST_PASSWORD
- SENTRY_DSN (optional)

## Files included for deployment
- Procfile (repo root)
- requirements.txt (repo root)
- runtime.txt (repo root)
- social_media_api/settings/production.py
- deploy/nginx/social_media_api.conf
- deploy/systemd/gunicorn.service
- deploy/postman_collection.json (verification)
- deploy/verification.md (curl snippets)

## Deploy commands (Heroku - quick path)
1. Create app and push:
   - `heroku create your-app-name`
   - `git push heroku main`
2. Set env vars:
   - `heroku config:set DJANGO_SECRET_KEY="..." ALLOWED_HOSTS="your-app-name.herokuapp.com"`
3. Provision Postgres:
   - `heroku addons:create heroku-postgresql:hobby-dev`
4. Run migrations and collectstatic:
   - `heroku run python manage.py migrate --settings=social_media_api.settings.production`
   - `heroku run python manage.py collectstatic --noinput --settings=social_media_api.settings.production`

## Deploy commands (Ubuntu VM / DigitalOcean)
1. On server:
   - `sudo apt update && sudo apt install python3-venv python3-pip nginx postgresql certbot python3-certbot-nginx`
2. Clone repo and install:
   - `git clone <repo-url> /srv/social_media_api`
   - `cd /srv/social_media_api`
   - `python3 -m venv venv`
   - `source venv/bin/activate`
   - `pip install -r requirements.txt`
3. Configure DB, env vars, run:
   - `python manage.py migrate --settings=social_media_api.settings.production`
   - `python manage.py collectstatic --noinput --settings=social_media_api.settings.production`
4. Systemd + Nginx:
   - Copy `deploy/systemd/gunicorn.service` to `/etc/systemd/system/gunicorn.service`
   - `sudo systemctl daemon-reload && sudo systemctl start gunicorn && sudo systemctl enable gunicorn`
   - Copy `deploy/nginx/social_media_api.conf` to `/etc/nginx/sites-available/` and `ln -s` to sites-enabled
   - `sudo nginx -t && sudo systemctl restart nginx`
5. SSL:
   - `sudo certbot --nginx -d api.example.com`

## Verification commands (curl)
- Login (adjust endpoint):
  - `curl -X POST https://api.example.com/api/auth/login/ -H "Content-Type: application/json" -d '{"username":"test","password":"pass"}'`
- List posts:
  - `curl https://api.example.com/api/posts/`
- Create post:
  - `curl -X POST https://api.example.com/api/posts/ -H "Content-Type: application/json" -H "Authorization: Bearer TOKEN" -d '{"title":"Hi","content":"Hello"}'`

## Where to find files in this repo
- `/Procfile`
- `/requirements.txt`
- `/runtime.txt`
- `/social_media_api/settings/production.py`
- `/deploy/nginx/social_media_api.conf`
- `/deploy/systemd/gunicorn.service`
- `/deploy/postman_collection.json`
- `/deploy/verification.md`

## Notes
- Do not commit secrets or .env files.  
- After deployment, paste the live URL here: `LIVE_URL: https://api.example.com`.
