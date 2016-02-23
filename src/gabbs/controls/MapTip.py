# -*- coding: utf-8 -*-
"""

MapTip.py  -  map tool for show user defined map tips

======================================================================
AUTHOR:  Wei Wan, Purdue University

EMAIL:   rcac-help@purdue.edu

Copyright (c) 2016  Purdue University

See the file "license.terms" for information on usage and
redistribution of this file, and for a DISCLAIMER OF ALL WARRANTIES.

======================================================================

"""

from PyQt4.QtCore import *
#from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

from gabbs.MapUtils import iface, debug_trace


class MapTip(object):
    '''
    Base class for the map select tools
    '''
    def __init__(self):
        object.__init__(self)
        self.canvas = iface.mapCanvas
        self.mapTip = None
        self.timerMapTips = None
        self.createMapTips()

    def createMapTips( self ):
        """ Create MapTips on the map """
        self.timerMapTips = QTimer( self.canvas )
        self.mapTip = QgsMapTip()

    def turnOnMapTips(self):
        QObject.connect(self.canvas, SIGNAL( "xyCoordinates(const QgsPoint&)" ),
                        self.mapTipXYChanged)
        QObject.connect(self.timerMapTips, SIGNAL( "timeout()" ),
                        self.showMapTip)

    def turnOffMapTips(self):
        QObject.disconnect(self.canvas, SIGNAL( "xyCoordinates(const QgsPoint&)" ),
                           self.mapTipXYChanged)
        QObject.disconnect(self.timerMapTips, SIGNAL( "timeout()" ),
                           self.showMapTip)

    def mapTipXYChanged(self, p):
        """ SLOT. Initialize the Timer to show MapTips on the map """
        if self.canvas.underMouse(): # Only if mouse is over the map
            # Here you could check if your custom MapTips button is active or sth
            self.lastMapPosition = QgsPoint(p.x(), p.y())
            self.mapTip.clear(self.canvas)
            self.timerMapTips.start(750) # time in milliseconds

    def showMapTip(self):
        """ SLOT. Show  MapTips on the map """
        self.timerMapTips.stop()
        layer = self.canvas.currentLayer()
        if not layer:
            return
        if self.canvas.underMouse(): 
            # Here you could check if your custom MapTips button is active or sth
            pointQgs = self.lastMapPosition
            pointQt = self.canvas.mouseLastXY()
            self.mapTip.showMapTip(layer, pointQgs, pointQt, self.canvas)