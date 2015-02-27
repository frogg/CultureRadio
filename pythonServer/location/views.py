from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response



# Create your views here.

# Create your views here.
@api_view(['GET'])
def test(request, format=None):
    content = {'artist': 'DJ Bobo'}
    return Response(content)
