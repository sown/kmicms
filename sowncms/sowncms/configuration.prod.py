import os

ALLOWED_HOSTS = ["*"]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": os.environ.get('REDIS_URL'),
    },
}

CSRF_TRUSTED_ORIGINS = ["https://suws-web.containers-1.sown.org.uk", "https://sown-web.containers-1.sown.org.uk"]

DATABASE = {
    "ENGINE": 'django.db.backends.postgresql',
    "NAME": os.environ.get('SQL_DATABASE'),
    "USER": os.environ.get('SQL_USER'),
    "PASSWORD": os.environ.get('SQL_PASSWORD'),
    "HOST": os.environ.get('SQL_HOST'),
    "PORT": os.environ.get('SQL_PORT'),
}

EMAIL = {
    "BACKEND": "django.core.mail.backends.console.EmailBackend",
}

SECRET_KEY = os.environ.get('SECRET_KEY')

OIDC_ENABLED = True
OIDC_RP_CLIENT_ID = os.environ.get('OIDC_RP_CLIENT_ID')
OIDC_RP_CLIENT_SECRET = os.environ.get('OIDC_RP_CLIENT_SECRET')

TIME_ZONE = "Europe/London"

WAGTAILADMIN_BASE_URL = "https://sown-web.containers-1.sown.org.uk"