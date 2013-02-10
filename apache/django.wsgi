import os, sys

site.addsitedir('/var/www/thraxil/mithras/ve/lib/python2.7/site-packages')
sys.path.append('/var/www/thraxil/')
sys.path.append('/var/www/thraxil/mithras/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'mithras.settings_production'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
