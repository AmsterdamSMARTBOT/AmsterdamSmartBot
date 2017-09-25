'''
Created on 06 giu 2017

@author: ROCCO - GERARDO
'''

import json
import urllib.request
from django.contrib.gis.geos import GEOSGeometry
import numpy as np
from bot.models import MultiPolygon, ParkingZone
from persistence import multiPolygonHandler, parkingZoneHandler, timeSlotHandler

#the method loads the datas from the JSON regarding the shapes of the parking zones
def loadJSON():
    urld = 'https://amsterdam-maps.bma-collective.com/embed/parkeren/deploy_data/tarieven.json'
    r = urllib.request.urlopen(urld)
    data = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))
    geometryNames = []
    for singleData in data:
        geometryNames.append(singleData)
    data = convertData(data, geometryNames)
    tot = parkingZoneHandler.getNumberOfParkingZone()
    for name in geometryNames:
        pnt = GEOSGeometry(str(data[name]['location']))
        multiPolygonHandler.createMultiPolygon(name, pnt, 0)
        multiPolygon = multiPolygonHandler.getMultiPolygon(name)
        if tot == 0:
            extractCost(data[name]['tarieven'], multiPolygon)    

#the method parses the costs from JSON flow
def extractCost(data, multiPolygon):

    for d in data:
        print(str(d))
        if str(d) == '0' or str(d) == '60' or str(d) == '120' or str(d) == '180' or str(d) == '240':
            prezzi = data[d]
            for key1 in prezzi:
                parkingZone = ParkingZone()
                parkingZone.price = str(key1)
                parkingZone.maxHours = str(d)
                parkingZone.multi_polygon = multiPolygon
                parkingZoneHandler.saveParking(parkingZone)
                giorni = prezzi[key1]
                for key2 in giorni:
                    timeSlotHandler.createTimeSlot(str(key2), str(giorni[key2]), parkingZone)
        else:
            for key1 in d:
                parkingZone = ParkingZone()
                parkingZone.price = str(key1)
                parkingZone.maxHours = 0
                parkingZone.multi_polygon = multiPolygon
                parkingZoneHandler.saveParking(parkingZone)
                giorni = d[key1]
                for key2 in giorni:
                    timeSlotHandler.createTimeSlot(str(key2), str(giorni[key2]), parkingZone)

#the method converts the strings contained in the JSON to floats    
def convertData(data, geometryNames):
    i = 0
    for name in geometryNames:
        i = i + 1
        j = 0
        for subArray in data[name]['location']['coordinates']:
            arrayToModify = data[name]['location']['coordinates'][j][0]
            x = np.array(arrayToModify)
            y = x.astype(np.float)
            y = np.array(y).tolist()
            data[name]['location']['coordinates'][j][0] = y
            j = j + 1 
    return data