# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0002_auto_20150228_0921'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='location',
            name='longitude',
        ),
        migrations.AddField(
            model_name='location',
            name='geom',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, default=0),
            preserve_default=False,
        ),
    ]
