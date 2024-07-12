from .base import *  # pylint: disable=W0401,W0614

DEBUG = False

ADMINS = [
    ('Joaquin M', 'jmartinacu2002@gmail.com'),
]

ALLOWED_HOSTS = ['*']

# SSL/TLS

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True
