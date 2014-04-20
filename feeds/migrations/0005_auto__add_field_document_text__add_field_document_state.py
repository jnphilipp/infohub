# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Document.text'
        db.add_column('feeds_document', 'text',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Document.state'
        db.add_column('feeds_document', 'state',
                      self.gf('django_fsm.FSMField')(max_length=50, default='new'),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Document.text'
        db.delete_column('feeds_document', 'text')

        # Deleting field 'Document.state'
        db.delete_column('feeds_document', 'state')


    models = {
        'feeds.document': {
            'Meta': {'object_name': 'Document', 'ordering': "('-created_at',)"},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feeds.Feed']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta': ('django.db.models.fields.TextField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '4096', 'unique': 'True'}),
            'state': ('django_fsm.FSMField', [], {'max_length': '50', 'default': "'new'"}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('feeds.models.TextFieldSingleLine', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('feeds.models.TextFieldSingleLine', [], {'unique': 'True'})
        },
        'feeds.feed': {
            'Meta': {'object_name': 'Feed'},
            'alive': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '4096', 'unique': 'True'}),
            'title': ('feeds.models.TextFieldSingleLine', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('feeds.models.TextFieldSingleLine', [], {'unique': 'True'})
        },
        'feeds.report': {
            'Meta': {'object_name': 'Report', 'ordering': "('-created_at',)"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '4096', 'unique': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['feeds']