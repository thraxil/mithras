# Django settings for mithras project.
import sys
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ()

MANAGERS = ADMINS
ALLOWED_HOSTS = ['localhost', 'thraxil.org']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mithras',
        'HOST': '',
        'PORT': 5432,
        'USER': '',
        'PASSWORD': '',
    }
}

if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
            'HOST': '',
            'PORT': '',
            'USER': '',
            'PASSWORD': '', }}

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=mithras',
]

LOGIN_URL = "/login/"

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
STATIC_URL = '/media/'
STATIC_ROOT = ""
STATICFILES_DIRS = (
    os.path.join(os.path.dirname(__file__), "../media"),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '@0zqwb3^sy2a7mo)en36plqr9hx)hh60&tqkzo+p*vwn06r6vn'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
)

MIDDLEWARE_CLASSES = (
    'django_statsd.middleware.GraphiteRequestTimingMiddleware',
    'django_statsd.middleware.GraphiteMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'mithras.urls'

TEMPLATE_DIRS = (
    "/home/anders/code/python/mithras/mithras/abraxas/templates",
)

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mithras.abraxas',
    'django_nose',
    'django.contrib.sitemaps',
    'django_statsd',
    'django_markwhat',
    'gunicorn',
]

EMAIL_SUBJECT_PREFIX = '[thraxil] '
EMAIL_HOST = 'localhost'
SERVER_EMAIL = 'moderation@thraxil.org'

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_COOKIE_HTTPONLY = True

STATSD_CLIENT = 'statsd.client'
STATSD_PREFIX = 'mithras'
STATSD_HOST = '127.0.0.1'
STATSD_PORT = 8125

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'django.security.DisallowedHost': {
        'handlers': ['null'],
        'propagate': False,
    },
}
