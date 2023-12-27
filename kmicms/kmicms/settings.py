import os
import platform

from django.contrib.messages import constants as messages
from django.core.exceptions import ImproperlyConfigured
from pkg_resources import parse_version

#
# Environment setup
#

# Set the base directory two levels up
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

# Validate Python version
if parse_version(platform.python_version()) < parse_version("3.9.0"):  # pragma: nocover
    raise RuntimeError(
        f"SOWN CMS requires Python 3.9 or higher (current: Python {platform.python_version()})",
    )

#
# Configuration import
#

# Import configuration parameters
try:
    from kmicms import configuration
except ImportError as e:  # pragma: nocover
    if getattr(e, "name") == "configuration":
        raise ImproperlyConfigured(
            "Configuration file is not present. Please define kmicms/kmicms/configuration.py per the documentation.",  # noqa: E501
        ) from None
    raise

# Enforce required configuration parameters
for parameter in ["ALLOWED_HOSTS", "DATABASE", "SECRET_KEY"]:
    if not hasattr(configuration, parameter):
        raise ImproperlyConfigured(  # pragma: nocover
            f"Required parameter {parameter} is missing from configuration.py.",
        )

# Set required parameters
ALLOWED_HOSTS = getattr(configuration, "ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS = getattr(configuration, "CSRF_TRUSTED_ORIGINS")
DATABASE = getattr(configuration, "DATABASE")
SECRET_KEY = getattr(configuration, "SECRET_KEY")
WAGTAILADMIN_BASE_URL = getattr(configuration, "WAGTAILADMIN_BASE_URL")

# Set optional parameters
ADMINS = getattr(configuration, "ADMINS", [])

BASE_PATH = getattr(configuration, "BASE_PATH", "")
if BASE_PATH:
    BASE_PATH = BASE_PATH.strip("/") + "/"  # Enforce trailing slash only  # pragma: nocover

DEBUG = getattr(configuration, "DEBUG", False)
EMAIL = getattr(configuration, "EMAIL", {})
LANGUAGE_CODE = getattr(configuration, "LANGUAGE_CODE", "en-us")
TIME_ZONE = getattr(configuration, "TIME_ZONE", "UTC")
WAGTAIL_SITE_NAME = getattr(configuration, "WAGTAIL_SITE_NAME", "KMI.CMS")


if hasattr(configuration, "CACHES"):
    CACHES = getattr(configuration, "CACHES")

#
# Database
#

DATABASES = {"default": DATABASE}

#
# Email
#

EMAIL_BACKEND = EMAIL.get("BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = EMAIL.get("SERVER")
EMAIL_HOST_USER = EMAIL.get("USERNAME")
EMAIL_HOST_PASSWORD = EMAIL.get("PASSWORD")
EMAIL_PORT = EMAIL.get("PORT", 25)
EMAIL_SSL_CERTFILE = EMAIL.get("SSL_CERTFILE")
EMAIL_SSL_KEYFILE = EMAIL.get("SSL_KEYFILE")
EMAIL_SUBJECT_PREFIX = EMAIL.get("SUBJECT_PREFIX", "[SOWN CMS] ")
EMAIL_USE_SSL = EMAIL.get("USE_SSL", False)
EMAIL_USE_TLS = EMAIL.get("USE_TLS", False)
EMAIL_TIMEOUT = EMAIL.get("TIMEOUT", 10)
SERVER_EMAIL = EMAIL.get("FROM_EMAIL")

INSTALLED_APPS = [
    "accounts",
    "core",
    "pages.contact",
    "pages.home",
    "pages.infra",
    "pages.standard_page",
    # 3rd party
    "compressor",
    "django_recaptcha",
    "crispy_forms",
    "crispy_bootstrap5",
    # Wagtail / Django
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.contrib.routable_page",
    "wagtail.contrib.settings",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "modelcluster",
    "taggit",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sitemaps",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

if DEBUG:
    INSTALLED_APPS.extend(["debug_toolbar", "wagtail.contrib.styleguide"])
    MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE

    INTERNAL_IPS = ["127.0.0.1"]

ROOT_URLCONF = "kmicms.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PROJECT_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",
            ],
        },
    },
]

WSGI_APPLICATION = "kmicms.wsgi.application"

AUTH_USER_MODEL = "accounts.User"
WAGTAILIMAGES_IMAGE_MODEL = "core.CustomImage"

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# SSO configuration

USE_CONVENTIONAL_AUTH = not getattr(configuration, "SSO_ENABLED", False)

SSO_OIDC_CONFIGURATION_URL = getattr(configuration, "SSO_OIDC_CONFIGURATION_URL")
SSO_OIDC_CLIENT_ID = getattr(configuration, "SSO_OIDC_CLIENT_ID")
SSO_OIDC_CLIENT_SECRET = getattr(configuration, "SSO_OIDC_CLIENT_SECRET")
SSO_OIDC_SCOPES = "openid email profile"

SSO_STAFF_GROUP_NAME = getattr(configuration, "SSO_STAFF_GROUP_NAME", "kmicms:staff")
SSO_SUPERUSER_GROUP_NAME = getattr(configuration, "SSO_SUPERUSER_GROUP_NAME", "kmicms:superuser")

SSO_USER_SETTINGS_URL = "https://sso.sown.org.uk/if/user/#/settings"

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# https://docs.wagtail.org/en/v5.2.1/reference/settings.html#wagtail-password-management-enabled
# Don't let users change or reset their password
WAGTAIL_PASSWORD_MANAGEMENT_ENABLED = False
WAGTAIL_PASSWORD_RESET_ENABLED = False

# Don't require a password when creating a user,
# and blank password means cannot log in unless SSO
WAGTAILUSERS_PASSWORD_ENABLED = False

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Discord Integration
DISCORD_APP_CLIENT_ID = getattr(configuration, "DISCORD_APP_CLIENT_ID")
DISCORD_APP_CLIENT_SECRET = getattr(configuration, "DISCORD_APP_CLIENT_SECRET")
DISCORD_ACCESS_TOKEN_URL = "https://discordapp.com/api/oauth2/token"  # noqa: S105
DISCORD_AUTHORIZE_URL = "https://discordapp.com/api/oauth2/authorize"
DISCORD_REVOCATION_URL = "https://discord.com/api/oauth2/token/revoke"
DISCORD_USERINFO_ENDPOINT = "https://discordapp.com/api/users/@me"
DISCORD_CLIENT_KWARGS = {
    "token_endpoint_auth_method": "client_secret_post",
    "scope": "identify",
}


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

USE_I18N = True

USE_L10N = True

USE_TZ = True

MESSAGE_TAGS = {
    messages.DEBUG: "alert-info",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, "static"),
]

COMPRESS_PRECOMPILERS = (("text/x-scss", "django_libsass.SassCompiler"),)

# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# JavaScript / CSS assets being served from cache (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/4.2/ref/contrib/staticfiles/#manifeststaticfilesstorage
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"


# Wagtail settings

# Search
# https://docs.wagtail.org/en/stable/topics/search/backends.html
WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
    },
}


WAGTAILADMIN_RICH_TEXT_EDITORS = {
    "all-but-headings": {
        "WIDGET": "wagtail.admin.rich_text.DraftailRichTextArea",
        "OPTIONS": {
            "features": [
                "bold",
                "italic",
                "link",
                "document-link",
                "ol",
                "ul",
                "hr",
                "code",
                "superscript",
                "subscript",
                "strikethrough",
                "blockquote",
                "image",
                "embed",
            ],
        },
    },
}

# Brand Settings
AVAILABLE_BRANDS = [("sown", "SOWN"), ("suws", "SUWS")]

# Crispy

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# ReCAPTCHA
RECAPTCHA_PUBLIC_KEY = getattr(configuration, "RECAPTCHA_PUBLIC_KEY", None)
RECAPTCHA_PRIVATE_KEY = getattr(configuration, "RECAPTCHA_PRIVATE_KEY", None)

# Netbox Integration
NETBOX_GRAPHQL_ENDPOINT = getattr(configuration, "NETBOX_GRAPHQL_ENDPOINT")
NETBOX_API_TOKEN = getattr(configuration, "NETBOX_API_TOKEN")
NETBOX_REQUEST_TIMEOUT = getattr(configuration, "NETBOX_REQUEST_TIMEOUT", 0.5)
NETBOX_CACHE_TTL = getattr(configuration, "NETBOX_CACHE_TTL", 300)
