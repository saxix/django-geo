# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LocationType'
        db.create_table('geo_locationtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
        ))
        db.send_create_signal('geo', ['LocationType'])

        # Adding unique constraint on 'AdministrativeAreaType', fields ['country', 'name']
        db.create_unique('geo_administrativeareatype', ['country_id', 'name'])


        # Renaming column for 'Location.type' to match new field type.
        db.rename_column('geo_location', 'type', 'type_id')
        # Changing field 'Location.type'
        db.alter_column('geo_location', 'type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geo.LocationType'], null=True))
        # Adding index on 'Location', fields ['type']
        db.create_index('geo_location', ['type_id'])


    def backwards(self, orm):
        # Removing index on 'Location', fields ['type']
        db.delete_index('geo_location', ['type_id'])

        # Removing unique constraint on 'AdministrativeAreaType', fields ['country', 'name']
        db.delete_unique('geo_administrativeareatype', ['country_id', 'name'])

        # Deleting model 'LocationType'
        db.delete_table('geo_locationtype')


        # Renaming column for 'Location.type' to match new field type.
        db.rename_column('geo_location', 'type_id', 'type')
        # Changing field 'Location.type'
        db.alter_column('geo_location', 'type', self.gf('django.db.models.fields.IntegerField')())

    models = {
        'geo.administrativearea': {
            'Meta': {'ordering': "('_order',)", 'unique_together': "(('name', 'country', 'type'),)", 'object_name': 'AdministrativeArea'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'areas'", 'to': "orm['geo.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'areas'", 'null': 'True', 'to': "orm['geo.AdministrativeArea']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.AdministrativeAreaType']"})
        },
        'geo.administrativeareatype': {
            'Meta': {'ordering': "('_order',)", 'unique_together': "(('country', 'name'),)", 'object_name': 'AdministrativeAreaType'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['geo.AdministrativeAreaType']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'geo.country': {
            'Meta': {'ordering': "['name']", 'object_name': 'Country'},
            'continent': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Currency']", 'null': 'True', 'blank': 'True'}),
            'fullname': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso3_code': ('django.db.models.fields.CharField', [], {'default': 'None', 'unique': 'True', 'max_length': '3', 'db_index': 'True'}),
            'iso_code': ('django.db.models.fields.CharField', [], {'default': 'None', 'unique': 'True', 'max_length': '2', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'db_index': 'True'}),
            'num_code': ('django.db.models.fields.CharField', [], {'default': 'None', 'unique': 'True', 'max_length': '3'}),
            'region': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'geo.currency': {
            'Meta': {'ordering': "['code']", 'object_name': 'Currency'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'})
        },
        'geo.location': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Location'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'acc': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'area': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.AdministrativeArea']", 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Country']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_administrative': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_capital': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '18', 'decimal_places': '12', 'blank': 'True'}),
            'lng': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '18', 'decimal_places': '12', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.LocationType']", 'null': 'True', 'blank': 'True'})
        },
        'geo.locationtype': {
            'Meta': {'object_name': 'LocationType'},
            'description': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['geo']