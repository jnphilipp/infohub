# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    depends_on = (
        ("sources", "0001_initial"),
    )

    def forwards(self, orm):
        # Adding model 'Feed'
        db.create_table('feeds_feed', (
            ('source_ptr', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['sources.Source'], primary_key=True)),
        ))
        db.send_create_signal('feeds', ['Feed'])


    def backwards(self, orm):
        # Deleting model 'Feed'
        db.delete_table('feeds_feed')


    models = {
        'feeds.feed': {
            'Meta': {'object_name': 'Feed', '_ormbases': ['sources.Source']},
            'source_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['sources.Source']", 'primary_key': 'True'})
        },
        'sources.source': {
            'Meta': {'object_name': 'Source'},
            'alive': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '4096'}),
            'title': ('sources.models.TextFieldSingleLine', [], {'null': 'True', 'blank': 'True'}),
            'update_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('sources.models.TextFieldSingleLine', [], {'unique': 'True'})
        }
    }

    complete_apps = ['feeds']