from django.db import models
from location.models import Location

# Create your models here.

class Artist(models.Model):
    name = models.CharField(max_length=100)
    location = models.ManyToManyField(Location, related_name='location')