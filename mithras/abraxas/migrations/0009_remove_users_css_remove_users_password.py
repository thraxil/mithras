# Generated by Django 4.1.6 on 2023-02-12 13:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('abraxas', '0008_auto_20171013_1004'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='css',
        ),
        migrations.RemoveField(
            model_name='users',
            name='password',
        ),
    ]
