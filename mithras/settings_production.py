# flake8: noqa
from .settings_shared import *
import os

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates"),
)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
}

ALLOWED_HOSTS = ['localhost', 'thraxil.org']

AWS_S3_CUSTOM_DOMAIN = "d3nbegyfleeamo.cloudfront.net"
AWS_IS_GZIPPED = True
MEDIA_ROOT = "/var/www/thraxil/uploads/"
AWS_STORAGE_BUCKET_NAME = "thraxil-mithras-static-prod"
AWS_PRELOAD_METADATA = True
S3_URL = 'https://%s/' % AWS_S3_CUSTOM_DOMAIN
STATIC_URL = 'https://%s/media/' % AWS_S3_CUSTOM_DOMAIN
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_URL = STATIC_URL
MEDIA_URL = S3_URL + '/media/'
DEFAULT_FILE_STORAGE = 'cacheds3storage.MediaRootS3BotoStorage'
STATICFILES_STORAGE = 'cacheds3storage.CompressorS3BotoStorage'
COMPRESS_STORAGE = 'cacheds3storage.CompressorS3BotoStorage'
AWS_QUERYSTRING_AUTH = False

if 'migrate' not in sys.argv:
    INSTALLED_APPS = INSTALLED_APPS + [
        'raven.contrib.django.raven_compat',
    ]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'mithras-unique-snowflake',
    }
}

# local_settings.py can be used to override environment-specific settings
# like database and email that differ between development and production.
try:
    from local_settings import *
except ImportError:
    pass
