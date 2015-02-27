from django.db import models
from location.models import Location
from spotifyData.models import SpotifyData

# Create your models here.

class Artist(models.Model):
    name = models.CharField(max_length=100)
    spotifyUri = models.OneToOneField(SpotifyData)
    location = models.ManyToManyField(Location, related_name='location')