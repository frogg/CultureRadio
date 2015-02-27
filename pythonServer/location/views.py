from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from artist.models import Artist
from artist.serializers import ArtistSerializer
#for python3
import urllib.request
import logging
import json


logger = logging.getLogger(__name__)

# Create your views here.

# Create your views here.
@api_view(['GET'])
def getArtistList(request,latitude=1,longitude=1, format=None):
     artists = Artist.objects.all()
     serializer = ArtistSerializer(artists, many = True)
     getNearbyPlaces(latitude,longitude)
     return Response(serializer.data)

#get nearbyPlaces using the geonames api
def getNearbyPlaces(latitude,longitude):
     request = 'http://api.geonames.org/findNearbyPlaceNameJSON?lat='+latitude +'&lng='+longitude+'&radius=300&maxRow=15&cities=cities15000&username=' + loadGeoUsername()
     response = urllib.request.urlopen(request)
     data = json.loads(response.read().decode("utf-8"))
     logger.error('test')
     logger.error(data["geonames"][0]["toponymName"])




def loadGeoUsername():
     with open ("username.txt", "r") as myfile:
          username=myfile.read()
     #logger.error(username)
     return username