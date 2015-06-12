from django.db import models
from spotifyData.models import SpotifyData


class Track(models.Model):
    artist = models.ForeignKey('artist.Artist')
    spotify_uri = models.ForeignKey(SpotifyData)
    name = models.CharField(max_length=300)