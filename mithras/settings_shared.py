# Django settings for mithras project.
import os.path
from thraxilsettings.shared import common
from opencensus.trace import config_integration

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

    'opencensus.ext.django',
]

MIDDLEWARE += [ # noqa
    'django.contrib.messages.middleware.MessageMiddleware',
    'opencensus.ext.django.middleware.OpencensusMiddleware',
]

OPENCENSUS_TRACE = {
    'SAMPLER': 'opencensus.trace.samplers.always_on.AlwaysOnSampler',
    'EXPORTER': 'opencensus.trace.exporters.print_exporter.PrintExporter',
    #    'PROPAGATOR':
    #    'opencensus.trace.propagation.google_cloud_format.'
    #    'GoogleCloudFormatPropagator',
}

OPENCENSUS_TRACE_PARAMS = {
    'SAMPLING_RATE': 0.5,
    'SERVICE_NAME': 'mithras',
}

integration = ['postgresql']

config_integration.trace_integrations(integration)

SERVER_EMAIL = 'moderation@thraxil.org'
USE_TZ = False
