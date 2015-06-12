# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spotifyData', '0002_auto_20150612_1048'),
        ('artist', '0003_artist_spotifyuri'),
    ]

    operations = [
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=300)),
                ('artist', models.ForeignKey(to='artist.Artist')),
                ('spotify_uri', models.ForeignKey(to='spotifyData.SpotifyData')),
            ],
        ),
    ]
