import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "home",
    "users",
    "posts",
    "root",
    "questions",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "samer.middleware.auth_middleware.RootMiddleware",
]

ROOT_URLCONF = "samerproject.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "users.context_processors.user_auth",
            ],
        },
    },
]


WSGI_APPLICATION = "samerproject.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {"default": {}}

# MongoDB

CONNECTION_STRING = os.getenv("CONNECTION_STRING", "")

DB_NAME = os.getenv("DB_NAME", "")


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",  # noqa
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",  # noqa
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",  # noqa
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Madrid"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# AWS S3

AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME", "")

AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "")

# CELERY

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")

CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")

CELERY_ACCEPT_CONTENT = ["json"]

CELERY_TASK_SERIALIZER = "json"

CELERY_RESULT_SERIALIZER = "json"

CELERY_TIMEZONE = "UTC"

# AUTH USER

AUTHUSER_SESSION_ID = "userauth"

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

# MONGO MODELS

AUTH_ACTION_MODELS = [
    "User",
    "Post",
    "Tag",
    "Question",
]

AUTH_INCLUDE_PATHS = [
    {
        "name": "posts:add_posts_tag",
        "type": "dynamic",
        "args": ["66dd91747f069f8dd89be45a"],
    },
    {
        "name": "questions:create_answer",
        "type": "dynamic",
        "args": ["66dd91747f069f8dd89be45a", "dummy_edit"],
    },
    {
        "name": "questions:delete_root",
        "type": "dynamic",
        "args": ["66dd91747f069f8dd89be45a"],
    },
    {
        "name": "questions:toxic",
        "type": "dynamic",
        "args": ["66dd91747f069f8dd89be45a"],
    },
    {
        "name": "posts:search_posts",
        "type": "static",
    },
    {
        "name": "questions:archive",
        "type": "static",
    },
    {
        "name": "home:home_edit_profile",
        "type": "static",
    },
]
