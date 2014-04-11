# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Source'
        db.create_table('sources_source', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=4096, unique=True)),
            ('url', self.gf('sources.models.TextFieldSingleLine')(unique=True)),
            ('title', self.gf('sources.models.TextFieldSingleLine')(blank=True, null=True)),
            ('update_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('alive', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('sources', ['Source'])


    def backwards(self, orm):
        # Deleting model 'Source'
        db.delete_table('sources_source')


    models = {
        'sources.source': {
            'Meta': {'object_name': 'Source'},
            'alive': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '4096', 'unique': 'True'}),
            'title': ('sources.models.TextFieldSingleLine', [], {'blank': 'True', 'null': 'True'}),
            'update_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'url': ('sources.models.TextFieldSingleLine', [], {'unique': 'True'})
        }
    }

    complete_apps = ['sources']