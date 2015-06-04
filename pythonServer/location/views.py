import os
from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from artist.models import Artist
from artist.serializers import ArtistSerializer
# for python3
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
def get_spotify_uris(request, latitude=1, longitude=1, format=None):
    dic = get_nearby_places(latitude, longitude)
    # logger.error(type(dic))
    if len(dic["result"]) > 0:
        return Response(dic)
    else:
        logger.error('enlarge search radius')
        # move position for 300km
        for x in range(0, 4, 1):
            if x == 0:
                dic = get_nearby_places(str(float(latitude) + 2.0), longitude)
            if x == 1:
                dic = get_nearby_places(str(float(latitude) - 2.0), longitude)
            if x == 2:
                dic = get_nearby_places(latitude, str(float(longitude) - 2.0))
            if x == 3:
                dic = get_nearby_places(latitude, str(float(longitude) + 2.0))
            if len(dic["result"]) > 0:
                return Response(dic)
    return Response('Nothing found')  # enlarge the search


# get Spotify Ids
def get_spotify_id(artist):
    url = 'https://api.spotify.com/v1/search?query=' + artist + '&type=track'
    r = requests.get(url);
    # Problem if user asks again => gets the same uri
    try:
        # logger.error(r.json()["tracks"]["items"][0]["uri"])
        return {'continueSearching': False, 'result': r.json()["tracks"]["items"][0]["uri"]}
    except:
        return {'continueSearching': True, 'result': ""}


# get artists for city
def get_artist_for_city(location):
    serializer = LocationSerializer(location)
    dbdic = load_artists_from_data_base(location)
    # no db entries, load from web
    if dbdic['dbEntries']:
        # logger.error('loadedFromDB')
        return {'continueSearching': dbdic['continueSearching'], 'result': dbdic['result']}
        # here could some background data collection be done with Celery
    else:
        # logger.error('load artists from api')
        # city="San Francisco" #dummyData
        city = location.name
        # improvement idea => ask for multiple cities at one time with or
        url = 'http://musicbrainz.org/ws/2/artist/?query=beginarea:' + city + '%20OR%20area:' + city + '%20OR%20endarea:' + city + '&limit=100'
        r = requests.get(url)
        dom = parseString(r.text)
        list_results = []
        # logger.error(dom2.toxml())
        # go through the artists
        for node in dom.getElementsByTagName('artist'):  # visit every node with the tag "artist"
            dic = get_spotify_id(node.firstChild.firstChild.nodeValue)
            # found spotify uri for artist
            if not dic["continueSearching"]:
                artist_name = node.firstChild.firstChild.nodeValue
                list_results.append({'uri': dic["result"], 'location': serializer.data, 'artist': artist_name})
                try:
                    location.save()
                    # location is already stored in database (exception because of unique identifier)
                except:
                    # logger.error('location already stored')
                    location = Location.objects.get(name=location.name, countryCode=location.countryCode)
                    spotify = SpotifyData(uri=dic["result"])
                    artist = Artist(name=artist_name)
                    # get_or_create: useful
                    spotify.save()
                    artist.spotifyUri = spotify
                    artist.save()
                    artist.location.add(location)
                    # for update
                    artist.save()

                    # stop searching and return result
                    if len(list_results) > 5:
                        return {'continueSearching': False, 'result': list_results}

          # found nothing less than x results => continue searching for another type
        return {'continueSearching': True, 'result': list_results}


def load_artists_from_data_base(location):
    serializer = LocationSerializer(location)
    db_list = []
    # check if there are any entries for a location in database
    try:
        # raises exception if it returns multiple values or none Element
        location_entry = Location.objects.get(name=location.name, countryCode=location.countryCode)
        # get artists connected with this article
        artist = Artist.objects.filter(location=location_entry)
        # logger.error(artist)
        for a in artist:
            # logger.error(a.name)
            spotify_data = SpotifyData.objects.filter(artist=a)
            for s in spotify_data:
                # logger.error(s.uri)
                db_list.append({'uri': s.uri, 'location': serializer.data, 'artist': a.name})
        # exit search if list size is bigger than 5
        return {'dbEntries': True, 'continueSearching': (not len(db_list) > 5), 'result': db_list}
    except Location.DoesNotExist:
        return {'dbEntries': False, 'continueSearching': True, 'result': db_list}


# get nearbyPlaces using the geonames api
def get_nearby_places(latitude, longitude):

    request = 'http://api.geonames.org/findNearbyPlaceNameJSON?lat={}&lng={}&radius=300&maxRow=15&cities=cities15000&username={}'.format(latitude, longitude, load_geo_username())
    google_url = "https://maps.googleapis.com/maps/api/geocode/json?latlng=40.714224,-73.961452&key=API_KEY"
    response = urllib.request.urlopen(request)
    data = json.loads(response.read().decode("utf-8"))
    list_results = []
    for num in range(0, len(data["geonames"])):
        da = data["geonames"][num]
        # data["geonames"][num]["toponymName"] contains the city name
        location = Location(name=da["toponymName"], countryName=da["countryName"], countryCode=da["countryCode"],
                            latitude=da["lat"], longitude=da["lng"])
        # location.save() don't save location here, just save locations with spotify tracks connected
        dic = get_artist_for_city(location)
        if not dic["continueSearching"] or (len(list_results) + len(dic["result"])) > 5:
            list_results.extend(dic["result"])
            # stop searching and return result immediatly (interrupt for-loop)
            return {'result': list_results}
    return {'result': list_results}

# get Username for Geo Api that is is not visible on gitHub

def load_geo_username():
    username = os.environ.get('GEONAMES_USERNAME', False)
    try:
        if not username:
            with open("username.txt", "r") as my_file:
                username = my_file.read()
    except FileNotFoundError:
        return "scriptkiddi"

    return username
