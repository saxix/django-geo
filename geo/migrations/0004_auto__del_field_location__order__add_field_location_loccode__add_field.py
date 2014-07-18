# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Location', fields ['area', 'name']
        db.delete_unique(u'geo_location', ['area_id', 'name'])

        # Deleting field 'Location._order'
        db.delete_column(u'geo_location', '_order')

        # Adding field 'Location.loccode'
        db.add_column(u'geo_location', 'loccode',
                      self.gf('django.db.models.fields.CharField')(db_index=True, max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Location.flags'
        db.add_column(u'geo_location', 'flags',
                      self.gf('django.db.models.fields.BigIntegerField')(default=1),
                      keep_default=False)

        # Adding field 'Location.status'
        db.add_column(u'geo_location', 'status',
                      self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Location._order'
        db.add_column(u'geo_location', '_order',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'Location.loccode'
        db.delete_column(u'geo_location', 'loccode')

        # Deleting field 'Location.flags'
        db.delete_column(u'geo_location', 'flags')

        # Deleting field 'Location.status'
        db.delete_column(u'geo_location', 'status')

        # Adding unique constraint on 'Location', fields ['area', 'name']
        db.create_unique(u'geo_location', ['area_id', 'name'])


    models = {
        'geo.administrativearea': {
            'Meta': {'ordering': "(u'_order',)", 'unique_together': "(('name', 'country', 'type'),)", 'object_name': 'AdministrativeArea'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Country']", 'related_name': "'areas'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'default': 'None', 'to': "orm['geo.AdministrativeArea']", 'null': 'True', 'related_name': "'areas'", 'blank': 'True'}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.AdministrativeAreaType']"}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'default': "''", 'max_length': '32', 'unique': 'True', 'blank': 'True'})
        },
        'geo.administrativeareatype': {
            'Meta': {'ordering': "(u'_order',)", 'unique_together': "(('country', 'name'),)", 'object_name': 'AdministrativeAreaType'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Country']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'to': "orm['geo.AdministrativeAreaType']", 'null': 'True', 'related_name': "'children'", 'blank': 'True'}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'default': "''", 'max_length': '32', 'unique': 'True', 'blank': 'True'})
        },
        'geo.country': {
            'Meta': {'ordering': "['name']", 'object_name': 'Country'},
            'continent': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Currency']", 'null': 'True', 'blank': 'True'}),
            'expired': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'fips': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'fullname': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'icao': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'unique': 'True', 'db_index': 'True'}),
            'iso_code3': ('django.db.models.fields.CharField', [], {'max_length': '3', 'unique': 'True', 'db_index': 'True'}),
            'iso_num': ('django.db.models.fields.CharField', [], {'max_length': '3', 'unique': 'True'}),
            'itu': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'default': 'datetime.datetime.now', 'blank': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '18', 'decimal_places': '12', 'blank': 'True'}),
            'lng': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '18', 'decimal_places': '12', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'nato3': ('django.db.models.fields.CharField', [], {'max_length': '3', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'phone_prefix': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['geo.UNRegion']", 'null': 'True', 'blank': 'True'}),
            'timezone': ('timezone_field.fields.TimeZoneField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'tld': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'undp': ('django.db.models.fields.CharField', [], {'max_length': '3', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'default': "''", 'max_length': '32', 'unique': 'True', 'blank': 'True'})
        },
        'geo.currency': {
            'Meta': {'ordering': "['iso_code']", 'object_name': 'Currency'},
            'decimals': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_code': ('django.db.models.fields.CharField', [], {'max_length': '5', 'unique': 'True', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'numeric_code': ('django.db.models.fields.CharField', [], {'max_length': '5', 'unique': 'True'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'default': "''", 'max_length': '32', 'unique': 'True', 'blank': 'True'})
        },
        u'geo.location': {
            'Meta': {'object_name': 'Location'},
            'acc': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'area': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.AdministrativeArea']", 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Country']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'flags': ('django.db.models.fields.BigIntegerField', [], {'default': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_administrative': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_capital': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '18', 'decimal_places': '12', 'blank': 'True'}),
            'lng': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '18', 'decimal_places': '12', 'blank': 'True'}),
            'loccode': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.LocationType']", 'null': 'True', 'blank': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'default': "''", 'max_length': '32', 'unique': 'True', 'blank': 'True'})
        },
        'geo.locationtype': {
            'Meta': {'object_name': 'LocationType'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'default': "''", 'max_length': '32', 'unique': 'True', 'blank': 'True'})
        },
        'geo.unregion': {
            'Meta': {'ordering': "['name']", 'object_name': 'UNRegion'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '5', 'unique': 'True', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['geo']