# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='countryName',
            field=models.CharField(max_length=100, default='Switzerland'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='location',
            unique_together=set([('name', 'countryCode')]),
        ),
    ]
