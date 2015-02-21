# flake8: noqa
from settings_shared import *

TEMPLATE_DIRS = (
    "/var/www/thraxil/mithras/mithras/abraxas/templates",
    "/var/www/thraxil/mithras/ve/django/contrib/sitemaps/templates"
)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
}

ALLOWED_HOSTS = ['localhost', 'thraxil.org']

STATIC_ROOT = os.path.join(os.path.dirname(__file__), "../media")
STATICFILES_DIRS = ()
COMPRESS_ENABLED = True

if 'migrate' not in sys.argv:
    INSTALLED_APPS = INSTALLED_APPS + [
        'raven.contrib.django.raven_compat',
    ]

# local_settings.py can be used to override environment-specific settings
# like database and email that differ between development and production.
try:
    from local_settings import *
except ImportError:
    pass
