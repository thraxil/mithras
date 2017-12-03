# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField()),
                ('url', models.CharField(max_length=256)),
                ('via_name', models.CharField(max_length=256)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('version', models.IntegerField()),
                ('via_url', models.CharField(max_length=256)),
                ('format', models.CharField(max_length=256)),
            ],
            options={
                'db_table': 'bookmark',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('body', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('author_email', models.CharField(max_length=256)),
                ('author_name', models.CharField(max_length=256)),
                ('author_url', models.CharField(max_length=256)),
                ('reply_to', models.IntegerField()),
                ('status', models.CharField(default=b'pending', max_length=30, choices=[(b'pending', b'Pending Moderation'), (b'approved', b'Approved')])),
            ],
            options={
                'db_table': 'comment',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField()),
                ('thumb_width', models.IntegerField()),
                ('thumb_height', models.IntegerField()),
                ('height', models.IntegerField()),
                ('width', models.IntegerField()),
                ('ext', models.CharField(max_length=3)),
                ('version', models.IntegerField()),
                ('modified', models.DateTimeField(auto_now=True)),
                ('format', models.CharField(max_length=256)),
            ],
            options={
                'db_table': 'image',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MetaField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field_value', models.CharField(max_length=256)),
                ('field_name', models.CharField(max_length=256)),
            ],
            options={
                'db_table': 'meta_field',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.CharField(max_length=256)),
                ('status', models.CharField(max_length=7)),
                ('comments_allowed', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=256)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(max_length=8)),
            ],
            options={
                'db_table': 'node',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('body', models.TextField()),
                ('modified', models.DateTimeField(auto_now=True)),
                ('version', models.IntegerField()),
                ('format', models.CharField(max_length=256)),
                ('node', models.ForeignKey(to='abraxas.Node', on_delete=models.CASCADE)),
            ],
            options={
                'db_table': 'post',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('slug', models.SlugField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(unique=True, max_length=128)),
                ('email', models.CharField(max_length=256)),
                ('fullname', models.CharField(max_length=256)),
                ('password', models.CharField(max_length=256)),
                ('bio', models.TextField()),
                ('css', models.TextField()),
            ],
            options={
                'db_table': 'users',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(to='abraxas.Users', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='node',
            name='tags',
            field=models.ManyToManyField(to='abraxas.Tag', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='node',
            name='user',
            field=models.ForeignKey(to='abraxas.Users', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='metafield',
            name='node',
            field=models.ForeignKey(to='abraxas.Node', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='image',
            name='node',
            field=models.ForeignKey(to='abraxas.Node', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='image',
            name='user',
            field=models.ForeignKey(to='abraxas.Users', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='node',
            field=models.ForeignKey(to='abraxas.Node', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bookmark',
            name='node',
            field=models.ForeignKey(to='abraxas.Node', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bookmark',
            name='user',
            field=models.ForeignKey(to='abraxas.Users', on_delete=models.CASCADE),
            preserve_default=True,
        ),
    ]
