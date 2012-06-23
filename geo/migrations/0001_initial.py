# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Currency'
        db.create_table('geo_currency', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=5)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('symbol', self.gf('django.db.models.fields.CharField')(max_length=5, null=True, blank=True)),
        ))
        db.send_create_signal('geo', ['Currency'])

        # Adding model 'Country'
        db.create_table('geo_country', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('iso_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=2, db_index=True)),
            ('iso3_code', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=3, null=True, blank=True)),
            ('num_code', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('fullname', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('region', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('continent', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('currency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geo.Currency'], null=True, blank=True)),
        ))
        db.send_create_signal('geo', ['Country'])

        # Adding model 'AdministrativeAreaType'
        db.create_table('geo_administrativeareatype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geo.Country'])),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['geo.AdministrativeAreaType'])),
            ('_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('geo', ['AdministrativeAreaType'])

        # Adding model 'AdministrativeArea'
        db.create_table('geo_administrativearea', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=5, db_index=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='areas', null=True, to=orm['geo.AdministrativeArea'])),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(related_name='areas', to=orm['geo.Country'])),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geo.AdministrativeAreaType'])),
            ('_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('geo', ['AdministrativeArea'])

        # Adding unique constraint on 'AdministrativeArea', fields ['name', 'country', 'type']
        db.create_unique('geo_administrativearea', ['name', 'country_id', 'type_id'])

        # Adding model 'Location'
        db.create_table('geo_location', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geo.Country'])),
            ('area', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geo.AdministrativeArea'], null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('is_capital', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_administrative', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('lat', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=18, decimal_places=12, blank=True)),
            ('lng', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=18, decimal_places=12, blank=True)),
            ('acc', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('geo', ['Location'])


    def backwards(self, orm):
        # Removing unique constraint on 'AdministrativeArea', fields ['name', 'country', 'type']
        db.delete_unique('geo_administrativearea', ['name', 'country_id', 'type_id'])

        # Deleting model 'Currency'
        db.delete_table('geo_currency')

        # Deleting model 'Country'
        db.delete_table('geo_country')

        # Deleting model 'AdministrativeAreaType'
        db.delete_table('geo_administrativeareatype')

        # Deleting model 'AdministrativeArea'
        db.delete_table('geo_administrativearea')

        # Deleting model 'Location'
        db.delete_table('geo_location')


    models = {
        'geo.administrativearea': {
            'Meta': {'ordering': "('_order',)", 'unique_together': "(('name', 'country', 'type'),)", 'object_name': 'AdministrativeArea'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True'}),
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
            'Meta': {'ordering': "('_order',)", 'object_name': 'AdministrativeAreaType'},
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
            'fullname': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso3_code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'iso_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'num_code': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
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
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['geo']