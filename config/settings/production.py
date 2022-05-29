from config.settings.base import *
from corsheaders.defaults import default_headers

SECRET_KEY = env("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = [
    '.sayches-load-balancer-271777887.eu-west-2.elb.amazonaws.com', # ELB DNS
    '.10.0.0.54', # VPC IP Address
    '.35.178.121.64', # Elastic IP of the EC2
    '.sayches.com',
    'sayches-static.s3.amazonaws.com', # S3 Bucket
    ".d7cwfqpm9607r.cloudfront.net", # CloudFront
    ]


CORS_ORIGIN_ALLOW_ALL = False

CORS_ALLOW_HEADERS = default_headers + (
    'Access-Control-Allow-Origin',
)
CORS_ORIGIN_WHITELIST = [
    'https://sayches-load-balancer-271777887.eu-west-2.elb.amazonaws.com', # ELB DNS
    'http://10.0.0.54', # VPC IP Address
    'http://35.178.121.64', # Elastic IP of the EC2
    'https://sayches.com',
    'http://sayches.com',
    'https://cdn.sayches.com',
    'http://cdn.sayches.com',
    'https://sayches-static.s3.amazonaws.com', # S3 Bucket
    "https://d7cwfqpm9607r.cloudfront.net", # CloudFront
]

DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.postgresql_psycopg2',
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST'),
        'PORT': env('POSTGRES_PORT'),
        }
    }

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_BROWSER_XSS_FILTER = True

USE_X_FORWARDED_HOST = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')

AWS_ACCESS_KEY_ID = env("DJANGO_AWS_ACCESS_KEY_ID")

AWS_SECRET_ACCESS_KEY = env("DJANGO_AWS_SECRET_ACCESS_KEY")

AWS_STORAGE_BUCKET_NAME = env("DJANGO_AWS_STORAGE_BUCKET_NAME")

AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": 'max-age=86400'
}

AWS_DEFAULT_ACL = env("AWS_DEFAULT_ACL")

AWS_S3_CUSTOM_DOMAIN = env("AWS_S3_CUSTOM_DOMAIN")

STATICFILES_LOCATION = 'static'

STATICFILES_STORAGE = 'config.storages.StaticStorage'

MEDIAFILES_LOCATION = 'media'

MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}/'

DEFAULT_FILE_STORAGE = 'config.storages.MediaStorage'

STATIC_ROOT = '/static/'

COMPRESS_ROOT = STATIC_ROOT

STATICFILES_STORAGE = 'config.storages.CachedS3Boto3Storage'

COMPRESS_STORAGE = STATICFILES_STORAGE

STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'

COMPRESS_URL = STATIC_URL

TEMPLATES[-1]["OPTIONS"]["loaders"] = [
    (
        "django.template.loaders.cached.Loader",
        [
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
        ],
    )
]

INSTALLED_APPS += [
    'gunicorn',
    'storages',
    'django.contrib.sitemaps'
    ]  

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
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
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": True,
        },
    },