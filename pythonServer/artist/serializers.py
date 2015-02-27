__author__ = 'larissa'

from rest_framework import serializers
from .models import Artist


class ArtistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Artist
        fields = ('spotifyUri',) #that location,id, and name is not shown