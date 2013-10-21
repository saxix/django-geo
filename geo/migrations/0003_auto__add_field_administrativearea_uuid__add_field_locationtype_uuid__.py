# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'AdministrativeArea.uuid'
        db.add_column(u'geo_administrativearea', 'uuid',
                      self.gf('uuidfield.fields.UUIDField')(default='', unique=True, max_length=32, blank=True),
                      keep_default=False)

        # Adding field 'LocationType.uuid'
        db.add_column(u'geo_locationtype', 'uuid',
                      self.gf('uuidfield.fields.UUIDField')(default='', unique=True, max_length=32, blank=True),
                      keep_default=False)

        # Adding field 'Currency.uuid'
        db.add_column(u'geo_currency', 'uuid',
                      self.gf('uuidfield.fields.UUIDField')(default='', unique=True, max_length=32, blank=True),
                      keep_default=False)

        # Adding field 'Country.uuid'
        db.add_column(u'geo_country', 'uuid',
                      self.gf('uuidfield.fields.UUIDField')(default='', unique=True, max_length=32, blank=True),
                      keep_default=False)

        # Adding field 'AdministrativeAreaType.uuid'
        db.add_column(u'geo_administrativeareatype', 'uuid',
                      self.gf('uuidfield.fields.UUIDField')(default='', unique=True, max_length=32, blank=True),
                      keep_default=False)

        # Adding field 'Location.uuid'
        db.add_column(u'geo_location', 'uuid',
                      self.gf('uuidfield.fields.UUIDField')(default='', unique=True, max_length=32, blank=True),
                      keep_default=False)

        # Adding unique constraint on 'Location', fields ['name', 'area']
        db.create_unique(u'geo_location', ['name', 'area_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Location', fields ['name', 'area']
        db.delete_unique(u'geo_location', ['name', 'area_id'])

        # Deleting field 'AdministrativeArea.uuid'
        db.delete_column(u'geo_administrativearea', 'uuid')

        # Deleting field 'LocationType.uuid'
        db.delete_column(u'geo_locationtype', 'uuid')

        # Deleting field 'Currency.uuid'
        db.delete_column(u'geo_currency', 'uuid')

        # Deleting field 'Country.uuid'
        db.delete_column(u'geo_country', 'uuid')

        # Deleting field 'AdministrativeAreaType.uuid'
        db.delete_column(u'geo_administrativeareatype', 'uuid')

        # Deleting field 'Location.uuid'
        db.delete_column(u'geo_location', 'uuid')


    models = {
        'geo.administrativearea': {
            'Meta': {'ordering': "(u'_order',)", 'unique_together': "(('name', 'country', 'type'),)", 'object_name': 'AdministrativeArea'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'areas'", 'to': "orm['geo.Country']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'areas'", 'null': 'True', 'to': "orm['geo.AdministrativeArea']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.AdministrativeAreaType']"}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'default': "''", 'unique': 'True', 'max_length': '32', 'blank': 'True'})
        },
        'geo.administrativeareatype': {
            'Meta': {'ordering': "(u'_order',)", 'unique_together': "(('country', 'name'),)", 'object_name': 'AdministrativeAreaType'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Country']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['geo.AdministrativeAreaType']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'default': "''", 'unique': 'True', 'max_length': '32', 'blank': 'True'})
        },
        'geo.country': {
            'Meta': {'ordering': "['name']", 'object_name': 'Country'},
            'continent': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Currency']", 'null': 'True', 'blank': 'True'}),
            'fullname': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso3_code': ('django.db.models.fields.CharField', [], {'default': 'None', 'unique': 'True', 'max_length': '3', 'db_index': 'True'}),
            'iso_code': ('django.db.models.fields.CharField', [], {'default': 'None', 'unique': 'True', 'max_length': '2', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'db_index': 'True'}),
            'num_code': ('django.db.models.fields.CharField', [], {'default': 'None', 'unique': 'True', 'max_length': '3'}),
            'region': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'default': "''", 'unique': 'True', 'max_length': '32', 'blank': 'True'})
        },
        'geo.currency': {
            'Meta': {'ordering': "['code']", 'object_name': 'Currency'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'default': "''", 'unique': 'True', 'max_length': '32', 'blank': 'True'})
        },
        'geo.location': {
            'Meta': {'ordering': "(u'_order',)", 'unique_together': "(('area', 'name'),)", 'object_name': 'Location'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'acc': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'area': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.AdministrativeArea']", 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Country']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_administrative': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_capital': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '18', 'decimal_places': '12', 'blank': 'True'}),
            'lng': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '18', 'decimal_places': '12', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.LocationType']", 'null': 'True', 'blank': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'default': "''", 'unique': 'True', 'max_length': '32', 'blank': 'True'})
        },
        'geo.locationtype': {
            'Meta': {'object_name': 'LocationType'},
            'description': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'default': "''", 'unique': 'True', 'max_length': '32', 'blank': 'True'})
        }
    }

    complete_apps = ['geo']