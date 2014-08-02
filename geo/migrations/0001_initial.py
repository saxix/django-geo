# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import bitfield.models
import django.core.validators
import mptt.fields
import uuidfield.fields
import timezone_field.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdministrativeArea',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('uuid', uuidfield.fields.UUIDField(help_text='unique id', unique=True, editable=False, blank=True, default=b'', max_length=32)),
                ('name', models.CharField(max_length=255, verbose_name='Name', db_index=True)),
                ('code', models.CharField(help_text=b'ISO 3166-2 code', verbose_name='Code', db_index=True, blank=True, null=True, max_length=10)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(to='geo.AdministrativeArea', blank=True, default=None, null=True)),
            ],
            options={
                'verbose_name_plural': 'Administrative Areas',
                'ordering': [b'name'],
                'verbose_name': 'Administrative Area',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AdministrativeAreaType',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('uuid', uuidfield.fields.UUIDField(help_text='unique id', unique=True, editable=False, blank=True, default=b'', max_length=32)),
                ('name', models.CharField(max_length=100, verbose_name='Name', db_index=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(to='geo.AdministrativeAreaType', blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Administrative Area Types',
                'ordering': [b'name'],
                'verbose_name': 'Administrative Area Type',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='administrativearea',
            name='type',
            field=models.ForeignKey(to='geo.AdministrativeAreaType'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('iso_code', models.CharField(max_length=2, db_index=True, unique=True, help_text=b'ISO 3166-1 alpha 2', validators=[django.core.validators.MinLengthValidator(2)])),
                ('iso_code3', models.CharField(max_length=3, db_index=True, unique=True, help_text=b'ISO 3166-1 alpha 3', validators=[django.core.validators.MinLengthValidator(3)])),
                ('iso_num', models.CharField(max_length=3, unique=True, help_text=b'ISO 3166-1 numeric', validators=[django.core.validators.RegexValidator(b'\\d\\d\\d')])),
                ('uuid', uuidfield.fields.UUIDField(help_text='unique id', unique=True, editable=False, blank=True, default=b'', max_length=32)),
                ('undp', models.CharField(validators=[django.core.validators.MinLengthValidator(3)], help_text=b'UNDP code', unique=True, blank=True, max_length=3, null=True)),
                ('nato3', models.CharField(validators=[django.core.validators.MinLengthValidator(3)], help_text=b'NATO3 code', unique=True, blank=True, max_length=3, null=True)),
                ('fips', models.CharField(blank=True, max_length=255, help_text=b'fips code', null=True)),
                ('itu', models.CharField(blank=True, max_length=255, help_text=b'ITU code', null=True)),
                ('icao', models.CharField(blank=True, max_length=255, help_text=b'ICAO code', null=True)),
                ('name', models.CharField(max_length=100, db_index=True)),
                ('fullname', models.CharField(max_length=100, db_index=True)),
                ('continent', models.CharField(choices=[(b'AF', 'Africa'), (b'AN', 'Antartica'), (b'AS', 'Asia'), (b'EU', 'Europe'), (b'NA', 'North America'), (b'OC', 'Oceania'), (b'SA', 'South America')], max_length=2)),
                ('tld', models.CharField(blank=True, max_length=5, help_text=b'Internet tld', null=True)),
                ('phone_prefix', models.CharField(blank=True, max_length=20, help_text=b'Phone prefix number', null=True)),
                ('timezone', timezone_field.fields.TimeZoneField(blank=True, default=None, max_length=63, choices=None, null=True)),
                ('expired', models.DateField(blank=True, default=None, null=True)),
                ('lat', models.DecimalField(blank=True, decimal_places=12, verbose_name=b'Latitude', max_digits=18, null=True)),
                ('lng', models.DecimalField(blank=True, decimal_places=12, verbose_name=b'Longitude', max_digits=18, null=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': [b'name'],
                'verbose_name_plural': 'Countries',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='administrativeareatype',
            name='country',
            field=models.ForeignKey(to='geo.Country'),
            preserve_default=True,
        ),
        migrations.AlterOrderWithRespectTo(
            name='administrativeareatype',
            order_with_respect_to=b'country',
        ),
        migrations.AlterUniqueTogether(
            name='administrativeareatype',
            unique_together=set([(b'country', b'name')]),
        ),
        migrations.AddField(
            model_name='administrativearea',
            name='country',
            field=models.ForeignKey(to='geo.Country'),
            preserve_default=True,
        ),
        migrations.AlterOrderWithRespectTo(
            name='administrativearea',
            order_with_respect_to=b'country',
        ),
        migrations.AlterUniqueTogether(
            name='administrativearea',
            unique_together=set([(b'name', b'country', b'type')]),
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('uuid', uuidfield.fields.UUIDField(help_text='unique id', unique=True, editable=False, blank=True, default=b'', max_length=32)),
                ('iso_code', models.CharField(max_length=5, unique=True, help_text=b'ISO 4217 code', db_index=True)),
                ('numeric_code', models.CharField(unique=True, help_text=b'ISO 4217 code', max_length=5)),
                ('decimals', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=100)),
                ('symbol', models.CharField(blank=True, max_length=5, null=True)),
            ],
            options={
                'ordering': [b'iso_code'],
                'verbose_name_plural': b'Currencies',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='country',
            name='currency',
            field=models.ForeignKey(to='geo.Currency', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('is_capital', models.BooleanField(default=False, help_text=b'True if is the capital of `country`')),
                ('is_administrative', models.BooleanField(default=False, help_text=b'True if is administrative for `area`')),
                ('uuid', uuidfield.fields.UUIDField(help_text='unique id', unique=True, editable=False, blank=True, default=b'', max_length=32)),
                ('name', models.CharField(max_length=255, verbose_name='Name', db_index=True)),
                ('loccode', models.CharField(blank=True, max_length=255, null=True, verbose_name='UN LOCODE', db_index=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('lat', models.DecimalField(blank=True, decimal_places=12, max_digits=18, null=True)),
                ('lng', models.DecimalField(blank=True, decimal_places=12, max_digits=18, null=True)),
                ('acc', models.IntegerField(blank=True, default=0, choices=[(0, 'None'), (10, 'Country'), (20, 'Exact')], help_text=b'Define the level of accuracy of lat/lng infos', null=True)),
                ('flags', bitfield.models.BitField(default=0, flags=[])),
                ('status', models.CharField(blank=True, max_length=2, choices=[(b'AA', b'Approved by competent national government agency'), (b'AC', b'Approved by Customs Authority'), (b'AF', b'Approved by national facilitation body'), (b'AI', b'Code adopted by international organisation (IATA or ECLAC)'), (b'RL', b'Recognised location - Existence and representation of location name confirmed by check against nominated gazetteer or other reference work'), (b'RN', b'Request from credible national sources for locations in their own country'), (b'RQ', b'Request under consideration'), (b'RR', b'Request rejected'), (b'QQ', b'Original entry not verified since date indicated'), (b'XX', b'Entry that will be removed from the next issue of UN/LOCODE')], null=True)),
                ('area', models.ForeignKey(to='geo.AdministrativeArea', blank=True, null=True)),
                ('country', models.ForeignKey(to='geo.Country')),
            ],
            options={
                'verbose_name_plural': 'Locations',
                'ordering': (b'name', b'country'),
                'verbose_name': 'Location',
            },
            bases=(models.Model,),
        ),
        migrations.AlterOrderWithRespectTo(
            name='location',
            order_with_respect_to=b'country',
        ),
        migrations.CreateModel(
            name='LocationType',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('uuid', uuidfield.fields.UUIDField(help_text='unique id', unique=True, editable=False, blank=True, default=b'', max_length=32)),
                ('description', models.CharField(unique=True, max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Location Types',
                'verbose_name': 'Location Type',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='location',
            name='type',
            field=models.ForeignKey(to='geo.LocationType', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='location',
            unique_together=set([(b'area', b'name')]),
        ),
        migrations.CreateModel(
            name='UNRegion',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('code', models.CharField(max_length=5, unique=True, db_index=True)),
                ('name', models.CharField(max_length=100)),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': [b'name'],
                'verbose_name_plural': 'UN Regions',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='country',
            name='region',
            field=models.ForeignKey(to='geo.UNRegion', blank=True, default=None, null=True),
            preserve_default=True,
        ),
    ]
