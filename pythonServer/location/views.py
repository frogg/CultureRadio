from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from artist.models import Artist
from artist.serializers import ArtistSerializer
import logging

logger = logging.getLogger(__name__)

# Create your views here.

# Create your views here.
@api_view(['GET'])
def getArtistList(request,latitude=1,longitude=1, format=None):
     artists = Artist.objects.all()
     serializer = ArtistSerializer(artists, many = True)
     return Response(serializer.data)

#get nearbyPlaces using the geonames api
def getNearbyPlaces(latitude,longitude):
    # http://api.geonames.org/findNearbyPlaceName?lat=48.639291&lng=9.135565&radius=300&maxRow=50&cities=cities15000&username=loadFromGitIgnore
     loadGeoUsername()
     logger.error('test')

def loadGeoUsername():
     with open ("username.txt", "r") as myfile:
          username=myfile.read()
     logger.error(username)
     return username