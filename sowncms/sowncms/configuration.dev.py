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

OIDC_RP_CLIENT_ID = ''
OIDC_RP_CLIENT_SECRET = ''
