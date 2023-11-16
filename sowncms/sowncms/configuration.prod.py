import os

ALLOWED_HOSTS = ["*"]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": os.environ.get('REDIS_URL'),
    },
}

CSRF_TRUSTED_ORIGINS = ["http://suws.localhost:8000", "http://sown.localhost:8000"]

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

TIME_ZONE = "Europe/London"

WAGTAILADMIN_BASE_URL = "http://localhost:8000"
