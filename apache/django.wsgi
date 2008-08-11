import os, sys

sys.path.append('/var/www/thraxil/')
sys.path.append('/var/www/thraxil/mithras/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'mithras.settings_production'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
