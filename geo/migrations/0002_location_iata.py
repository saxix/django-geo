# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='iata',
            field=models.CharField(verbose_name='IATA code (if exists)', blank=True, max_length=255, db_index=True, null=True),
            preserve_default=True,
        ),
    ]
