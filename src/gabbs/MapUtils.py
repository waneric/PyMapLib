# -*- coding: utf-8 -*-
"""

MapUtils.py  -  utilities fuctions for example program

======================================================================
AUTHOR:  Wei Wan, Purdue University

EMAIL:   rcac-help@purdue.edu

Copyright (c) 2016  Purdue University

See the file "license.terms" for information on usage and
redistribution of this file, and for a DISCLAIMER OF ALL WARRANTIES.

======================================================================
"""

#from PyQt4.QtCore import *
from PyQt4.QtGui import QColor
from qgis.core import *
from qgis.gui import *

class ReturnCode:
    SUCCESS = "SUCCESS"
    CREATE_LAYER_ERROR = "CREATE_LAYER_ERROR"
    ADD_LAYER_ERROR = "ADD_LAYER_ERROR"

class iface:
    '''Global class for interface to hold mapCanvas'''
    # Gui
    mainWindow = None
    mapCanvas = None
    mapContainer = None
    mapOverview = None
    mapToolBar = None
    mapLegend = None
    # Map zoom and cneter
    mapZoomScale = None
    mapCenterPoint = None

    @classmethod
    def getMainWindow(cls):
        return cls.mainWindow

    @classmethod
    def getMapCanvas(cls):
        return cls.mapCanvas

    @classmethod
    def legendInterface(cls):
        return cls.mapLegend

    @classmethod
    def addToolBarIcon(cls, action):
        cls.mapToolBar.addAction(action)

    @classmethod
    def removeToolBarIcon(cls, action):
        cls.mapToolBar.removeAction(action)

    @classmethod
    def addDockWidget(cls, dockWidgetArea, dockwidget):
        cls.mainWindow.addDockWidget(dockWidgetArea, dockwidget)

    @classmethod
    def removeDockWidget(cls, dockwidget):
        cls.mainWindow.removeDockWidget(dockwidget)

def debug_trace():
    '''set a tracepoint in the Python Debugger that works with Qt'''
    from PyQt4.QtCore import pyqtRemoveInputHook
    from pdb import set_trace
    pyqtRemoveInputHook()
    set_trace()