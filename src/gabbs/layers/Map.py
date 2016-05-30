# -*- coding: utf-8 -*-
"""

map.py  -  map layer file for gabbs maps

======================================================================
AUTHOR:  Wei Wan, Purdue University

EMAIL:   rcac-help@purdue.edu

Copyright (c) 2016  Purdue University

See the file "license.terms" for information on usage and
redistribution of this file, and for a DISCLAIMER OF ALL WARRANTIES.

======================================================================

"""

import os
import math
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

from gabbs.layers.Layer import Layer
from gabbs.layers.LayerProperty import *

import gabbs.resources_rc

from gabbs.MapUtils import iface, debug_trace

import os
import math
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

from gabbs.layers.Layer import Layer
from gabbs.layers.LayerProperty import *

import gabbs.resources_rc

from gabbs.MapUtils import iface, debug_trace

class Map(Layer):
    def __init__(self, mapName, layerOption = None):
        Layer.__init__(self)

        # default
        mapProp = {'center':
                      {'lon': -86.21,
                       'lat': 39.82},
                   'zoom':    6,
                   'maxZoom': 15,
                   'minZoom': 0,
                   'mapTypeId': 'OSM'}

        if layerOption == None:
            self.option = mapProp
        else:
            self.option = layerOption

        self.canvas = iface.mapCanvas
        self.window = iface.mainWindow
        
        if mapName == None or mapName == "":
            self.layerName = self.getMapLayerName()
        else:
            self.layerName = mapName
        
        self.layerTypeName = self.getLayerTypeName()
        self.layerTypeId = self.getLayerTypeId()
        self.mapTypeName = self.getMapTypeName()
        self.layer = self.createLayer()
        self.scale = MapScaleLevels(maxZoomlevel=15,
                                    minZoomlevel=0,
                                    dpi=self.window.physicalDpiX())
        self.centerPoint = self.getMapCenter()
        self.zoomScale = self.getMapScale()

        self.setLayerAttribution()
        self.setLayerAttributionIcon()

        self.setAddLayerCallback(self.addMapLayerCallback)

    def setMapZoom(self, zoom):
        
        zoomLevel = int(zoom)
        zoomScale = self.scale.getScale(zoomLevel)
        self.zoomScale = zoomScale

        iface.mapCanvas.zoomScale(self.zoomScale)
        iface.mapZoomScale = self.zoomScale
        
        return

    def setMapScale(self, minZoom = 0, maxZoom = 15):

        self.scale = MapScaleLevels(maxZoomlevel=int(maxZoom),
                                    minZoomlevel=int(minZoom),
                                    dpi=self.window.physicalDpiX())

        return

    def setMapCenter(self, lon, lat):

        center = None

        crsTransform = self.createCrsTransform()
        center = crsTransform.transform(QgsPoint(lon, lat), QgsCoordinateTransform.ForwardTransform)

        self.centerPoint = center

        iface.mapCanvas.setCenter(self.centerPoint)
        iface.mapCenterPoint = self.centerPoint

        return 


    def getMapLayerName(self, mapName):
        if 'layerName' in self.option:
            layerName = str(self.option['layerName'])
        elif 'mapTypeId' in self.option:
            layerName = self.option['mapTypeId'].lower().replace("_", " ")
        else:
           layerName = 'web layer'
        return layerName

    def getMapTypeName(self):
        typeName = ''
        if 'mapTypeId' in self.option:
            typeName = self.option['mapTypeId']
        else:
            typeName = 'OSM'
        return typeName

    def getLayerTypeName(self):
        return LayerTypeName.TMS

    def getLayerTypeId(self):
        return LayerTypeId.TMS

    def setLayerAttribution(self):
        if self.mapTypeName in (MapTypeName.GOOGLE_TERRAIN, 
                                MapTypeName.GOOGLE_ROADMAP,
                                MapTypeName.GOOGLE_HYBRID,
                                MapTypeName.GOOGLE_SATELLITE):
            attribution = u"Map data © 2015 Google"
            xOffset = 170
            yOffset = 16
        elif self.mapTypeName in (MapTypeName.OSM,
                                  MapTypeName.OCM,
                                  MapTypeName.OCM_LANDSCAPE,
                                  MapTypeName.OCM_TRANSPORT):
            attribution = u"© OpenStreetMap contributors"
            xOffset = 200
            yOffset = 16
        else:
            attribution = None
            return

        self.canvas.setOverlayText(attribution, xOffset, yOffset)

    def setLayerAttributionIcon(self):
        if self.mapTypeName in (MapTypeName.GOOGLE_TERRAIN, 
                                MapTypeName.GOOGLE_ROADMAP,
                                MapTypeName.GOOGLE_HYBRID,
                                MapTypeName.GOOGLE_SATELLITE):
            attributionIcon = QImage(':/gabbs/resources/img/google-logo.png')
            xOffset = 10
            yOffset = 32
        else:
            attributionIcon = None
            return

        self.canvas.setOverlayImage(attributionIcon, xOffset, yOffset)

    def gdalTMSConfig(self):
        if self.mapTypeName is not None:
            gdalTMS = self.mapTypeName.lower() + ".xml"
            # read GDAL TMS config from file
            path = os.path.join(os.path.dirname(__file__), 'gdal_tms', gdalTMS)
            return path
            """
            try:
                f = open(path, 'r')
                config = f.read()
            except:
                return None
            finally:
                f.close()
            return config
            """
        else:
            return None

    def createLayer(self):
        # create GDAL TMS layer with XML string as datasource
        if not self.layerName:
            return None
        cfg = self.gdalTMSConfig()
        if not cfg:
            return None
        layer = QgsRasterLayer(cfg, self.layerName)
        #layer.setAttribution(QString(self.layerAttribution))
        return layer

    def getMapScale(self):
        zoomScale = None
        if 'maxZoom' in self.option:
            zoomLevel = int(self.option['maxZoom'])
            self.scale.setMaxZoomlevel(zoomLevel)
        if 'minZoom' in self.option:
            zoomLevel = int(self.option['minZoom'])
            self.scale.setMinZoomlevel(zoomLevel)
        if 'zoom' in self.option:
            zoomLevel = int(self.option['zoom'])
            zoomScale = self.scale.getScale(zoomLevel)
        return zoomScale

    def createCrsTransform(self, srcCrsId=4326, destCrsId=3857):
        srcCrs = QgsCoordinateReferenceSystem()
        srcCrs.createFromString("EPSG:4326")
        destCrs = QgsCoordinateReferenceSystem()
        destCrs.createFromString("EPSG:3857")
        crsTransform = QgsCoordinateTransform(srcCrs, destCrs)
        return crsTransform

    def getMapCenter(self):
        lon = 0.0
        lat = 0.0
        centerPoint = None
        if 'center' in self.option:
            centerPoint = self.option['center']
            if 'lon' in centerPoint:
                lon = float(centerPoint['lon'])
            if 'lat' in centerPoint:
                lat = float(centerPoint['lat'])
            crsTransform = self.createCrsTransform()
            centerPoint = crsTransform.transform(QgsPoint(lon, lat), QgsCoordinateTransform.ForwardTransform)
        return centerPoint

    def addMapLayerCallback(self):
        # Set extent to the extent of our layer
        iface.mapCanvas.setExtent(self.layer.extent())
        # Scale the map
        if self.zoomScale:
            iface.mapCanvas.zoomScale(self.zoomScale)
            iface.mapZoomScale = self.zoomScale
        # Center the map
        if self.centerPoint:
            iface.mapCanvas.setCenter(self.centerPoint)
            iface.mapCenterPoint = self.centerPoint
        # Connet the slot for auto scale adjust to map level
        iface.mapCanvas.scaleChanged.connect(self.scaleChanged)

    def scaleChanged(self, scale):
        # print "scale chaned to",
        # print scale,
        # print "(",
        # print self.scale.getZoomlevel(scale),
        # print ")"

        scale = int(scale)            
        if scale not in self.scale.zoomlevels.values():
            zoomlevel = self.scale.getZoomlevel(scale)
            if zoomlevel <> None:
                newScale = self.scale.getScale(zoomlevel)
                if scale <> newScale:
                    ## Disconnect to prevent infinite scaling loop
                    self.canvas.scaleChanged.disconnect(self.scaleChanged)
                    self.canvas.zoomScale(newScale)
                    self.canvas.scaleChanged.connect(self.scaleChanged)

## @package TileMapScaleLevels
#       Sets the scale to levels according to the Tile Map Specification used by Google, Osm, etc.
#       get correct dpi by using self.iface.mainWindow().physicalDpiX()

class MapScaleLevels(object):
    def __init__(self, maxZoomlevel=18, minZoomlevel=0, dpi=96, tileSize=256, earthRadius=6378137):
        self.__dpi = dpi
        self.inchesPerMeter = 39.37
        self.maxScalePerPixel = 156543.04
        self.earthRadius = earthRadius
        self.tileSize = tileSize
        self.__maxZoomlevel = maxZoomlevel
        self.__minZoomlevel = minZoomlevel

        self.zoomlevels = {}
        self.calculateScaleStorage()

    def minZoomlevel(self):
        return self.__minZoomlevel
    def setMinZoomlevel(self, zoomlevel):
        self.__minZoomlevel = zoomlevel

    def maxZoomlevel(self):
        return self.__maxZoomlevel
    def setMaxZoomlevel(self, zoomlevel):
        self.__maxZoomlevel = zoomlevel

    def dpi(self):
        return self.__dpi
    def setDpi(self, dpi):
        self.__dpi = dpi

    def getScale(self, zoomlevel):
        try:
            zoomlevel = int(zoomlevel)
            scale = (self.dpi() * self.inchesPerMeter * self.maxScalePerPixel) / (math.pow(2, zoomlevel))
            scale = int(scale)
            return scale
        except TypeError:
            raise
            #pass
        except Exception as e:
            raise e

    def getZoomlevel(self, scale):
        if scale <> 0:
            zoomlevel = int(round(math.log( ((self.dpi() * self.inchesPerMeter * self.maxScalePerPixel) / scale), 2 ), 0))
            if zoomlevel > self.maxZoomlevel():
                return self.maxZoomlevel()
            elif zoomlevel <= self.minZoomlevel():
                return self.minZoomlevel()
            else:
                return zoomlevel

    def mapWidth(self, zoomlevel):
        return self.tileSize * math.pow(2, zoomlevel)

    def pixelSize(self, zoomlevel):
        return 2.0 * math.pi * self.earthRadius / self.mapWidth(zoomlevel)

    def calculateScaleStorage(self):
        for zoomlevel in xrange(self.minZoomlevel(), self.maxZoomlevel()):
            self.zoomlevels[zoomlevel] = self.getScale(zoomlevel)