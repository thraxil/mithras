# flake8: noqa
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Users'
        db.create_table(u'users', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('fullname', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('bio', self.gf('django.db.models.fields.TextField')()),
            ('css', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('abraxas', ['Users'])

        # Adding model 'Tag'
        db.create_table('abraxas_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal('abraxas', ['Tag'])

        # Adding model 'Node'
        db.create_table(u'node', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('comments_allowed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['abraxas.Users'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=8)),
        ))
        db.send_create_signal('abraxas', ['Node'])

        # Adding M2M table for field tags on 'Node'
        db.create_table(u'node_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('node', models.ForeignKey(orm['abraxas.node'], null=False)),
            ('tag', models.ForeignKey(orm['abraxas.tag'], null=False))
        ))
        db.create_unique(u'node_tags', ['node_id', 'tag_id'])

        # Adding model 'MetaField'
        db.create_table(u'meta_field', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['abraxas.Node'])),
            ('field_value', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('field_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('abraxas', ['MetaField'])

        # Adding model 'Post'
        db.create_table(u'post', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['abraxas.Node'])),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('version', self.gf('django.db.models.fields.IntegerField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['abraxas.Users'])),
            ('format', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('abraxas', ['Post'])

        # Adding model 'Bookmark'
        db.create_table(u'bookmark', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['abraxas.Node'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('via_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('version', self.gf('django.db.models.fields.IntegerField')()),
            ('via_url', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['abraxas.Users'])),
            ('format', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('abraxas', ['Bookmark'])

        # Adding model 'Image'
        db.create_table(u'image', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['abraxas.Node'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('thumb_width', self.gf('django.db.models.fields.IntegerField')()),
            ('thumb_height', self.gf('django.db.models.fields.IntegerField')()),
            ('height', self.gf('django.db.models.fields.IntegerField')()),
            ('width', self.gf('django.db.models.fields.IntegerField')()),
            ('ext', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('version', self.gf('django.db.models.fields.IntegerField')()),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['abraxas.Users'])),
            ('format', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('abraxas', ['Image'])

        # Adding model 'Comment'
        db.create_table(u'comment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['abraxas.Node'])),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('author_email', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('author_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('author_url', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('reply_to', self.gf('django.db.models.fields.IntegerField')()),
            ('status', self.gf('django.db.models.fields.CharField')(default='pending', max_length=30)),
        ))
        db.send_create_signal('abraxas', ['Comment'])


    def backwards(self, orm):
        # Deleting model 'Users'
        db.delete_table(u'users')

        # Deleting model 'Tag'
        db.delete_table('abraxas_tag')

        # Deleting model 'Node'
        db.delete_table(u'node')

        # Removing M2M table for field tags on 'Node'
        db.delete_table('node_tags')

        # Deleting model 'MetaField'
        db.delete_table(u'meta_field')

        # Deleting model 'Post'
        db.delete_table(u'post')

        # Deleting model 'Bookmark'
        db.delete_table(u'bookmark')

        # Deleting model 'Image'
        db.delete_table(u'image')

        # Deleting model 'Comment'
        db.delete_table(u'comment')


    models = {
        'abraxas.bookmark': {
            'Meta': {'object_name': 'Bookmark', 'db_table': "u'bookmark'"},
            'description': ('django.db.models.fields.TextField', [], {}),
            'format': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['abraxas.Node']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['abraxas.Users']"}),
            'version': ('django.db.models.fields.IntegerField', [], {}),
            'via_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'via_url': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'abraxas.comment': {
            'Meta': {'object_name': 'Comment', 'db_table': "u'comment'"},
            'author_email': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'author_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'author_url': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['abraxas.Node']"}),
            'reply_to': ('django.db.models.fields.IntegerField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '30'})
        },
        'abraxas.image': {
            'Meta': {'object_name': 'Image', 'db_table': "u'image'"},
            'description': ('django.db.models.fields.TextField', [], {}),
            'ext': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'format': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'height': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['abraxas.Node']"}),
            'thumb_height': ('django.db.models.fields.IntegerField', [], {}),
            'thumb_width': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['abraxas.Users']"}),
            'version': ('django.db.models.fields.IntegerField', [], {}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        },
        'abraxas.metafield': {
            'Meta': {'object_name': 'MetaField', 'db_table': "u'meta_field'"},
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'field_value': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['abraxas.Node']"})
        },
        'abraxas.node': {
            'Meta': {'object_name': 'Node', 'db_table': "u'node'"},
            'comments_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['abraxas.Tag']", 'symmetrical': 'False', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['abraxas.Users']"})
        },
        'abraxas.post': {
            'Meta': {'object_name': 'Post', 'db_table': "u'post'"},
            'body': ('django.db.models.fields.TextField', [], {}),
            'format': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['abraxas.Node']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['abraxas.Users']"}),
            'version': ('django.db.models.fields.IntegerField', [], {})
        },
        'abraxas.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'abraxas.users': {
            'Meta': {'object_name': 'Users', 'db_table': "u'users'"},
            'bio': ('django.db.models.fields.TextField', [], {}),
            'css': ('django.db.models.fields.TextField', [], {}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'fullname': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        }
    }

    complete_apps = ['abraxas']
