# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    depends_on = (
        ("parsers", "0002_add_default_parser"),
    )

    def forwards(self, orm):
        # Adding model 'Feed'
        db.create_table('feeds_feed', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=4096, unique=True)),
            ('url', self.gf('feeds.models.TextFieldSingleLine')(unique=True)),
            ('title', self.gf('feeds.models.TextFieldSingleLine')(null=True, blank=True)),
            ('alive', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('parser', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['parsers.Parser'], blank=True, null=True)),
        ))
        db.send_create_signal('feeds', ['Feed'])


    def backwards(self, orm):
        # Deleting model 'Feed'
        db.delete_table('feeds_feed')


    models = {
        'feeds.feed': {
            'Meta': {'object_name': 'Feed'},
            'alive': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['parsers.Parser']", 'blank': 'True', 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '4096', 'unique': 'True'}),
            'title': ('feeds.models.TextFieldSingleLine', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'url': ('feeds.models.TextFieldSingleLine', [], {'unique': 'True'})
        },
        'parsers.parser': {
            'Meta': {'object_name': 'Parser', 'ordering': "('name',)"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('parsers.models.TextFieldSingleLine', [], {'unique': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '4096', 'unique': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'})
        }
    }

    complete_apps = ['feeds']