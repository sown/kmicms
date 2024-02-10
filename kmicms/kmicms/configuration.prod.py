import os

ALLOWED_HOSTS = ["*"]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": os.environ.get("REDIS_URL"),
    },
}

CSRF_TRUSTED_ORIGINS = [
    "https://cms-staging.containers-1.sown.org.uk",
    "https://sown-staging.containers-1.sown.org.uk",
    "https://suws-staging.containers-1.sown.org.uk",
]

DATABASE = {
    "ENGINE": "django.db.backends.postgresql",
    "NAME": os.environ.get("SQL_DATABASE"),
    "USER": os.environ.get("SQL_USER"),
    "PASSWORD": os.environ.get("SQL_PASSWORD"),
    "HOST": os.environ.get("SQL_HOST"),
    "PORT": os.environ.get("SQL_PORT"),
}

EMAIL = {
    "BACKEND": "django.core.mail.backends.console.EmailBackend",
}

SECRET_KEY = os.environ.get("SECRET_KEY")

SSO_ENABLED = True
SSO_OIDC_CONFIGURATION_URL = os.environ.get("SSO_OIDC_CONFIGURATION_URL")
SSO_OIDC_CLIENT_ID = os.environ.get("SSO_OIDC_CLIENT_ID")
SSO_OIDC_CLIENT_SECRET = os.environ.get("SSO_OIDC_CLIENT_SECRET")
SSO_STAFF_GROUP_NAME = os.environ.get("SSO_STAFF_GROUP_NAME")
SSO_SUPERUSER_GROUP_NAME = os.environ.get("SSO_SUPERUSER_GROUP_NAME")

RECAPTCHA_PUBLIC_KEY = os.environ.get("RECAPTCHA_PUBLIC_KEY")
RECAPTCHA_PRIVATE_KEY = os.environ.get("RECAPTCHA_PRIVATE_KEY")

TIME_ZONE = "Europe/London"

WAGTAILADMIN_BASE_URL = "https://kmicms.containers-1.sown.org.uk"

NETBOX_GRAPHQL_ENDPOINT = "https://netbox.sown.org.uk/graphql/"
NETBOX_API_TOKEN = os.environ.get("NETBOX_API_TOKEN")
NETBOX_REQUEST_TIMEOUT = 0.5
NETBOX_CACHE_TTL = 300
