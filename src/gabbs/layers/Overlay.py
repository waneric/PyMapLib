# -*- coding: utf-8 -*-
"""

Overlay.py  -  overlay file for geohub maps

======================================================================
AUTHOR:  Wei Wan, Purdue University

EMAIL:   rcac-help@purdue.edu

Copyright (c) 2016  Purdue University

See the file "license.terms" for information on usage and
redistribution of this file, and for a DISCLAIMER OF ALL WARRANTIES.

======================================================================

"""
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from osgeo import gdal

from gabbs.layers.Layer import Layer
from gabbs.layers.LayerProperty import *
from gabbs.MapUtils import iface, debug_trace
import gabbs.MapUtils as MapUtils


class Vector(Layer):
    def __init__(self, vectorFilePath, vectorName = None, option=None):
        Layer.__init__(self)
        self.option = option
        self.layer = self.createLayer(vectorFilePath, vectorName)
        self.setLayerProperty(self.option)
        self.setAddLayerCallback(self.addVectorLayerCallback)

    def createLayer(self, vectorFilePath, vectorName):
        # if 'fileName' in self.option:
        #     fileName = self.option['fileName']
        # else:
        #     return None
        # if 'layerName' in self.option:
        #     layerName = self.option['layerName']
        # else:
        #     layerName = fileName.lower().replace("_", " ")
        # layer = QgsVectorLayer(fileName, layerName, "ogr")

        if vectorFilePath == None or vectorFilePath == "":
            return None
        else:
            fileName = vectorFilePath

        if vectorName == None or vectorName == "":
            layerName = vectorFilePath.lower().replace("_", " ")
        else:
            layerName = vectorName

        layer = QgsVectorLayer(fileName, layerName, "ogr")
        #layer.setCrs(QgsCoordinateReferenceSystem(3857, QgsCoordinateReferenceSystem.EpsgCrsId))
        self.layerName = layerName
        return layer

    def setCustomStyle(self, filePath):
        res = self.loadStyleFile(filePath)
        return

    def setCustomScale(self, scaleRange):
        self.layer.toggleScaleBasedVisibility(True)
        self.layer.setMaximumScale(self.getScale(scaleRange[0]) + 1)
        self.layer.setMinimumScale(self.getScale(scaleRange[1]) - 1)   
        return

    def setLayerProperty(self, option):

        if option == None:

            return

        if 'attribution' in option:
             attribution = option['attribution']
             self.layer.setAttribution(QString(attribution))

        if "useSystemStyle" in option:
            if option['useSystemStyle'] == True:
                dirPath = os.path.join(os.path.dirname(__file__), '..', 'resources', 'style')
                filePath = os.path.join(dirPath, option['styleName'].lower() + '.qml')
                res = self.loadStyleFile(filePath)
        elif "useCostumStyle" in option:
            if option['useCostumStyle'] == True:
                filePath = option['styleFileName']
                res = self.loadStyleFile(filePath)
        elif "useSimpleStyle" in option:
            if option['useSimpleStyle'] == True:
                if "color" in option:
                    color = QColor(option["color"])
                    symbols = self.layer.rendererV2().symbols()
                    s = symbols[0]
                    s.setColor(color)

        if 'opacity' in option:
             opacity = option['opacity']
             if opacity >= 0 and opacity <= 1:
                 trans = (1 - opacity) * 100
                 self.layer.setLayerTransparency(trans)     

        if 'visible' in option:
            mapLayer = QgsMapLayerRegistry.instance().mapLayer(self.layer.id())
            if not mapLayer:
                return
            if option['visible'] == True:
                mapLayer.setVisible(True)
            elif option['visible'] == False:
                mapLayer.setVisible(False)

        if "customScale" in option:
            print "scale factor",
            print self.getScale(option["customScale"][1]),
            print "/",
            print self.getScale(option["customScale"][0])
            self.layer.toggleScaleBasedVisibility(True)
            self.layer.setMaximumScale(self.getScale(option["customScale"][0]) + 1)
            self.layer.setMinimumScale(self.getScale(option["customScale"][1]) - 1)   



    def addVectorLayerCallback(self):
        # Set active layer
        #iface.mapCanvas.setCurrentLayer(self.layer)
        pass

class Raster(Layer):
    def __init__(self, option):
        Layer.__init__(self)
        self.option = option
        self.layer = self.createLayer()
        self.setLayerProperty(self.option)
        self.setAddLayerCallback(self.addRasterLayerCallback)

    def createLayer(self):
        if 'fileName' in self.option:
            fileName = self.option['fileName']
        else:
            return None
        if 'layerName' in self.option:
            layerName = self.option['layerName']
        else:
            layerName = fileName.lower().replace("_", " ")
        layer = QgsRasterLayer(fileName, layerName)
        #layer.setCrs(QgsCoordinateReferenceSystem(3857, QgsCoordinateReferenceSystem.EpsgCrsId))
        self.layerName = layerName
        return layer

    def setLayerProperty(self, option):
        if 'attribution' in option:
             attribution = option['attribution']
             self.layer.setAttribution(QString(attribution))
        if "useSystemStyle" in option:
            if option['useSystemStyle'] == True:
                dirPath = os.path.join(os.path.dirname(__file__), '..', 'resources', 'style')
                filePath = os.path.join(dirPath, option['styleName'].lower() + '.qml')
                res = self.loadStyleFile(filePath)
                if res:
                    return
        elif "useCostumStyle" in option:
            if option['useCostumStyle'] == True:
                filePath = option['styleFileName']
                res = self.loadStyleFile(filePath)
                if res:
                    return
        if 'opacity' in option:
            opacity = option['opacity']
            if opacity >= 0 and opacity <= 1:
                opacity = float(opacity)
                self.layer.renderer().setOpacity(opacity)
        if "visible" in option:
            mapLayer = QgsMapLayerRegistry.instance().mapLayer(self.layer.id())
            if not mapLayer:
                return
            if option['visible'] == True:
                mapLayer.setVisible(True)
            elif option['visible'] == False:
                mapLayer.setVisible(False)

    def addRasterLayerCallback(self):
        # Set active layer
        #iface.mapCanvas.setCurrentLayer(self.layer)
        pass

class DelimitedText(Layer):
    def __init__(self, option):
        Layer.__init__(self)
        self.option = option
        self.layer = self.createLayer()
        self.setLayerProperty(self.option)
        self.setAddLayerCallback(self.addDelimitedTextLayerCallback)

    def createLayer(self):
        if 'fileName' in self.option:
            fileName = self.option['fileName']
        else:
            return None
        if 'layerName' in self.option:
            layerName = self.option['layerName']
        else:
            layerName = fileName.lower().replace("_", " ")
        de = ","
        x = "Longitude"
        y = "Latitude"
        if 'delimiter' in self.option:
            de = self.option['delimiter']
        if 'xField' in self.option:
            x = self.option['xField']
        if 'yField' in self.option:
            y = self.option['yField']
        #uri = "file:///" + fileName + "?crs=epsg:3857&delimiter=%s&xField=%s&yField=%s" % (",", "Longitude", "Latitude")
        uri = "file:///" + fileName + "?delimiter=%s&xField=%s&yField=%s" % (de, x, y)
        layer = QgsVectorLayer(uri, layerName, "delimitedtext")
        self.layerName = layerName
        return layer

    def setLayerProperty(self, option):
        if 'attribution' in option:
             attribution = option['attribution']
             self.layer.setAttribution(QString(attribution))
        if "useSystemStyle" in option:
            if option['useSystemStyle'] == True:
                dirPath = os.path.join(os.path.dirname(__file__), '..', 'resources', 'style')
                filePath = os.path.join(dirPath, option['styleName'].lower() + '.qml')
                res = self.loadStyleFile(filePath)
                if res:
                    return
        elif "useCostumStyle" in option:
            if option['useCostumStyle'] == True:
                filePath = option['styleFileName']
                res = self.loadStyleFile(filePath)
                if res:
                    return
        elif "useSimpleStyle" in option:
            if option['useSimpleStyle'] == True:
                if "color" in option:
                    color = QColor(option["color"])
                    symbols = self.layer.rendererV2().symbols()
                    s = symbols[0]
                    s.setColor(color)
        if 'opacity' in option:
            opacity = option['opacity']
            if opacity >= 0 and opacity <= 1:
                trans = (1 - opacity) * 100
                self.layer.setLayerTransparency(trans)
        if "visible" in option:
            mapLayer = QgsMapLayerRegistry.instance().mapLayer(self.layer.id())
            if not mapLayer:
                return
            if option['visible'] == True:
                mapLayer.setVisible(True)
            elif option['visible'] == False:
                mapLayer.setVisible(False)
        if 'attribution' in option:
             attribution = option['attribution']
             self.layer.setAttribution(QString(attribution))

    def addDelimitedTextLayerCallback(self):
        # Set active layer
        #iface.mapCanvas.setCurrentLayer(self.layer)
        pass