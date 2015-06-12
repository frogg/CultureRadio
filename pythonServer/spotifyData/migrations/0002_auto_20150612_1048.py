# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spotifyData', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spotifydata',
            name='uri',
            field=models.CharField(unique=True, max_length=300),
        ),
    ]
