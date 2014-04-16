# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    depends_on = (
        ("feeds", "0001_initial"),
    )

    def forwards(self, orm):
        # Adding model 'Plenarprotokoll'
        db.create_table('bundestag_plenarprotokoll', (
            ('feed_ptr', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, primary_key=True, to=orm['feeds.Feed'])),
        ))
        db.send_create_signal('bundestag', ['Plenarprotokoll'])


    def backwards(self, orm):
        # Deleting model 'Plenarprotokoll'
        db.delete_table('bundestag_plenarprotokoll')


    models = {
        'bundestag.plenarprotokoll': {
            'Meta': {'object_name': 'Plenarprotokoll', '_ormbases': ['feeds.Feed']},
            'feed_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'primary_key': 'True', 'to': "orm['feeds.Feed']"})
        },
        'feeds.feed': {
            'Meta': {'object_name': 'Feed', '_ormbases': ['sources.Source']},
            'source_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'primary_key': 'True', 'to': "orm['sources.Source']"})
        },
        'sources.source': {
            'Meta': {'object_name': 'Source'},
            'alive': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '4096', 'unique': 'True'}),
            'title': ('sources.models.TextFieldSingleLine', [], {'null': 'True', 'blank': 'True'}),
            'update_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('sources.models.TextFieldSingleLine', [], {'unique': 'True'})
        }
    }

    complete_apps = ['bundestag']