# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Currency'
        db.create_table(u'geo_currency', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('uuidfield.fields.UUIDField')(blank=True, unique=True, default='', max_length=32)),
            ('iso_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=5, db_index=True)),
            ('numeric_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=5)),
            ('decimals', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('symbol', self.gf('django.db.models.fields.CharField')(blank=True, max_length=5, null=True)),
        ))
        db.send_create_signal('geo', ['Currency'])

        # Adding model 'Country'
        db.create_table(u'geo_country', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('iso_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=2, db_index=True)),
            ('iso_code3', self.gf('django.db.models.fields.CharField')(unique=True, max_length=3, db_index=True)),
            ('iso_num', self.gf('django.db.models.fields.CharField')(unique=True, max_length=3)),
            ('uuid', self.gf('uuidfield.fields.UUIDField')(blank=True, unique=True, default='', max_length=32)),
            ('name', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=100)),
            ('fullname', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=100)),
            ('region', self.gf('django.db.models.fields.IntegerField')(blank=True, default=None, null=True)),
            ('continent', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('currency', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, to=orm['geo.Currency'], null=True)),
            ('tld', self.gf('django.db.models.fields.CharField')(blank=True, max_length=5, null=True)),
            ('phone_prefix', self.gf('django.db.models.fields.CharField')(blank=True, max_length=20, null=True)),
            ('timezone', self.gf('timezone_field.fields.TimeZoneField')(blank=True, default=None, null=True)),
            ('expired', self.gf('django.db.models.fields.DateField')(blank=True, default=None, null=True)),
            ('lat', self.gf('django.db.models.fields.DecimalField')(blank=True, max_digits=18, decimal_places=12, null=True)),
            ('lng', self.gf('django.db.models.fields.DecimalField')(blank=True, max_digits=18, decimal_places=12, null=True)),
        ))
        db.send_create_signal('geo', ['Country'])

        # Adding model 'AdministrativeAreaType'
        db.create_table(u'geo_administrativeareatype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('uuidfield.fields.UUIDField')(blank=True, unique=True, default='', max_length=32)),
            ('name', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=100)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geo.Country'])),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, null=True, to=orm['geo.AdministrativeAreaType'], related_name='children')),
            ('_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            (u'lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('geo', ['AdministrativeAreaType'])

        # Adding unique constraint on 'AdministrativeAreaType', fields ['country', 'name']
        db.create_unique(u'geo_administrativeareatype', ['country_id', 'name'])

        # Adding model 'AdministrativeArea'
        db.create_table(u'geo_administrativearea', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('uuidfield.fields.UUIDField')(blank=True, unique=True, default='', max_length=32)),
            ('name', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=255)),
            ('code', self.gf('django.db.models.fields.CharField')(blank=True, null=True, db_index=True, max_length=10)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(to=orm['geo.AdministrativeArea'], blank=True, null=True, default=None, related_name='areas')),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geo.Country'], related_name='areas')),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geo.AdministrativeAreaType'])),
            ('_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            (u'lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('geo', ['AdministrativeArea'])

        # Adding unique constraint on 'AdministrativeArea', fields ['name', 'country', 'type']
        db.create_unique(u'geo_administrativearea', ['name', 'country_id', 'type_id'])

        # Adding model 'LocationType'
        db.create_table(u'geo_locationtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('uuidfield.fields.UUIDField')(blank=True, unique=True, default='', max_length=32)),
            ('description', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
        ))
        db.send_create_signal('geo', ['LocationType'])

        # Adding model 'Location'
        db.create_table(u'geo_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geo.Country'])),
            ('area', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, to=orm['geo.AdministrativeArea'], null=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, to=orm['geo.LocationType'], null=True)),
            ('is_capital', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_administrative', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('uuid', self.gf('uuidfield.fields.UUIDField')(blank=True, unique=True, default='', max_length=32)),
            ('name', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(blank=True, max_length=100, null=True)),
            ('lat', self.gf('django.db.models.fields.DecimalField')(blank=True, max_digits=18, decimal_places=12, null=True)),
            ('lng', self.gf('django.db.models.fields.DecimalField')(blank=True, max_digits=18, decimal_places=12, null=True)),
            ('acc', self.gf('django.db.models.fields.IntegerField')(blank=True, default=0, null=True)),
            ('_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('geo', ['Location'])

        # Adding unique constraint on 'Location', fields ['area', 'name']
        db.create_unique(u'geo_location', ['area_id', 'name'])


    def backwards(self, orm):
        # Removing unique constraint on 'Location', fields ['area', 'name']
        db.delete_unique(u'geo_location', ['area_id', 'name'])

        # Removing unique constraint on 'AdministrativeArea', fields ['name', 'country', 'type']
        db.delete_unique(u'geo_administrativearea', ['name', 'country_id', 'type_id'])

        # Removing unique constraint on 'AdministrativeAreaType', fields ['country', 'name']
        db.delete_unique(u'geo_administrativeareatype', ['country_id', 'name'])

        # Deleting model 'Currency'
        db.delete_table(u'geo_currency')

        # Deleting model 'Country'
        db.delete_table(u'geo_country')

        # Deleting model 'AdministrativeAreaType'
        db.delete_table(u'geo_administrativeareatype')

        # Deleting model 'AdministrativeArea'
        db.delete_table(u'geo_administrativearea')

        # Deleting model 'LocationType'
        db.delete_table(u'geo_locationtype')

        # Deleting model 'Location'
        db.delete_table(u'geo_location')


    models = {
        'geo.administrativearea': {
            'Meta': {'object_name': 'AdministrativeArea', 'ordering': "(u'_order',)", 'unique_together': "(('name', 'country', 'type'),)"},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'code': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'db_index': 'True', 'max_length': '10'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Country']", 'related_name': "'areas'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'to': "orm['geo.AdministrativeArea']", 'blank': 'True', 'null': 'True', 'default': 'None', 'related_name': "'areas'"}),
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
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['geo.AdministrativeAreaType']", 'related_name': "'children'"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'blank': 'True', 'unique': 'True', 'default': "''", 'max_length': '32'})
        },
        'geo.country': {
            'Meta': {'object_name': 'Country', 'ordering': "['name']"},
            'continent': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['geo.Currency']", 'null': 'True'}),
            'expired': ('django.db.models.fields.DateField', [], {'blank': 'True', 'default': 'None', 'null': 'True'}),
            'fullname': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2', 'db_index': 'True'}),
            'iso_code3': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3', 'db_index': 'True'}),
            'iso_num': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'blank': 'True', 'max_digits': '18', 'decimal_places': '12', 'null': 'True'}),
            'lng': ('django.db.models.fields.DecimalField', [], {'blank': 'True', 'max_digits': '18', 'decimal_places': '12', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100'}),
            'phone_prefix': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '20', 'null': 'True'}),
            'region': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'default': 'None', 'null': 'True'}),
            'timezone': ('timezone_field.fields.TimeZoneField', [], {'blank': 'True', 'default': 'None', 'null': 'True'}),
            'tld': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '5', 'null': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'blank': 'True', 'unique': 'True', 'default': "''", 'max_length': '32'})
        },
        'geo.currency': {
            'Meta': {'object_name': 'Currency', 'ordering': "['iso_code']"},
            'decimals': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'numeric_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            'symbol': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '5', 'null': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'blank': 'True', 'unique': 'True', 'default': "''", 'max_length': '32'})
        },
        'geo.location': {
            'Meta': {'object_name': 'Location', 'ordering': "(u'_order',)", 'unique_together': "(('area', 'name'),)"},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'acc': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'default': '0', 'null': 'True'}),
            'area': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['geo.AdministrativeArea']", 'null': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Country']"}),
            'description': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_administrative': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_capital': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'blank': 'True', 'max_digits': '18', 'decimal_places': '12', 'null': 'True'}),
            'lng': ('django.db.models.fields.DecimalField', [], {'blank': 'True', 'max_digits': '18', 'decimal_places': '12', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['geo.LocationType']", 'null': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'blank': 'True', 'unique': 'True', 'default': "''", 'max_length': '32'})
        },
        'geo.locationtype': {
            'Meta': {'object_name': 'LocationType'},
            'description': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'blank': 'True', 'unique': 'True', 'default': "''", 'max_length': '32'})
        }
    }

    complete_apps = ['geo']