__author__ = 'larissa'

from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url
from .views import getArtistList

urlpatterns = format_suffix_patterns([
    url(r'^lat/(?P<latitude>(-?\d+\.\d+))/long/(?P<longitude>(-?\d+\.\d+))/$', getArtistList),
])
