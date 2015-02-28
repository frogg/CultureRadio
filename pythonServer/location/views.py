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
from location.models import Location
from rest_framework.renderers import JSONRenderer
from location.serializers import LocationSerializer
from spotifyData.models import SpotifyData


logger = logging.getLogger(__name__)

# Create your views here.

# Create your views here.
@api_view(['GET'])
def getSpotifyUris(request,latitude=1,longitude=1, format=None):
     artists = Artist.objects.all()
     serializer = ArtistSerializer(artists, many = True)

     #return Response(serializer.data)
     #check if there is an existing entry in database (not far away from current location)
     list = []
     dic = getNearbyPlaces(latitude,longitude)
     #logger.error(type(dic))
     if len(dic["result"])>0:
          return Response(dic)
     return Response('Nothing found')

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
def getArtistForCity(location):
     #city="San Francisco" #dummyData
     city = location.name
     #improvement idea => ask for multiple cities at one time with or
     url= 'http://musicbrainz.org/ws/2/artist/?query=beginarea:'+city+'%20OR%20area:'+city+'%20OR%20endarea:'+city+'&limit=100'
     r = requests.get(url)
     dom = parseString(r.text)
     listResults = []
     #logger.error(dom2.toxml())
     serializer = LocationSerializer(location)
     #go through the artists
     for node in dom.getElementsByTagName('artist'):  # visit every node with this tag
          #node.firstChild.firstChild.nodeValue is the artists name
          dic = getSpotifyId(node.firstChild.firstChild.nodeValue)
          #logger.error(node.firstChild.firstChild.nodeValue)
          if not dic["continueSearching"] :
               artistName = node.firstChild.firstChild.nodeValue
               listResults.append({'uri':dic["result"],'location':serializer.data,'artist':artistName})
               #stop searching and return result
               try:
                    location.save()
               #location is already stored in database
               except:
                    logger.error('already stored')
                    spotify = SpotifyData(uri = dic["result"])
                    artist = Artist(name=artistName)
                    #get_or_create: useful
                    spotify.save()
                    artist.spotifyUri=spotify
                    artist.save()
                    #query for location
                    #artist.location.add(location)


               if(len(listResults)>5):
                    return {'continueSearching':False, 'result':listResults}

     #found nothing less than x results => continue searching
     return {'continueSearching':True, 'result':listResults}


#get nearbyPlaces using the geonames api
def getNearbyPlaces(latitude,longitude):
     request = 'http://api.geonames.org/findNearbyPlaceNameJSON?lat='+latitude +'&lng='+longitude+'&radius=300&maxRow=15&cities=cities15000&username=' + loadGeoUsername()
     response = urllib.request.urlopen(request)
     data = json.loads(response.read().decode("utf-8"))
     listResults = []
     for num in range(0,len(data["geonames"])):
          da = data["geonames"][num]
          #data["geonames"][num]["toponymName"] contains the city names
          location = Location(name=da["toponymName"], countryName=da["countryName"], countryCode=da["countryCode"],latitude=da["lat"],longitude=da["lng"])
          #location.save() don't save location here, just save locations with spotify tracks connected
          dic = getArtistForCity(location)
          if not dic["continueSearching"] or (len(listResults)+len(dic["result"]))>5:
               listResults.extend(dic["result"])
               #stop searching and return result immediatly (interrupt for-loop)
               return {'result':listResults}

     return {'result':listResults}


def loadGeoUsername():
     with open ("username.txt", "r") as myfile:
          username=myfile.read()
     #logger.error(username)
     return username


