##############################################################
#  This file serves as a base configuration for development  #
#  only. It is not intended for production use.              #
##############################################################

ALLOWED_HOSTS = ["localhost"]

CSRF_TRUSTED_ORIGINS = ["http://localhost:8000"]

DATABASE = {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": "db.sqlite3",
}

SECRET_KEY = "django-insecure-rT1fjisdfhsdfsiof3fsdfjs9d0fwqe78(UO-X^FPe"  # noqa: S105

DEBUG = True

EMAIL = {
    "BACKEND": "django.core.mail.backends.console.EmailBackend",
}

WAGTAILADMIN_BASE_URL = "http://localhost:8000"

SSO_OIDC_CONFIGURATION_URL = ""
SSO_OIDC_CLIENT_ID = ""
SSO_OIDC_CLIENT_SECRET = ""

DISCORD_APP_CLIENT_ID = ""
DISCORD_APP_CLIENT_SECRET = ""

RECAPTCHA_PUBLIC_KEY = ""
RECAPTCHA_PRIVATE_KEY = ""

NETBOX_GRAPHQL_ENDPOINT = "https://netbox.example.com/graphql/"
NETBOX_API_TOKEN = "abc"  # noqa: S105
NETBOX_REQUEST_TIMEOUT = 0.5
NETBOX_CACHE_TTL = 300
