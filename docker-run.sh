#!/bin/bash

cd /var/www/mithras/mithras/
python manage.py migrate --noinput --settings=mithras.settings_docker
python manage.py collectstatic --noinput --settings=mithras.settings_docker
python manage.py compress --settings=mithras.settings_docker
exec gunicorn --env \
  DJANGO_SETTINGS_MODULE=mithras.settings_docker \
  mithras.wsgi:application -b 0.0.0.0:8000 -w 3 \
  --access-logfile=- --error-logfile=-
