# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0004_auto_20150612_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='countryCode',
            field=models.CharField(max_length=100, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='location',
            name='countryName',
            field=models.CharField(max_length=100, default=''),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='location',
            unique_together=set([('name', 'countryCode')]),
        ),
        migrations.RemoveField(
            model_name='location',
            name='address',
        ),
        migrations.RemoveField(
            model_name='location',
            name='barrier',
        ),
        migrations.RemoveField(
            model_name='location',
            name='highway',
        ),
        migrations.RemoveField(
            model_name='location',
            name='is_in',
        ),
        migrations.RemoveField(
            model_name='location',
            name='man_made',
        ),
        migrations.RemoveField(
            model_name='location',
            name='osm_id',
        ),
        migrations.RemoveField(
            model_name='location',
            name='other_tags',
        ),
        migrations.RemoveField(
            model_name='location',
            name='place',
        ),
        migrations.RemoveField(
            model_name='location',
            name='ref',
        ),
    ]
