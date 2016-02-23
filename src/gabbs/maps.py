# -*- coding: utf-8 -*-
"""

maps.py  -  main api file for geohub maps

======================================================================
AUTHOR:  Wei Wan, Purdue University

EMAIL:   rcac-help@purdue.edu

Copyright (c) 2016  Purdue University

See the file "license.terms" for information on usage and
redistribution of this file, and for a DISCLAIMER OF ALL WARRANTIES.

======================================================================
"""

from qgis.core import *
from qgis.gui import *
from gabbs.basic.MapCanvas import MapCanvas
from gabbs.basic.MapConfig import MapConfig
from gabbs.layers.Map import Map
from gabbs.layers.Layer import Layer
from gabbs.layers.Overlay import (Vector,
                                  Raster,
                                  DelimitedText)
from gabbs.events.MapEvent import (addListener,
                                   addAction)
from gabbs.gui.MapContainer import MapContainer
from gabbs.tools.ServerThread import ServerThread
from gabbs.MapUtils import *

""" Api functions
"""
def getLayerNames():
    names = []
    layers = QgsMapLayerRegistry.instance().mapLayers()
    for name, layer in layers.iteritems():
        names.append(layer.name())
    return names

def getLayerIds():
    ids = []
    layers = QgsMapLayerRegistry.instance().mapLayers()
    for name, layer in layers.iteritems():
        ids.append(layer.id())
    return ids

def setCurrentLayer(layerId):
    layer = QgsMapLayerRegistry.instance().mapLayer(layerId)
    iface.mapCanvas.setCurrentLayer(layer)

""" Public Api functions
"""
def gbsLoadLibrary():
    # Environment variable QGISHOME must be set to the install directory
    # before running the application
    qgis_prefix = "/usr" #os.getenv("QGISHOME")
    QgsApplication.setPrefixPath(qgis_prefix, True)
    QgsApplication.initQgis()

def gbsUnloadLibrary():
    # Exit
    QgsApplication.exitQgis()

def gbsGetSelectedAttributes():
    """ Get features from selection
    """
    layer = iface.mapCanvas.currentLayer()
    if not layer or layer.type() != QgsMapLayer.VectorLayer:
        return None
    attributesAll = []
    for f in layer.selectedFeatures():
        attrs = []
        for attr in f.attributes():
            attrs.append(str(attr.toString()))
        attributesAll.append(attrs)
    return attributesAll

def gbsGetSelectedBounds():
    """ Get bonding box of features from selection
    """
    clayer = iface.mapCanvas.currentLayer()
    if not clayer or clayer.type() != QgsMapLayer.VectorLayer:
        return None

    box = clayer.boundingBoxOfSelected()
    return box.toRectF()

def gbsGetDrawingBounds():
    """ Get bonding box of Drawing
    """
    box = QRectF()
    plugins = iface.mapContainer.plugins
    if 'drawingtool' in plugins:
        box = plugins["drawingtool"].tool.getBoundingBox()
    return box

def gbsRemoveLayer(mapLayer):
    """ Remove layer by map object name
    """
    if not mapLayer or mapLayer.getLayer() is None:
        return
    layerId = mapLayer.getLayer().id()
    iface.mapLegend.removeLayer(layerId)

def gbsRemoveLayerById(layerId):
    """ Remove layer by id
    """
    iface.mapLegend.removeLayer(layerId)

def gbsHideLayer(mapLayer):
    """ Hide layer by map object name
    """
    if not mapLayer or mapLayer.getLayer() is None:
        return
    layerId = mapLayer.getLayer().id()
    iface.mapLegend.hideLayer(layerId)

def gbsShowLayer(mapLayer):
    """ Show layer by map object name
    """
    if not mapLayer or mapLayer.getLayer() is None:
        return
    layerId = mapLayer.getLayer().id()
    iface.mapLegend.showLayer(layerId)