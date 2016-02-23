# -*- coding: utf-8 -*-
"""

Layer.py  -  base layer for gabbs maps

======================================================================
AUTHOR:  Wei Wan, Purdue University

EMAIL:   rcac-help@purdue.edu

Copyright (c) 2016  Purdue University

See the file "license.terms" for information on usage and
redistribution of this file, and for a DISCLAIMER OF ALL WARRANTIES.

======================================================================

"""

from os.path import isfile
from PyQt4.QtGui import QAction, QIcon
from qgis.gui import *
from gabbs.layers.LayerProperty import *
from gabbs.MapUtils import iface, debug_trace

class Layer(object):
    """Base class for layers"""
    layerName = None
    """Layer type name in menu"""
    layerIcon = None
    """Group icon in menu"""
    layerTypeName = None
    """Layer type identificator used to store in project"""
    layerTypeId = None
    """Numerical ID used in versions < 2.3"""
    layerId = None
    """Store 2 qgis objects"""
    layer = None
    layerAction = None

    layerAttribution = None

    def __init__(self):
        object.__init__(self)

    def getLayer(self):
        return self.layer

    def getLayerId(self):
        return self.layerId

    def setAddLayerCallback(self, addLayerCallback):
        """Set post processing in add layer method in canvas class
        """
        self.addLayerCallback = addLayerCallback

    def loadStyleFile(self, symPath):
        if isfile(symPath):
            res = self.layer.loadNamedStyle(symPath)
            if res[1]:
                return True
            else:
                return False
        else:
            return False