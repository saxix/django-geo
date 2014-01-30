# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Country.name_de'
        db.add_column(u'geo_country', 'name_de',
                      self.gf('django.db.models.fields.CharField')(null=True, blank=True, max_length=100, db_index=True),
                      keep_default=False)

        # Adding field 'Country.name_en'
        db.add_column(u'geo_country', 'name_en',
                      self.gf('django.db.models.fields.CharField')(null=True, blank=True, max_length=100, db_index=True),
                      keep_default=False)

        # Adding field 'Country.name_zh'
        db.add_column(u'geo_country', 'name_zh',
                      self.gf('django.db.models.fields.CharField')(null=True, blank=True, max_length=100, db_index=True),
                      keep_default=False)

        # Adding field 'Country.name_it'
        db.add_column(u'geo_country', 'name_it',
                      self.gf('django.db.models.fields.CharField')(null=True, blank=True, max_length=100, db_index=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Country.name_de'
        db.delete_column(u'geo_country', 'name_de')

        # Deleting field 'Country.name_en'
        db.delete_column(u'geo_country', 'name_en')

        # Deleting field 'Country.name_zh'
        db.delete_column(u'geo_country', 'name_zh')

        # Deleting field 'Country.name_it'
        db.delete_column(u'geo_country', 'name_it')


    models = {
        'geo.administrativearea': {
            'Meta': {'unique_together': "(('name', 'country', 'type'),)", 'object_name': 'AdministrativeArea', 'ordering': "(u'_order',)"},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'code': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '10', 'db_index': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'areas'", 'to': "orm['geo.Country']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'null': 'True', 'default': 'None', 'related_name': "'areas'", 'blank': 'True', 'to': "orm['geo.AdministrativeArea']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.AdministrativeAreaType']"}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'default': "''", 'blank': 'True', 'max_length': '32'})
        },
        'geo.administrativeareatype': {
            'Meta': {'unique_together': "(('country', 'name'),)", 'object_name': 'AdministrativeAreaType', 'ordering': "(u'_order',)"},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Country']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['geo.AdministrativeAreaType']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'default': "''", 'blank': 'True', 'max_length': '32'})
        },
        'geo.country': {
            'Meta': {'object_name': 'Country', 'ordering': "['name']"},
            'continent': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Currency']", 'null': 'True', 'blank': 'True'}),
            'expired': ('django.db.models.fields.DateField', [], {'default': 'None', 'blank': 'True', 'null': 'True'}),
            'fullname': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'db_index': 'True', 'max_length': '2'}),
            'iso_code3': ('django.db.models.fields.CharField', [], {'unique': 'True', 'db_index': 'True', 'max_length': '3'}),
            'iso_num': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True', 'auto_now': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'decimal_places': '12', 'blank': 'True', 'null': 'True', 'max_digits': '18'}),
            'lng': ('django.db.models.fields.DecimalField', [], {'decimal_places': '12', 'blank': 'True', 'null': 'True', 'max_digits': '18'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100'}),
            'name_de': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '100', 'db_index': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '100', 'db_index': 'True'}),
            'name_it': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '100', 'db_index': 'True'}),
            'name_zh': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '100', 'db_index': 'True'}),
            'phone_prefix': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '20'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['geo.UNRegion']", 'null': 'True', 'blank': 'True'}),
            'timezone': ('timezone_field.fields.TimeZoneField', [], {'default': 'None', 'blank': 'True', 'null': 'True'}),
            'tld': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '5'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'default': "''", 'blank': 'True', 'max_length': '32'})
        },
        'geo.currency': {
            'Meta': {'object_name': 'Currency', 'ordering': "['iso_code']"},
            'decimals': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'db_index': 'True', 'max_length': '5'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'numeric_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            'symbol': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '5'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'default': "''", 'blank': 'True', 'max_length': '32'})
        },
        'geo.location': {
            'Meta': {'unique_together': "(('area', 'name'),)", 'object_name': 'Location', 'ordering': "(u'_order',)"},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'acc': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True', 'null': 'True'}),
            'area': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.AdministrativeArea']", 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Country']"}),
            'description': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_administrative': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_capital': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'decimal_places': '12', 'blank': 'True', 'null': 'True', 'max_digits': '18'}),
            'lng': ('django.db.models.fields.DecimalField', [], {'decimal_places': '12', 'blank': 'True', 'null': 'True', 'max_digits': '18'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.LocationType']", 'null': 'True', 'blank': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'default': "''", 'blank': 'True', 'max_length': '32'})
        },
        'geo.locationtype': {
            'Meta': {'object_name': 'LocationType'},
            'description': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'default': "''", 'blank': 'True', 'max_length': '32'})
        },
        'geo.unregion': {
            'Meta': {'object_name': 'UNRegion', 'ordering': "['name']"},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'db_index': 'True', 'max_length': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['geo']