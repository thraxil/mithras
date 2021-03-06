# flake8: noqa
from .settings_shared import *
from thraxilsettings.docker import common
import os.path
import os

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

HONEYCOMB_WRITEKEY = os.environ.get('HONEYCOMB_WRITEKEY')
HONEYCOMB_DATASET = os.environ.get('HONEYCOMB_DATASET')
