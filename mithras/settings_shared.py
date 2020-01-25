# Django settings for mithras project.
import os.path
from thraxilsettings.shared import common

app = 'mithras'
base = os.path.dirname(__file__)

locals().update(common(app=app, base=base))

ALLOWED_HOSTS += ['.thraxil.org', 'thraxil.org', '127.0.0.1']  # noqa

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
    'expvarcmdline',
    'expvarpsutil',
    'bootstrap3',

    'django_otp',
    'django_otp.plugins.otp_static',
    'django_otp.plugins.otp_totp',
    'two_factor',
    'otp_yubikey',
]

MIDDLEWARE += [ # noqa
    'django.contrib.messages.middleware.MessageMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'beeline.middleware.django.HoneyMiddleware',
]

SERVER_EMAIL = 'moderation@thraxil.org'
USE_TZ = False

LOGIN_URL = 'two_factor:login'

# this one is optional
LOGIN_REDIRECT_URL = 'two_factor:profile'

SECURE_BROWSER_XSS_FILTER = True

# default off
HONEYCOMB_WRITEKEY = None
HONEYCOMB_DATASET = None
