"""
Django settings for the AgriCare project (Hamitech ACIDA platform).
"""

from pathlib import Path

import environ
from celery.schedules import crontab

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False),
    GIS_ENABLED=(bool, False),
)
environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("SECRET_KEY", default="django-insecure-change-me-in-.env")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])

GIS_ENABLED = env("GIS_ENABLED")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

if GIS_ENABLED:
    INSTALLED_APPS.append("django.contrib.gis")

INSTALLED_APPS += [
    "rest_framework",
    "rest_framework.authtoken",
    "django_filters",
    "corsheaders",
    "apps.accounts",
    "apps.farms",
    "apps.advisory",
    "apps.geodata",
    "apps.prediction",
    "apps.dashboard",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "agricare.urls"

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

WSGI_APPLICATION = "agricare.wsgi.application"

# Database
# Defaults to SQLite so the project runs with zero external setup.
# Set DATABASE_URL in .env to point at Postgres/PostGIS, e.g.:
#   DATABASE_URL=postgis://agricare:agricare@localhost:5432/agricare
DATABASES = {
    "default": env.db("DATABASE_URL", default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}")
}

AUTH_USER_MODEL = "accounts.User"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Kampala"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "dashboard:login"
LOGIN_REDIRECT_URL = "dashboard:home"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    "DEFAULT_PAGINATION_CLASS": "agricare.pagination.StandardPagination",
    "PAGE_SIZE": 25,
}

CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=["http://localhost:3000"])
# Flutter's web dev server picks a random port each run, so an exact-origin
# allowlist isn't practical in local dev; only ever enabled when DEBUG is on.
CORS_ALLOW_ALL_ORIGINS = DEBUG

# Celery
CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="redis://localhost:6379/0")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND", default="redis://localhost:6379/0")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE

CELERY_BEAT_SCHEDULE = {
    "ingest-chirps-rainfall-daily": {
        "task": "apps.geodata.tasks.ingest_chirps_rainfall",
        "schedule": crontab(hour=3, minute=0),
    },
    "ingest-ndvi-daily": {
        "task": "apps.geodata.tasks.ingest_ndvi",
        "schedule": crontab(hour=3, minute=30),
    },
    "generate-advisories-daily": {
        "task": "apps.advisory.tasks.generate_advisories",
        "schedule": crontab(hour=4, minute=0),
    },
}

# Google Earth Engine (CHIRPS rainfall, NDVI) - set in .env
EE_SERVICE_ACCOUNT_EMAIL = env("EE_SERVICE_ACCOUNT_EMAIL", default="")
EE_SERVICE_ACCOUNT_KEY_FILE = env("EE_SERVICE_ACCOUNT_KEY_FILE", default="")
EE_PROJECT_ID = env("EE_PROJECT_ID", default="")

# Africa's Talking (SMS/USSD) - set in .env
AFRICASTALKING_USERNAME = env("AFRICASTALKING_USERNAME", default="")
AFRICASTALKING_API_KEY = env("AFRICASTALKING_API_KEY", default="")

EMAIL_BACKEND = env("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")
