# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spotifyData', '0001_initial'),
        ('artist', '0002_artist_spotifyuri'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='spotifyUri',
            field=models.ForeignKey(default=1, to='spotifyData.SpotifyData'),
            preserve_default=False,
        ),
    ]
