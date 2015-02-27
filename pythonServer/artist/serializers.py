__author__ = 'larissa'

from rest_framework import serializers
from .models import Artist


class ArtistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Artist
        fields = ('name',) #that location and id is not shown