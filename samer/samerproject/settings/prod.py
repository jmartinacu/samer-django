from samer.samerproject.settings.base import *  # pylint: disable=W0401,W0614,E0611
from samer.utils import get_tuple_list_env

DEBUG = False

ADMINS = get_tuple_list_env(os.getenv('ADMINS'))

ALLOWED_HOSTS = ['*']

# SSL/TLS

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True
