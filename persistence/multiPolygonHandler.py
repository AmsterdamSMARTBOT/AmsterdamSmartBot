'''
Created on 06 giu 2017

@author: ROCCO - GERARDO
'''

from bot.models import MultiPolygon
from django.contrib.gis.geos import Point

def createMultiPolygon(name, polygon, prices):
    multiPolygon = MultiPolygon()
    multiPolygon.name = name
    multiPolygon.poly = polygon
    multiPolygon.description = prices  
    multiPolygon.save()
    
def getMultiPolygon(name):
    multiPolygon = MultiPolygon.objects.get(name=name)
    return multiPolygon

def getMultiPolygonByPoint(point):
    obj  = MultiPolygon.objects.filter(poly__intersects=point)
    return obj

def getAllMultiPolygon():
    obj  = MultiPolygon.objects.filter()
    return obj