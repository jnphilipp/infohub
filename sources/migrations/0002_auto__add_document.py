# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Document'
        db.create_table('sources_document', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=4096)),
            ('url', self.gf('sources.models.TextFieldSingleLine')(unique=True)),
            ('meta', self.gf('django.db.models.fields.TextField')()),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sources.Source'])),
        ))
        db.send_create_signal('sources', ['Document'])


    def backwards(self, orm):
        # Deleting model 'Document'
        db.delete_table('sources_document')


    models = {
        'sources.document': {
            'Meta': {'object_name': 'Document'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta': ('django.db.models.fields.TextField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '4096'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sources.Source']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'url': ('sources.models.TextFieldSingleLine', [], {'unique': 'True'})
        },
        'sources.source': {
            'Meta': {'object_name': 'Source'},
            'alive': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '4096'}),
            'title': ('sources.models.TextFieldSingleLine', [], {'null': 'True', 'blank': 'True'}),
            'update_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'url': ('sources.models.TextFieldSingleLine', [], {'unique': 'True'})
        }
    }

    complete_apps = ['sources']