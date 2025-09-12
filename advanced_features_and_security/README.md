## Permissions and Groups Setup

I added four custom permissions to `Book`:

- `can_view`  
- `can_create`  
- `can_edit`  
- `can_delete`  

Three groups manage these:

| Group   | Permissions                      |
| ------- | -------------------------------- |
| Viewers | can_view                         |
| Editors | can_view, can_create, can_edit   |
| Admins  | can_view, can_create, can_edit, can_delete |

Views are protected with:
```python
@permission_required('bookshelf.can_edit', raise_exception=True)

## Security Best Practices

- DEBUG disabled in production  
- XSS filters, clickjacking and MIME-sniff protections enabled  
- CSRF tokens in all forms  
- ORM usage prevents SQL injection  
- Content Security Policy restricts external assets

## HTTPS & Secure Redirects

1. **settings.py**  
   - `SECURE_SSL_REDIRECT = True` redirects all HTTP to HTTPS.  
   - `SECURE_HSTS_SECONDS = 31536000`, `INCLUDE_SUBDOMAINS`, `PRELOAD` enable HSTS.  
   - `SESSION_COOKIE_SECURE` & `CSRF_COOKIE_SECURE` ensure cookies use HTTPS only.  
   - `X_FRAME_OPTIONS='DENY'`, `SECURE_CONTENT_TYPE_NOSNIFF`, `SECURE_BROWSER_XSS_FILTER` add clickjacking, MIME-sniff, and XSS protections.  
   - Development override via `if DEBUG:` block disables HTTPS enforcement locally.

2. **Deployment (Nginx)**  
   - HTTP→HTTPS redirect server block.  
   - SSL server block with Let’s Encrypt cert paths.  
   - Proxy headers for correct `X-Forwarded-Proto`.  
