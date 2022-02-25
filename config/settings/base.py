"""
Base settings to build other settings files upon.
"""
import os
from datetime import timedelta
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import gettext_lazy as _
from pathlib import Path
import environ
from six import python_2_unicode_compatible
import django.utils.encoding

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent

APPS_DIR = ROOT_DIR / "sayches"

env = environ.Env()

X_FRAME_OPTIONS = 'SAMEORIGIN'

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)

if READ_DOT_ENV_FILE:
    env.read_env(str(ROOT_DIR / ".env"))

DEBUG = env.bool("DEBUG", False)

TIME_ZONE = "UTC"

LANGUAGE_CODE = "en-us"

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [str(ROOT_DIR / "locale")]

STATICFILES_DIRS = [str(APPS_DIR / "static")]

if USE_TZ:
    CELERY_TIMEZONE = TIME_ZONE

CELERY_BROKER_URL = env("CELERY_BROKER_URL")

CELERY_RESULT_BACKEND = CELERY_BROKER_URL

CELERY_ACCEPT_CONTENT = ["json"]

CELERY_TASK_SERIALIZER = "json"

CELERY_RESULT_SERIALIZER = "json"

CELERY_TASK_TIME_LIMIT = 5 * 60

CELERY_TASK_SOFT_TIME_LIMIT = 60

CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,
        },
    }
}

CACHE_TTL = 60 * 15

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.admin",
    "django.forms",
    "django.contrib.postgres",
]

THIRD_PARTY_APPS = [
    "crispy_forms",
    "rest_framework",
    'rest_framework.authtoken',
    "widget_tweaks",
    "django_countries",
    'django_celery_beat',
    "celery",
    "qr_code",
    "django_otp",
    "django_otp.plugins.otp_totp",
    "taggit",
    "ckeditor_uploader",
    "compressor",
    "ckeditor",
]

LOCAL_APPS = [
    "users.apps.UserConfig",
    "sign.apps.SignConfig",
    "posts.apps.PostsConfig",
    "subsections.apps.SubsectionsConfig",
    "message.apps.MessagesConfig",
    "ads.apps.AdsConfig",
    "sudo.apps.SudoConfig",
    "api.apps.ApiConfig",
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIGRATION_MODULES = {"sites": "sayches.contrib.sites.migrations"}

AUTH_USER_MODEL = "users.User"

LOGIN_REDIRECT_URL = "subsections:home"

LOGIN_URL = "login"

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_otp.middleware.OTPMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "users.middleware.UpdateLastActivityMiddleware",
    'users.middleware.TimezoneMiddleware',
    "users.middleware.OneSessionPerUserMiddleware",
]

OTP_TOTP_ISSUER = 'Sayches'
 
SET_INTERVAL_ALLOW = 60 # IN MIN

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(APPS_DIR / "templates")],
        "OPTIONS": {
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "sayches.utils.context_processors.settings_context",
            ],
        },
    }
]
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

CRISPY_TEMPLATE_PACK = "bootstrap4"

FIXTURE_DIRS = (str(APPS_DIR / "fixtures"),)

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

COMPRESS_ENABLED = True

COMPRESS_CSS_FILTERS = ['compressor.filters.css_default.CssAbsoluteFilter', 'compressor.filters.cssmin.CSSMinFilter']

COMPRESS_JS_FILTERS = ['compressor.filters.jsmin.JSMinFilter']

SESSION_COOKIE_HTTPONLY = True

CSRF_COOKIE_HTTPONLY = True

SECURE_BROWSER_XSS_FILTER = True

X_FRAME_OPTIONS = "DENY"

EMAIL_TIMEOUT = 5

FRONTEND_URL = "sayches.com"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

DEFAULT_FROM_EMAIL = "info@sayches.com"

BASE_URL ="https://sayches.com"

ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)

ACCOUNT_AUTHENTICATION_METHOD = "username"

FRONTEND_HOST = BASE_URL

ACCOUNT_EMAIL_SUBJECT_PREFIX =("Sayches | ")

current_site = BASE_URL

ACCOUNT_FORMS = {"signup": "sayches.sign.forms.UserRegistrationForm",}

ACCOUNT_PRESERVE_USERNAME_CASING = False

QR_CODE_CACHE_ALIAS = 'qr-code'

APPEND_SLASH = False

django.utils.encoding.python_2_unicode_compatible = python_2_unicode_compatible

YOUR_HCAPTCHA_SECRET_KEY = env('YOUR_HCAPTCHA_SECRET_KEY')

VERIFY_URL = env('VERIFY_URL')

YOUR_HCAPTCHA_SITE_KEY = env('YOUR_HCAPTCHA_SITE_KEY')

REST_FRAMEWORK = {
'DEFAULT_PERMISSION_CLASSES': (
    'rest_framework.permissions.IsAdminUser',
    ),
}

COINBASE_EXCHANGE_RATES_API = 'https://api.coinbase.com/v2/exchange-rates?currency=BTC'

CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_ALLOW_NONIMAGE_FILES = False

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

SEND_EMAIL_PASSCODE = env('SEND_EMAIL_PASSCODE')

COUNTRIES_OVERRIDE = {
    'IL': None,
    'SA': ('Arabia'),
}

TOKEN_EXPIRATION_PERIOD = 360 # IN DAYS