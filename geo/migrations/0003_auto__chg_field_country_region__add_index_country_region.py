# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Renaming column for 'Country.region' to match new field type.
        db.rename_column(u'geo_country', 'region', 'region_id')
        # Changing field 'Country.region'
        db.alter_column(u'geo_country', 'region_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['geo.UNRegion']))
        # Adding index on 'Country', fields ['region']
        db.create_index(u'geo_country', ['region_id'])


    def backwards(self, orm):
        # Removing index on 'Country', fields ['region']
        db.delete_index(u'geo_country', ['region_id'])


        # Renaming column for 'Country.region' to match new field type.
        db.rename_column(u'geo_country', 'region_id', 'region')
        # Changing field 'Country.region'
        db.alter_column(u'geo_country', 'region', self.gf('django.db.models.fields.IntegerField')(null=True))

    models = {
        'geo.administrativearea': {
            'Meta': {'unique_together': "(('name', 'country', 'type'),)", 'ordering': "(u'_order',)", 'object_name': 'AdministrativeArea'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True', 'db_index': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Country']", 'related_name': "'areas'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'default': 'None', 'blank': 'True', 'null': 'True', 'to': "orm['geo.AdministrativeArea']", 'related_name': "'areas'"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.AdministrativeAreaType']"}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'max_length': '32', 'default': "''", 'blank': 'True', 'unique': 'True'})
        },
        'geo.administrativeareatype': {
            'Meta': {'unique_together': "(('country', 'name'),)", 'ordering': "(u'_order',)", 'object_name': 'AdministrativeAreaType'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Country']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['geo.AdministrativeAreaType']", 'related_name': "'children'"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'max_length': '32', 'default': "''", 'blank': 'True', 'unique': 'True'})
        },
        'geo.country': {
            'Meta': {'ordering': "['name']", 'object_name': 'Country'},
            'continent': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['geo.Currency']"}),
            'expired': ('django.db.models.fields.DateField', [], {'default': 'None', 'blank': 'True', 'null': 'True'}),
            'fullname': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'unique': 'True', 'db_index': 'True'}),
            'iso_code3': ('django.db.models.fields.CharField', [], {'max_length': '3', 'unique': 'True', 'db_index': 'True'}),
            'iso_num': ('django.db.models.fields.CharField', [], {'max_length': '3', 'unique': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True', 'auto_now': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'decimal_places': '12', 'blank': 'True', 'null': 'True', 'max_digits': '18'}),
            'lng': ('django.db.models.fields.DecimalField', [], {'decimal_places': '12', 'blank': 'True', 'null': 'True', 'max_digits': '18'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'phone_prefix': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True', 'null': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'blank': 'True', 'null': 'True', 'to': "orm['geo.UNRegion']"}),
            'timezone': ('timezone_field.fields.TimeZoneField', [], {'default': 'None', 'blank': 'True', 'null': 'True'}),
            'tld': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True', 'null': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'max_length': '32', 'default': "''", 'blank': 'True', 'unique': 'True'})
        },
        'geo.currency': {
            'Meta': {'ordering': "['iso_code']", 'object_name': 'Currency'},
            'decimals': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_code': ('django.db.models.fields.CharField', [], {'max_length': '5', 'unique': 'True', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'numeric_code': ('django.db.models.fields.CharField', [], {'max_length': '5', 'unique': 'True'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True', 'null': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'max_length': '32', 'default': "''", 'blank': 'True', 'unique': 'True'})
        },
        'geo.location': {
            'Meta': {'unique_together': "(('area', 'name'),)", 'ordering': "(u'_order',)", 'object_name': 'Location'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'acc': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True', 'null': 'True'}),
            'area': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['geo.AdministrativeArea']"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Country']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_administrative': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_capital': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'decimal_places': '12', 'blank': 'True', 'null': 'True', 'max_digits': '18'}),
            'lng': ('django.db.models.fields.DecimalField', [], {'decimal_places': '12', 'blank': 'True', 'null': 'True', 'max_digits': '18'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['geo.LocationType']"}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'max_length': '32', 'default': "''", 'blank': 'True', 'unique': 'True'})
        },
        'geo.locationtype': {
            'Meta': {'object_name': 'LocationType'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'max_length': '32', 'default': "''", 'blank': 'True', 'unique': 'True'})
        },
        'geo.unregion': {
            'Meta': {'ordering': "['name']", 'object_name': 'UNRegion'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '5', 'unique': 'True', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['geo']