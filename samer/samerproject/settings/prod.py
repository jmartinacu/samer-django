from samer.samerproject.settings.base import *  # noqa
from samer.utils import get_tuple_list_env

DEBUG = False

ADMINS = get_tuple_list_env(os.getenv("ADMINS"))  # noqa

ALLOWED_HOSTS = ["*"]

SECRET_KEY = os.getenv(  # noqa
    "SECRET_KEY",
    "django-insecure-lifiv!v&qwh$j*5$0cz#iizeesc7vf(y$eofl5u!y-82sb(^6n",
)

# SSL/TLS

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

CSRF_TRUSTED_ORIGINS = ["https://samervalme.duckdns.org"]

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True
