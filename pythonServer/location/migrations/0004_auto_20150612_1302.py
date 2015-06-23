# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0003_auto_20150612_1108'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='address',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='location',
            name='barrier',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='location',
            name='highway',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='location',
            name='is_in',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='location',
            name='man_made',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='location',
            name='osm_id',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='location',
            name='other_tags',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='location',
            name='place',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='location',
            name='ref',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='location',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='location',
            name='countryCode',
        ),
        migrations.RemoveField(
            model_name='location',
            name='countryName',
        ),
    ]
