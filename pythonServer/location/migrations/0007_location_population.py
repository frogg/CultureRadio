# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0006_auto_20150612_1334'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='population',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
