# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        orm.Parser.objects.create(name='Default Parser', slug='default')

    def backwards(self, orm):
        "Write your backwards methods here."
        orm.Parser.objects.get(slug='default').delete()

    models = {
        'parsers.parser': {
            'Meta': {'object_name': 'Parser', 'ordering': "('name',)"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('parsers.models.TextFieldSingleLine', [], {'unique': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '4096', 'unique': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['parsers']
    symmetrical = True
