# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Location.iata'
        db.add_column(u'geo_location', 'iata',
                      self.gf('django.db.models.fields.CharField')(blank=True, max_length=255, null=True, db_index=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Location.iata'
        db.delete_column(u'geo_location', 'iata')


    models = {
        'geo.administrativearea': {
            'Meta': {'ordering': "(u'_order',)", 'unique_together': "(('name', 'country', 'type'),)", 'object_name': 'AdministrativeArea'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'code': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '10', 'null': 'True', 'db_index': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Country']", 'related_name': "'areas'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'to': "orm['geo.AdministrativeArea']", 'blank': 'True', 'default': 'None', 'related_name': "'areas'", 'null': 'True'}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.AdministrativeAreaType']"}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'blank': 'True', 'max_length': '32', 'default': "''", 'unique': 'True'})
        },
        'geo.administrativeareatype': {
            'Meta': {'ordering': "(u'_order',)", 'unique_together': "(('country', 'name'),)", 'object_name': 'AdministrativeAreaType'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Country']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'to': "orm['geo.AdministrativeAreaType']", 'blank': 'True', 'related_name': "'children'", 'null': 'True'}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'blank': 'True', 'max_length': '32', 'default': "''", 'unique': 'True'})
        },
        'geo.country': {
            'Meta': {'ordering': "['name']", 'object_name': 'Country'},
            'continent': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Currency']", 'blank': 'True', 'null': 'True'}),
            'expired': ('django.db.models.fields.DateField', [], {'blank': 'True', 'default': 'None', 'null': 'True'}),
            'fips': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'null': 'True'}),
            'fullname': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'icao': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'db_index': 'True', 'unique': 'True'}),
            'iso_code3': ('django.db.models.fields.CharField', [], {'max_length': '3', 'db_index': 'True', 'unique': 'True'}),
            'iso_num': ('django.db.models.fields.CharField', [], {'max_length': '3', 'unique': 'True'}),
            'itu': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'null': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'blank': 'True', 'decimal_places': '12', 'null': 'True'}),
            'lng': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'blank': 'True', 'decimal_places': '12', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'nato3': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '3', 'null': 'True', 'unique': 'True'}),
            'phone_prefix': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '20', 'null': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.UNRegion']", 'blank': 'True', 'default': 'None', 'null': 'True'}),
            'timezone': ('timezone_field.fields.TimeZoneField', [], {'blank': 'True', 'default': 'None', 'null': 'True'}),
            'tld': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '5', 'null': 'True'}),
            'undp': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '3', 'null': 'True', 'unique': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'blank': 'True', 'max_length': '32', 'default': "''", 'unique': 'True'})
        },
        'geo.currency': {
            'Meta': {'ordering': "['iso_code']", 'object_name': 'Currency'},
            'decimals': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_code': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True', 'unique': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'numeric_code': ('django.db.models.fields.CharField', [], {'max_length': '5', 'unique': 'True'}),
            'symbol': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '5', 'null': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'blank': 'True', 'max_length': '32', 'default': "''", 'unique': 'True'})
        },
        'geo.location': {
            'Meta': {'ordering': "(u'_order',)", 'unique_together': "(('area', 'name'),)", 'object_name': 'Location'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'acc': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'default': '0', 'null': 'True'}),
            'area': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.AdministrativeArea']", 'blank': 'True', 'null': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Country']"}),
            'description': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100', 'null': 'True'}),
            'flags': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'iata': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'null': 'True', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_administrative': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_capital': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'blank': 'True', 'decimal_places': '12', 'null': 'True'}),
            'lng': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'blank': 'True', 'decimal_places': '12', 'null': 'True'}),
            'loccode': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'null': 'True', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '2', 'null': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.LocationType']", 'blank': 'True', 'null': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'blank': 'True', 'max_length': '32', 'default': "''", 'unique': 'True'})
        },
        'geo.locationtype': {
            'Meta': {'object_name': 'LocationType'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'blank': 'True', 'max_length': '32', 'default': "''", 'unique': 'True'})
        },
        'geo.unregion': {
            'Meta': {'ordering': "['name']", 'object_name': 'UNRegion'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True', 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['geo']