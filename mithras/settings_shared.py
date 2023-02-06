# Django settings for mithras project.
import os.path

from thraxilsettings.shared import common

app = "mithras"
base = os.path.dirname(__file__)

locals().update(common(app=app, base=base))

ALLOWED_HOSTS += [  # noqa
    ".thraxil.org",
    "thraxil.org",
    "mithras.fly.dev",
    "127.0.0.1",
]  # noqa

MEDIA_ROOT = "/var/www/thraxil/uploads/"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(os.path.dirname(__file__), "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.request",
                "django.template.context_processors.debug",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

INSTALLED_APPS += [  # noqa
    "mithras.abraxas",
    "django.contrib.sitemaps",
    "expvar",
    "expvarcmdline",
    "expvarpsutil",
    "bootstrap3",
]

MIDDLEWARE += [  # noqa
    "django.contrib.messages.middleware.MessageMiddleware",
    "beeline.middleware.django.HoneyMiddleware",
]

SERVER_EMAIL = "moderation@thraxil.org"
USE_TZ = False

SECURE_BROWSER_XSS_FILTER = True

# default off
HONEYCOMB_WRITEKEY = None
HONEYCOMB_DATASET = None

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
