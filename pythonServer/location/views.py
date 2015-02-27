from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from artist.models import Artist
from artist.serializers import ArtistSerializer




# Create your views here.

# Create your views here.
@api_view(['GET'])
def getArtistList(request,latitude=1,longitude=1, format=None):
     artists = Artist.objects.all()
     serializer = ArtistSerializer(artists, many = True)
     return Response(serializer.data)

