from config.settings.base import *
from config.settings.base import env
from corsheaders.defaults import default_headers
import socket

SECRET_KEY = env('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = ['*']

DOMAINS_WHITELIST = ['*']

CORS_ORIGIN_ALLOW_ALL = False

CORS_ALLOW_HEADERS = default_headers + (
    'Access-Control-Allow-Origin',
)

CORS_ORIGIN_WHITELIST = ('http://0.0.0.0:8000',)

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    },
    "qr-code": {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'qr-code-cache',
        'TIMEOUT': 3600
    }
}

COMPRESS_STORAGE = 'compressor.storage.GzipCompressorFileStorage'

STATIC_ROOT = str(ROOT_DIR / "staticfiles")

STATIC_URL = "/static/"

STATICFILES_DIRS = [str(APPS_DIR / "static")]

MEDIA_ROOT = str(APPS_DIR / "media")

MEDIA_URL = "/media/"

EMAIL_BACKEND = env("DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")

DATABASES = {"default": env.db("DATABASE_URL")}

DATABASES["default"]["ATOMIC_REQUESTS"] = True

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}

INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]

if env("USE_DOCKER") == "yes":
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]

INSTALLED_APPS += [
    "debug_toolbar",
    "django.contrib.sitemaps",
    "django_extensions",
    ]

CELERY_TASK_EAGER_PROPAGATES = True

EMAIL_HOST = "localhost"

EMAIL_PORT = 1025
