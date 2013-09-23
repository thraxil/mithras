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

# local_settings.py can be used to override environment-specific settings
# like database and email that differ between development and production.
try:
    from local_settings import *
except ImportError:
    pass
