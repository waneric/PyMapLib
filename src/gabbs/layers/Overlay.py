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
    def __init__(self, vectorFilePath, name = None, provider=None, option=None):
        Layer.__init__(self)
        self.option = option
        self.layer = self.createLayer(vectorFilePath, name, provider)
        self.setLayerProperty(self.option)
        self.setAddLayerCallback(self.addVectorLayerCallback)

    def createLayer(self, vectorFilePath, vectorName, provider):
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

        if provider == None or provider == "ogr":
            layer = QgsVectorLayer(fileName, layerName, "ogr")
        elif provider == "WFS":
            layer = QgsVectorLayer(fileName, layerName, "WFS")
        else:
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
            self.layer.toggleScaleBasedVisibility(True)
            self.layer.setMaximumScale(self.getScale(option["customScale"][0]) + 1)
            self.layer.setMinimumScale(self.getScale(option["customScale"][1]) - 1)



    def addVectorLayerCallback(self):
        # Set active layer
        #iface.mapCanvas.setCurrentLayer(self.layer)
        pass

class Raster(Layer):
    def __init__(self, rasterFilePath, name = None, option = None):
        Layer.__init__(self)
        self.option = option
        self.layer = self.createLayer(rasterFilePath, name)
        self.setLayerProperty(self.option)
        self.setAddLayerCallback(self.addRasterLayerCallback)

    def createLayer(self, rasterFilePath, rasterName):
        # if 'fileName' in self.option:
        #     fileName = self.option['fileName']
        # else:
        #     return None
        # if 'layerName' in self.option:
        #     layerName = self.option['layerName']
        # else:
        #     layerName = fileName.lower().replace("_", " ")
        # layer = QgsRasterLayer(fileName, layerName)

        if rasterFilePath == None or rasterFilePath == "":
            return None
        else:
            fileName = rasterFilePath

        if rasterName == None or rasterName == "":
            layerName = rasterFilePath.lower().replace("_", " ")
        else:
            layerName = rasterName

        layer = QgsRasterLayer(fileName, layerName)

        #layer.setCrs(QgsCoordinateReferenceSystem(3857, QgsCoordinateReferenceSystem.EpsgCrsId))
        self.layerName = layerName
        return layer

    def setCustomStyle(self, filePath):
        """ Beautify layer with custom style
        """
        res = self.loadStyleFile(filePath)
        return

    def setCustomScale(self, scaleRange):
        """ Set visible zoom range of the layer e.g. scaleRange = [3,7]
        """
        self.layer.toggleScaleBasedVisibility(True)
        self.layer.setMaximumScale(self.getScale(scaleRange[0]) + 1)
        self.layer.setMinimumScale(self.getScale(scaleRange[1]) - 1)
        return

    def setLayerProperty(self, option):
        """ Set options for the layer with specific properties
        """
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

        if "customScale" in option:
            self.layer.toggleScaleBasedVisibility(True)
            self.layer.setMaximumScale(self.getScale(option["customScale"][0]) + 1)
            self.layer.setMinimumScale(self.getScale(option["customScale"][1]) - 1)


    def addRasterLayerCallback(self):
        # Set active layer
        #iface.mapCanvas.setCurrentLayer(self.layer)
        pass

class DelimitedText(Layer):
    def __init__(self, dtFilePath, name = None, option = None):
        Layer.__init__(self)
        self.option = option
        self.layer = self.createLayer(dtFilePath, name)
        self.setLayerProperty(self.option)
        self.setAddLayerCallback(self.addDelimitedTextLayerCallback)

    def createLayer(self, dtFilePath, dtName):
        # if 'fileName' in self.option:
        #     fileName = self.option['fileName']
        # else:
        #     return None
        # if 'layerName' in self.option:
        #     layerName = self.option['layerName']
        # else:
        #     layerName = fileName.lower().replace("_", " ")

        if dtFilePath == None or dtFilePath == "":
            return None
        else:
            fileName = dtFilePath

        if dtName == None or dtName == "":
            layerName = dtFilePath.lower().replace("_", " ")
        else:
            layerName = dtName

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

    def setCustomStyle(self, filePath):
        """ Beautify layer with custom style
        """
        res = self.loadStyleFile(filePath)
        return

    def setCustomScale(self, scaleRange):
        """ Set visible zoom range of the layer e.g. scaleRange = [3,7]
        """
        self.layer.toggleScaleBasedVisibility(True)
        self.layer.setMaximumScale(self.getScale(scaleRange[0]) + 1)
        self.layer.setMinimumScale(self.getScale(scaleRange[1]) - 1)
        return

    def setLayerProperty(self, option):
        """ Set options for the layer with specific properties
        """
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

        if "customScale" in option:
            self.layer.toggleScaleBasedVisibility(True)
            self.layer.setMaximumScale(self.getScale(option["customScale"][0]) + 1)
            self.layer.setMinimumScale(self.getScale(option["customScale"][1]) - 1)

    def addDelimitedTextLayerCallback(self):
        # Set active layer
        #iface.mapCanvas.setCurrentLayer(self.layer)
        pass
