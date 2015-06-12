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
from django.contrib.gis.measure import D
from django.contrib.gis.geos import GEOSGeometry
import musicbrainzngs
logger = logging.getLogger(__name__)
from track.models import Track
# Create your views here.

# Create your views here.
@api_view(['GET'])
def get_spotify_uris(request, latitude=1, longitude=1, format=None):
    point = GEOSGeometry('POINT({} {})'.format(latitude, longitude))
    radius = 10
    results = []
    while len(results) < 5:
        locations = Location.objects.filter(geom__distance_lte=(point, D(km=radius))).order_by('-population')[:5]
        for location in locations:
            results += Track.objects.filter(artist__location=location)
            if len(results) > 5:
                break
            get_artists_for_city(location)

        radius += 10
    response = []
    for track in results:
        response.append({"name": track.name, "artist": track.artist.name, "uri": track.spotify_uri.uri})
    return Response(response)


def get_tracks_for_artist(artist):

    url = 'https://api.spotify.com/v1/artists/{}/top-tracks?country=De'.format(artist.spotifyUri.uri[15:])
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        r = r.json()
        track_list = r.get('tracks')
        for track in track_list:
            uri = SpotifyData(uri=track.get('uri'))
            uri.save()
            t = Track(name=track.get('name'), artist=artist, spotify_uri=uri)
            t.save()

    #TODO error handeling


def get_spotify_artists_for_name(artist_name):
    url = 'https://api.spotify.com/v1/search?q={}&type=artist&limit=5'.format(artist_name)
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        r = r.json()
        return r.get('artists').get('items')


# get artists for city
def get_artists_for_city(location):
    #TODO add celery here
    city = location.name
    musicbrainzngs.set_useragent("CultureRadio", 1)
    response = musicbrainzngs.search_artists(area=city, beginarea=city, endarea=city)
    response_artist_list = response.get('artist-list')
    for artist in response_artist_list:
        spotify_artists = get_spotify_artists_for_name(artist.get('name'))
        if len(spotify_artists) == 0:
            continue
        for spotify_artist in spotify_artists:
            uri, created = SpotifyData.objects.get_or_create(uri=spotify_artist.get('uri'))
            uri.save()
            a, created = Artist.objects.get_or_create(name=spotify_artist.get('name'), spotifyUri=uri)
            a.location.add(location)
            a.save()
            get_tracks_for_artist(a)

