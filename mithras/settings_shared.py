# Django settings for mithras project.
import os.path
from thraxilsettings.shared import common

app = 'mithras'
base = os.path.dirname(__file__)

locals().update(common(app=app, base=base))

ALLOWED_HOSTS += ['.thraxil.org', 'thraxil.org']  # noqa

MEDIA_ROOT = '/var/www/thraxil/uploads/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(os.path.dirname(__file__), "templates"),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

INSTALLED_APPS += [  # noqa
    'mithras.abraxas',
    'django.contrib.sitemaps',
    'expvar',
]

SERVER_EMAIL = 'moderation@thraxil.org'
