# PolyGhar BACKEND (Django) — admin panel + product API

This is the "brain" of your store. It has NO public pages — it does two jobs:

1. **Admin panel** (`/admin`) — where you add/edit products, upload photos,
   set price, quantity, build time, and your WhatsApp number.
2. **API** (`/api/...`) — feeds product data to your separate frontend site.

## Run it locally

You need Python 3.11+ (python.org — tick "Add Python to PATH" on Windows).

```
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   ← invent your admin login
python manage.py runserver
```

- Admin panel: http://127.0.0.1:8000/admin
- API (what the frontend reads): http://127.0.0.1:8000/api/products/

Demo products are already loaded. Remove them in the admin whenever.

## Managing products (in the admin)

- **Add:** Products → Add product → fill the form → upload photos at the
  bottom (first photo = thumbnail) → Save. Live instantly.
- **Photos:** add more rows to upload more; tick "Delete" on a row + Save to remove.
- **Sold out:** set quantity to 0 (badge shows, product stays visible).
- **Hide without deleting:** untick "published".
- **Your WhatsApp number / brand / bio / socials:** Site settings section.

## API endpoints (for reference)

| URL | Returns |
|-----|---------|
| `/api/health/` | is the backend alive |
| `/api/products/` | all published products |
| `/api/products/<slug>/` | one product with gallery + specs |
| `/api/settings/` | brand, WhatsApp number, socials, bio |

## Deploy to PythonAnywhere (free)

Same steps as a normal Django app — see INTEGRATION.md in this folder
for the full walkthrough including connecting the frontend.

**Backup tip:** your entire store = `db.sqlite3` + the `media/` folder.
