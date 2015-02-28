from django.db import models

# Create your models here.

class Location(models.Model):
    name = models.CharField(max_length=100)
    countryName = models.CharField(max_length=100)
    countryCode = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=20, decimal_places = 10)
    longitude = models.DecimalField(max_digits=20, decimal_places = 10)

    class Meta:
        unique_together = ('name', 'countryCode',)