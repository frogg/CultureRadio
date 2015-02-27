# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('countryCode', models.CharField(max_length=100)),
                ('latitude', models.DecimalField(max_digits=20, decimal_places=10)),
                ('longitude', models.DecimalField(max_digits=20, decimal_places=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
