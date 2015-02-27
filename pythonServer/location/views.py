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
import requests
from xml.dom.minidom import parseString


logger = logging.getLogger(__name__)

# Create your views here.

# Create your views here.
@api_view(['GET'])
def getArtistList(request,latitude=1,longitude=1, format=None):
     artists = Artist.objects.all()
     serializer = ArtistSerializer(artists, many = True)
     getNearbyPlaces(latitude,longitude)
     return Response(serializer.data)

#get Spotify Ids
def getSpotifyId():
     url = 'https://api.spotify.com/v1/search?query=die+fantastischen+vier&type=track'
     r = requests.get(url);
     #Problem if user asks again => gets the same uri
     logger.error(r.json()["tracks"]["items"][0]["uri"])

#get artists for city
def getArtistForCity(city):
     city="Stuttgart"
     url= 'http://musicbrainz.org/ws/2/artist/?query=beginarea:'+city+'%20OR%20area:'+city+'%20OR%20endarea:'+city+'&limit=100'
     r = requests.get(url)
     dom2 = parseString(r.text)
     #logger.error(dom2.toxml())
     for node in dom2.getElementsByTagName('artist'):  # visit every node <bar />
          #get Artist Names
          logger.error(node.firstChild.firstChild.nodeValue)
     getSpotifyId()


#get nearbyPlaces using the geonames api
def getNearbyPlaces(latitude,longitude):
     request = 'http://api.geonames.org/findNearbyPlaceNameJSON?lat='+latitude +'&lng='+longitude+'&radius=300&maxRow=15&cities=cities15000&username=' + loadGeoUsername()
     response = urllib.request.urlopen(request)
     data = json.loads(response.read().decode("utf-8"))

     for num in range(0,len(data["geonames"])):
          logger.error(data["geonames"][num]["toponymName"])
     #logger.error(data["geonames"][0]["toponymName"])
     getArtistForCity(data["geonames"][0]["toponymName"])


def loadGeoUsername():
     with open ("username.txt", "r") as myfile:
          username=myfile.read()
     #logger.error(username)
     return username