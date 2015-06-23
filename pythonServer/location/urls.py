__author__ = 'larissa'

from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url
from .views import get_spotify_uris

urlpatterns = format_suffix_patterns([
    url(r'^(?P<latitude>(-?\d+\.\d+))/(?P<longitude>(-?\d+\.\d+))/$', get_spotify_uris),
])
