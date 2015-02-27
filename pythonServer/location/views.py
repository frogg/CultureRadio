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
def getSpotifyUris(request,latitude=1,longitude=1, format=None):
     artists = Artist.objects.all()
     serializer = ArtistSerializer(artists, many = True)

     #return Response(serializer.data)
     #check if there is an existing entry in database (not far away from current location)

     dic = getNearbyPlaces(latitude,longitude)
     #logger.error(type(dic))
     if dic["continueSearching"] != True :
          return Response(dic)
     return Response('Noting found yet')

#get Spotify Ids
def getSpotifyId(artist):
     url = 'https://api.spotify.com/v1/search?query='+ artist +'&type=track'
     r = requests.get(url);
     #Problem if user asks again => gets the same uri
     try:
          #logger.error(r.json()["tracks"]["items"][0]["uri"])
          return {'continueSearching':False, 'result':r.json()["tracks"]["items"][0]["uri"]}
     except:
          return {'continueSearching':True, 'result':""}



#get artists for city
def getArtistForCity(city):
     #city="San Francisco" #dummyData
     #improvement idea => ask for multiple cities at one time with or
     url= 'http://musicbrainz.org/ws/2/artist/?query=beginarea:'+city+'%20OR%20area:'+city+'%20OR%20endarea:'+city+'&limit=100'
     r = requests.get(url)
     dom = parseString(r.text)
     #logger.error(dom2.toxml())
     #go through the artists
     for node in dom.getElementsByTagName('artist'):  # visit every node with this tag
          #node.firstChild.firstChild.nodeValue is the artists name
          dic = getSpotifyId(node.firstChild.firstChild.nodeValue)
          #logger.error(node.firstChild.firstChild.nodeValue)
          if dic["continueSearching"] !=True :
               #stop searching and return result
               return {'continueSearching':False, 'result':dic["result"],'city':city}
     #found nothing till now => continue searching
     return {'continueSearching':True, 'result':""}


#get nearbyPlaces using the geonames api
def getNearbyPlaces(latitude,longitude):
     request = 'http://api.geonames.org/findNearbyPlaceNameJSON?lat='+latitude +'&lng='+longitude+'&radius=300&maxRow=15&cities=cities15000&username=' + loadGeoUsername()
     response = urllib.request.urlopen(request)
     data = json.loads(response.read().decode("utf-8"))

     for num in range(0,len(data["geonames"])):
          dic = getArtistForCity(data["geonames"][num]["toponymName"])
          if dic["continueSearching"] !=True :
               #stop searching and return result
               return {'continueSearching':False, 'result':dic["result"],'city':dic["city"]}
          else:
               logger.error(data["geonames"][num]["toponymName"])

     #logger.error(data["geonames"][0]["toponymName"])
     return {'continueSearching':True, 'result':""}



def loadGeoUsername():
     with open ("username.txt", "r") as myfile:
          username=myfile.read()
     #logger.error(username)
     return username