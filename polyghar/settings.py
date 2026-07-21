"""
Django settings for the PolyGhar store.
You normally never need to edit this file — site name, WhatsApp number
etc. are all changed in the admin panel (Site settings).
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# On PythonAnywhere you'll set these two via the WSGI file (see README).
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "dev-only-key-change-me-8f3k2j9d8s7a6f5g4h3j2k1l0",
)
DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"

ALLOWED_HOSTS = ["*"]  # fine for a small site; PythonAnywhere sits in front

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "shop",
]

MIDDLEWARE = [
    "shop.middleware.ApiCorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "polyghar.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "polyghar.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kathmandu"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Uploaded product photos live here
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ── Production security hardening ──
# These switch on automatically when DJANGO_DEBUG=0 (i.e. when deployed).
if not DEBUG:
    # PythonAnywhere terminates HTTPS in front of the app; this tells Django
    # to trust its forwarded-protocol header so CSRF/redirects work right.
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True            # force https
    SESSION_COOKIE_SECURE = True          # admin login cookie only over https
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SECURE_HSTS_SECONDS = 60 * 60 * 24 * 30   # browsers remember to use https
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
    SECURE_CONTENT_TYPE_NOSNIFF = True

# Lock the site to your real domain once deployed by setting
# DJANGO_ALLOWED_HOST in the WSGI file (see INTEGRATION.md).
_host = os.environ.get("DJANGO_ALLOWED_HOST")
if _host:
    ALLOWED_HOSTS = [_host]
    CSRF_TRUSTED_ORIGINS = [f"https://{_host}"]
