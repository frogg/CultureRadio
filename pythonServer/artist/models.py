from django.db import models
from location.models import Location
from spotifyData.models import SpotifyData

# Create your models here.

class Artist(models.Model):
    name = models.CharField(max_length=100)
    spotifyUri = models.ForeignKey(SpotifyData)
    #check for unique tuple at many to many realtionship
    location = models.ManyToManyField(Location, related_name='location')

