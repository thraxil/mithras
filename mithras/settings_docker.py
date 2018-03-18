# flake8: noqa
from .settings_shared import *
from thraxilsettings.docker import common
import os.path
import os
import raven

app = 'mithras'
base = os.path.dirname(__file__)

locals().update(
    common(
        app=app,
        base=base,
        celery=False,
        INSTALLED_APPS=INSTALLED_APPS,
        STATIC_ROOT=STATIC_ROOT,
        MIDDLEWARE=MIDDLEWARE,
    ))

RAVEN_DSN = os.environ.get('RAVEN_DSN', None)

if RAVEN_DSN:
    RAVEN_CONFIG = {
        'dsn': RAVEN_DSN,
        # If you are using git, you can also automatically configure the
        # release based on the git info.
        'release': raven.fetch_git_sha(os.path.abspath(os.pardir)),
    }
