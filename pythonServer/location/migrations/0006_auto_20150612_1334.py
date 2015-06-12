# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0005_auto_20150612_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='countryCode',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='countryName',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
