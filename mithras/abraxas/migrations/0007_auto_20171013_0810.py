# flake8: noqa
# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-13 08:10
from __future__ import unicode_literals

from django.db import migrations


def convert_to_markdown(apps, schema_editor):
    try:
        import textile
    except ImportError:
        return
        
    Bookmark = apps.get_model('abraxas', 'Bookmark')
    for bm in Bookmark.objects.filter(format='textile'):
        bm.description = textile.textile(bm.description).strip()
        bm.format = 'markdown'
        bm.save()
        print("bookmark", bm.id)

    Image = apps.get_model('abraxas', 'Image')
    for im in Image.objects.filter(format='textile'):
        im.description = textile.textile(im.description).strip()
        im.format = 'markdown'
        im.save()
        print("image", im.id)


class Migration(migrations.Migration):
    dependencies = [
        ('abraxas', '0006_auto_20171013_0805'),
    ]

    operations = [
        migrations.RunPython(convert_to_markdown)
    ]
