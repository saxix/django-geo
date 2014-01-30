# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Country.name_fr'
        db.add_column(u'geo_country', 'name_fr',
                      self.gf('django.db.models.fields.CharField')(db_index=True, null=True, blank=True, max_length=100),
                      keep_default=False)

        # Adding field 'Country.name_ru'
        db.add_column(u'geo_country', 'name_ru',
                      self.gf('django.db.models.fields.CharField')(db_index=True, null=True, blank=True, max_length=100),
                      keep_default=False)

        # Adding field 'Country.name_es'
        db.add_column(u'geo_country', 'name_es',
                      self.gf('django.db.models.fields.CharField')(db_index=True, null=True, blank=True, max_length=100),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Country.name_fr'
        db.delete_column(u'geo_country', 'name_fr')

        # Deleting field 'Country.name_ru'
        db.delete_column(u'geo_country', 'name_ru')

        # Deleting field 'Country.name_es'
        db.delete_column(u'geo_country', 'name_es')


    models = {
        'geo.administrativearea': {
            'Meta': {'object_name': 'AdministrativeArea', 'ordering': "(u'_order',)", 'unique_together': "(('name', 'country', 'type'),)"},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True', 'max_length': '10'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'areas'", 'to': "orm['geo.Country']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'related_name': "'areas'", 'null': 'True', 'to': "orm['geo.AdministrativeArea']", 'default': 'None', 'blank': 'True'}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.AdministrativeAreaType']"}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'blank': 'True', 'default': "''", 'max_length': '32'})
        },
        'geo.administrativeareatype': {
            'Meta': {'object_name': 'AdministrativeAreaType', 'ordering': "(u'_order',)", 'unique_together': "(('country', 'name'),)"},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Country']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'related_name': "'children'", 'null': 'True', 'to': "orm['geo.AdministrativeAreaType']", 'blank': 'True'}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'blank': 'True', 'default': "''", 'max_length': '32'})
        },
        'geo.country': {
            'Meta': {'object_name': 'Country', 'ordering': "['name']"},
            'continent': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['geo.Currency']", 'blank': 'True'}),
            'expired': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True', 'default': 'None'}),
            'fullname': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'db_index': 'True', 'max_length': '2'}),
            'iso_code3': ('django.db.models.fields.CharField', [], {'unique': 'True', 'db_index': 'True', 'max_length': '3'}),
            'iso_num': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True', 'default': 'datetime.datetime.now'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '18', 'decimal_places': '12', 'blank': 'True'}),
            'lng': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '18', 'decimal_places': '12', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100'}),
            'name_de': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True', 'max_length': '100'}),
            'name_en': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True', 'max_length': '100'}),
            'name_es': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True', 'max_length': '100'}),
            'name_fr': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True', 'max_length': '100'}),
            'name_it': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True', 'max_length': '100'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True', 'max_length': '100'}),
            'name_zh': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True', 'max_length': '100'}),
            'phone_prefix': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '20'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['geo.UNRegion']", 'default': 'None', 'blank': 'True'}),
            'timezone': ('timezone_field.fields.TimeZoneField', [], {'null': 'True', 'blank': 'True', 'default': 'None'}),
            'tld': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '5'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'blank': 'True', 'default': "''", 'max_length': '32'})
        },
        'geo.currency': {
            'Meta': {'object_name': 'Currency', 'ordering': "['iso_code']"},
            'decimals': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'db_index': 'True', 'max_length': '5'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'numeric_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            'symbol': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '5'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'blank': 'True', 'default': "''", 'max_length': '32'})
        },
        'geo.location': {
            'Meta': {'object_name': 'Location', 'ordering': "(u'_order',)", 'unique_together': "(('area', 'name'),)"},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'acc': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True', 'default': '0'}),
            'area': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['geo.AdministrativeArea']", 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Country']"}),
            'description': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_administrative': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_capital': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '18', 'decimal_places': '12', 'blank': 'True'}),
            'lng': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '18', 'decimal_places': '12', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['geo.LocationType']", 'blank': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'blank': 'True', 'default': "''", 'max_length': '32'})
        },
        'geo.locationtype': {
            'Meta': {'object_name': 'LocationType'},
            'description': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'blank': 'True', 'default': "''", 'max_length': '32'})
        },
        'geo.unregion': {
            'Meta': {'object_name': 'UNRegion', 'ordering': "['name']"},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'db_index': 'True', 'max_length': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['geo']