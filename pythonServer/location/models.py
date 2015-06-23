from django.contrib.gis.db import models

# Create your models here.

class Location(models.Model):
    name = models.CharField(max_length=100)
    countryName = models.CharField(max_length=100, null=True)
    countryCode = models.CharField(max_length=100, null=True)
    population = models.IntegerField()
    geom = models.PointField()
    objects = models.GeoManager()

    class Meta:
        unique_together = ('name', 'countryCode',)

    def __str__(self):
        return str(self.name)

    def get_lat_long(self):
        """Add an easy getter function, which returns the geometry coords in
        latitude longitude order
        """
        return (self.geom.coords[0], self.geom.coords[1])