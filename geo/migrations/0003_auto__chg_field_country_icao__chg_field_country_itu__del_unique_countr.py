# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Country', fields ['fips']
        db.delete_unique(u'geo_country', ['fips'])

        # Removing unique constraint on 'Country', fields ['itu']
        db.delete_unique(u'geo_country', ['itu'])


        # Changing field 'Country.icao'
        db.alter_column(u'geo_country', 'icao', self.gf('django.db.models.fields.CharField')(null=True, max_length=255))

        # Changing field 'Country.itu'
        db.alter_column(u'geo_country', 'itu', self.gf('django.db.models.fields.CharField')(null=True, max_length=255))

        # Changing field 'Country.fips'
        db.alter_column(u'geo_country', 'fips', self.gf('django.db.models.fields.CharField')(null=True, max_length=255))

    def backwards(self, orm):

        # Changing field 'Country.icao'
        db.alter_column(u'geo_country', 'icao', self.gf('separatedvaluesfield.models.SeparatedValuesField')(null=True, max_length=255))

        # Changing field 'Country.itu'
        db.alter_column(u'geo_country', 'itu', self.gf('django.db.models.fields.CharField')(null=True, max_length=3, unique=True))
        # Adding unique constraint on 'Country', fields ['itu']
        db.create_unique(u'geo_country', ['itu'])


        # Changing field 'Country.fips'
        db.alter_column(u'geo_country', 'fips', self.gf('django.db.models.fields.CharField')(null=True, max_length=3, unique=True))
        # Adding unique constraint on 'Country', fields ['fips']
        db.create_unique(u'geo_country', ['fips'])


    models = {
        'geo.administrativearea': {
            'Meta': {'object_name': 'AdministrativeArea', 'ordering': "(u'_order',)", 'unique_together': "(('name', 'country', 'type'),)"},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Country']", 'related_name': "'areas'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'null': 'True', 'to': "orm['geo.AdministrativeArea']", 'related_name': "'areas'", 'default': 'None', 'blank': 'True'}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.AdministrativeAreaType']"}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'blank': 'True', 'unique': 'True', 'default': "''", 'max_length': '32'})
        },
        'geo.administrativeareatype': {
            'Meta': {'object_name': 'AdministrativeAreaType', 'ordering': "(u'_order',)", 'unique_together': "(('country', 'name'),)"},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Country']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'null': 'True', 'to': "orm['geo.AdministrativeAreaType']", 'related_name': "'children'", 'blank': 'True'}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'blank': 'True', 'unique': 'True', 'default': "''", 'max_length': '32'})
        },
        'geo.country': {
            'Meta': {'object_name': 'Country', 'ordering': "['name']"},
            'continent': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['geo.Currency']", 'blank': 'True'}),
            'expired': ('django.db.models.fields.DateField', [], {'null': 'True', 'default': 'None', 'blank': 'True'}),
            'fips': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '255', 'blank': 'True'}),
            'fullname': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100'}),
            'icao': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'db_index': 'True', 'unique': 'True'}),
            'iso_code3': ('django.db.models.fields.CharField', [], {'max_length': '3', 'db_index': 'True', 'unique': 'True'}),
            'iso_num': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            'itu': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '255', 'blank': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True', 'default': 'datetime.datetime.now'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '18', 'decimal_places': '12', 'blank': 'True'}),
            'lng': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '18', 'decimal_places': '12', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100'}),
            'nato3': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'unique': 'True', 'blank': 'True'}),
            'phone_prefix': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '20', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['geo.UNRegion']", 'default': 'None', 'blank': 'True'}),
            'timezone': ('timezone_field.fields.TimeZoneField', [], {'null': 'True', 'default': 'None', 'blank': 'True'}),
            'tld': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '5', 'blank': 'True'}),
            'undp': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'unique': 'True', 'blank': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'blank': 'True', 'unique': 'True', 'default': "''", 'max_length': '32'})
        },
        'geo.currency': {
            'Meta': {'object_name': 'Currency', 'ordering': "['iso_code']"},
            'decimals': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_code': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True', 'unique': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'numeric_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            'symbol': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '5', 'blank': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'blank': 'True', 'unique': 'True', 'default': "''", 'max_length': '32'})
        },
        'geo.location': {
            'Meta': {'object_name': 'Location', 'ordering': "(u'_order',)", 'unique_together': "(('area', 'name'),)"},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'acc': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'default': '0', 'blank': 'True'}),
            'area': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['geo.AdministrativeArea']", 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Country']"}),
            'description': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_administrative': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_capital': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '18', 'decimal_places': '12', 'blank': 'True'}),
            'lng': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '18', 'decimal_places': '12', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['geo.LocationType']", 'blank': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'blank': 'True', 'unique': 'True', 'default': "''", 'max_length': '32'})
        },
        'geo.locationtype': {
            'Meta': {'object_name': 'LocationType'},
            'description': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'blank': 'True', 'unique': 'True', 'default': "''", 'max_length': '32'})
        },
        'geo.unregion': {
            'Meta': {'object_name': 'UNRegion', 'ordering': "['name']"},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True', 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['geo']