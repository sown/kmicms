import os
import platform

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
    from sowncms import configuration
except ImportError as e:  # pragma: nocover
    if getattr(e, "name") == "configuration":
        raise ImproperlyConfigured(
            "Configuration file is not present. Please define sowncms/sowncms/configuration.py per the documentation.",  # noqa: E501
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
    BASE_PATH = (
        BASE_PATH.strip("/") + "/"
    )  # Enforce trailing slash only  # pragma: nocover

DEBUG = getattr(configuration, "DEBUG", False)
EMAIL = getattr(configuration, "EMAIL", {})
LANGUAGE_CODE = getattr(configuration, "LANGUAGE_CODE", "en-us")
TIME_ZONE = getattr(configuration, "TIME_ZONE", "UTC")
WAGTAIL_SITE_NAME = getattr(configuration, "WAGTAIL_SITE_NAME", "SOWN")

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
    "core",
    "home",
    "search",
    "standard_page",
    "compressor",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
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

ROOT_URLCONF = "sowncms.urls"

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
            ],
        },
    },
]

WSGI_APPLICATION = "sowncms.wsgi.application"

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

USE_I18N = True

USE_L10N = True

USE_TZ = True


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
    }
}


WAGTAILADMIN_RICH_TEXT_EDITORS = {
    'all-but-headings': {
        'WIDGET': 'wagtail.admin.rich_text.DraftailRichTextArea',
        'OPTIONS': {
            'features': ['bold', 'italic', 'link', 'document-link', 'ol', 'ul', 'hr', 'code', 'superscript', 'subscript', 'strikethrough', 'blockquote', 'image', 'embed']
        }
    }
}