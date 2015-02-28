from django.db import models

# Create your models here.

class SpotifyData(models.Model):
    uri = models.CharField(max_length=300, unique=True)
    #here can different information be stored as images,...