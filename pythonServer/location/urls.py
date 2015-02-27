__author__ = 'larissa'

from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url
from .views import test

urlpatterns = format_suffix_patterns([
    url(r'^hallo/$', test, name='test'),

])
