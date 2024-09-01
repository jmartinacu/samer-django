from samer.samerproject.settings.base import *  # noqa
from samer.utils import get_tuple_list_env

DEBUG = False

ADMINS = get_tuple_list_env(os.getenv("ADMINS"))  # noqa

ALLOWED_HOSTS = ["*"]

# SSL/TLS

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True
