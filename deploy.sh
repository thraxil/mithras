#!/bin/bash
#TODO: skip .pyc files
rsync -r --progress --verbose -p -E /home/anders/code/python/mithras thraxil.org:/var/www/thraxil/
ssh thraxil.org touch /var/www/thraxil/mithras/apache/django.wsgi
