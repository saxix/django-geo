# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'UNRegion.name'
        db.alter_column(u'geo_unregion', 'name', self.gf('django.db.models.fields.CharField')(max_length=100))

    def backwards(self, orm):

        # Changing field 'UNRegion.name'
        db.alter_column(u'geo_unregion', 'name', self.gf('django.db.models.fields.CharField')(max_length=50))

    models = {
        'geo.administrativearea': {
            'Meta': {'ordering': "(u'_order',)", 'unique_together': "(('name', 'country', 'type'),)", 'object_name': 'AdministrativeArea'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'code': ('django.db.models.fields.CharField', [], {'blank': 'True', 'db_index': 'True', 'null': 'True', 'max_length': '10'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Country']", 'related_name': "'areas'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'default': 'None', 'to': "orm['geo.AdministrativeArea']", 'null': 'True', 'related_name': "'areas'"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.AdministrativeAreaType']"}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'blank': 'True', 'unique': 'True', 'default': "''", 'max_length': '32'})
        },
        'geo.administrativeareatype': {
            'Meta': {'ordering': "(u'_order',)", 'unique_together': "(('country', 'name'),)", 'object_name': 'AdministrativeAreaType'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Country']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'to': "orm['geo.AdministrativeAreaType']", 'null': 'True', 'related_name': "'children'"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'blank': 'True', 'unique': 'True', 'default': "''", 'max_length': '32'})
        },
        'geo.country': {
            'Meta': {'ordering': "['name']", 'object_name': 'Country'},
            'continent': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['geo.Currency']", 'null': 'True'}),
            'expired': ('django.db.models.fields.DateField', [], {'blank': 'True', 'default': 'None', 'null': 'True'}),
            'fullname': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'db_index': 'True', 'max_length': '2'}),
            'iso_code3': ('django.db.models.fields.CharField', [], {'unique': 'True', 'db_index': 'True', 'max_length': '3'}),
            'iso_num': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True', 'auto_now': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'decimal_places': '12', 'blank': 'True', 'null': 'True'}),
            'lng': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'decimal_places': '12', 'blank': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100'}),
            'phone_prefix': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '20'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'default': 'None', 'to': "orm['geo.UNRegion']", 'null': 'True'}),
            'timezone': ('timezone_field.fields.TimeZoneField', [], {'blank': 'True', 'default': 'None', 'null': 'True'}),
            'tld': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '5'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'blank': 'True', 'unique': 'True', 'default': "''", 'max_length': '32'})
        },
        'geo.currency': {
            'Meta': {'ordering': "['iso_code']", 'object_name': 'Currency'},
            'decimals': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'db_index': 'True', 'max_length': '5'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'numeric_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            'symbol': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '5'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'blank': 'True', 'unique': 'True', 'default': "''", 'max_length': '32'})
        },
        'geo.location': {
            'Meta': {'ordering': "(u'_order',)", 'unique_together': "(('area', 'name'),)", 'object_name': 'Location'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'acc': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'default': '0', 'null': 'True'}),
            'area': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['geo.AdministrativeArea']", 'null': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Country']"}),
            'description': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_administrative': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_capital': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'decimal_places': '12', 'blank': 'True', 'null': 'True'}),
            'lng': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'decimal_places': '12', 'blank': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['geo.LocationType']", 'null': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'blank': 'True', 'unique': 'True', 'default': "''", 'max_length': '32'})
        },
        'geo.locationtype': {
            'Meta': {'object_name': 'LocationType'},
            'description': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'blank': 'True', 'unique': 'True', 'default': "''", 'max_length': '32'})
        },
        'geo.unregion': {
            'Meta': {'ordering': "['name']", 'object_name': 'UNRegion'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'db_index': 'True', 'max_length': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['geo']