# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Feed.parser'
        db.add_column('feeds_feed', 'parser',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['feeds.Parser'], default=orm.Parser.objects.get(slug='default').id),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Feed.parser'
        db.delete_column('feeds_feed', 'parser_id')


    models = {
        'feeds.document': {
            'Meta': {'ordering': "('-created_at',)", 'object_name': 'Document'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feeds.Feed']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta': ('django.db.models.fields.TextField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '4096', 'unique': 'True'}),
            'state': ('django_fsm.FSMField', [], {'default': "'new'", 'max_length': '50'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('feeds.models.TextFieldSingleLine', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'url': ('feeds.models.TextFieldSingleLine', [], {'unique': 'True'})
        },
        'feeds.feed': {
            'Meta': {'object_name': 'Feed'},
            'alive': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feeds.Parser']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '4096', 'unique': 'True'}),
            'title': ('feeds.models.TextFieldSingleLine', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'url': ('feeds.models.TextFieldSingleLine', [], {'unique': 'True'})
        },
        'feeds.parser': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Parser'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('feeds.models.TextFieldSingleLine', [], {'unique': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '4096', 'unique': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'})
        },
        'feeds.report': {
            'Meta': {'ordering': "('-created_at',)", 'object_name': 'Report'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '4096', 'unique': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'})
        }
    }

    complete_apps = ['feeds']