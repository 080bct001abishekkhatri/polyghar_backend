# Connecting the frontend and backend (do this LAST)

You have two separate projects:

```
polyghar-backend/    Django — admin panel + API      → hosts on PythonAnywhere
polyghar-frontend/   Next.js — the site buyers see   → hosts on Vercel
```

They talk over the internet: frontend asks `backend/api/products/` for data
on every page view. You can develop, break, or redeploy either one without
touching the other.

## Local test (both on your PC)

Terminal 1 — backend:
```
cd polyghar-backend
python manage.py runserver
```
Terminal 2 — frontend:
```
cd polyghar-frontend
npm run dev
```
Open http://localhost:3000 — you should see the demo products.
Add a product at http://127.0.0.1:8000/admin, refresh the frontend — it's there.
That IS the integration. Deployment is the same idea with real URLs.

## Step 1 — put the backend online (PythonAnywhere, free)

1. Sign up at pythonanywhere.com → free Beginner account.
2. Zip `polyghar-backend`, upload via the **Files** tab, then in a
   **Bash console**:
   ```
   unzip polyghar-backend.zip && cd polyghar-backend
   pip3 install --user -r requirements.txt
   python3 manage.py migrate
   python3 manage.py createsuperuser
   python3 manage.py collectstatic --noinput
   ```
3. **Web** tab → Add a new web app → Manual configuration → newest Python.
4. Set **Source code** to `/home/YOURNAME/polyghar-backend`, then edit the
   **WSGI configuration file** — replace everything with:
   ```python
   import os, sys
   sys.path.insert(0, "/home/YOURNAME/polyghar-backend")
   os.environ["DJANGO_SETTINGS_MODULE"] = "polyghar.settings"
   os.environ["DJANGO_DEBUG"] = "0"
   os.environ["DJANGO_SECRET_KEY"] = "type-a-long-random-sentence-here"
   os.environ["DJANGO_ALLOWED_HOST"] = "YOURNAME.pythonanywhere.com"
   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```
5. Still on the Web tab, add **Static files** mappings:
   | URL | Directory |
   |----|----|
   | `/static/` | `/home/YOURNAME/polyghar-backend/staticfiles` |
   | `/media/` | `/home/YOURNAME/polyghar-backend/media` |
6. Click **Reload**. Test: `https://YOURNAME.pythonanywhere.com/api/health/`
   should show `{"status": "ok"}`. Your admin is at `/admin`.

## Step 2 — put the frontend online (Vercel, free)

1. Put `polyghar-frontend` on GitHub (its own repo).
2. vercel.com → sign in with GitHub → Add New → Project → pick the repo.
3. Before deploying, open **Environment Variables** and add:
   - Name: `NEXT_PUBLIC_API_URL`
   - Value: `https://YOURNAME.pythonanywhere.com`
4. Deploy. You get a URL like `https://polyghar.vercel.app`.

## Step 3 — close the loop

1. In `polyghar-frontend/config/site.js`, set `siteUrl` to your real Vercel
   URL (so WhatsApp messages link to the right product pages). Push the
   change — Vercel redeploys itself.
2. In your backend admin → Site settings, set your real WhatsApp number.

Done. Daily life from now on: open `YOURNAME.pythonanywhere.com/admin`
on any device, add/edit products, done. The Vercel site shows changes on
the next page load. You never redeploy anything for product updates.

## Two maintenance notes

- **PythonAnywhere free tier:** log in about once a month and click
  Reload/extend on the Web tab, or the backend gets paused.
- **Backups:** everything you enter lives in the backend —
  `db.sqlite3` + `media/`. Download those two now and then.
