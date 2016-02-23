# -*- coding: utf-8 -*-
"""

MapCanvas.py  -  canvas class for gabbs maps

======================================================================
AUTHOR:  Wei Wan, Purdue University

EMAIL:   rcac-help@purdue.edu

Copyright (c) 2016  Purdue University

See the file "license.terms" for information on usage and
redistribution of this file, and for a DISCLAIMER OF ALL WARRANTIES.

======================================================================
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

from gabbs.MapUtils import iface, debug_trace

class LayerControlStyle:
    SHOW = 'SHOW'     #displays a layer 
    HIDE = 'HIDE'     #displays no layer
    SHOW_PROPERTY = 'SHOW_PROPERTY'     #displays a layer property
    HIDE_PROPERTY = 'HIDE_PROPERTY'     #displays no layer property
    DEFAULT = 'DEFAULT' #display a layer property

class PanControlStyle:
    SMALL = 'SMALL'     #displays a mini-pan control (only pan)
    LARGE = 'LARGE'     #displays the standard select control
    DEFAULT = 'DEFAULT' #picks the best select control based on device and map size
    HORIZONTAL_BAR = 'HORIZONTAL_BAR' #display one button for each map type
    DROPDOWN_MENU = 'DROPDOWN_MENU'   #select map type via a dropdown menu

class ZoomControlStyle:
    SMALL = 'SMALL'     #displays a mini-zoom control (only + and - buttons)
    LARGE = 'LARGE'     #displays the standard zoom control
    DEFAULT = 'DEFAULT' #picks the best zoom control based on device and map size

class SelectControlStyle:
    SMALL = 'SMALL'     #displays a mini-select control (only select rectangle)
    LARGE = 'LARGE'     #displays the standard select control 
    DEFAULT = 'DEFAULT' #picks the best select control based on device and map size

class MapCanvas(QgsMapCanvas):
    def __init__(self):
        QgsMapCanvas.__init__(self)
        self.overlayTextEnabled = False
        self.overlayText = QString()
        self.overlayTextXOffset = 0
        self.overlayTextYOffset = 0
        self.overlayImageEnabled = False
        self.overlayImage = QImage()
        self.overlayImageXOffset = 0
        self.overlayImageYOffset = 0

    def drawForeground(self, painter, rect):
        '''Default method override to draw
        '''
        result = QGraphicsView.drawForeground(self, painter, rect)

        overlayRect = self.sceneRect()
          # draw Overlay Text 
        if self.overlayTextEnabled:
            painter.setBackgroundMode(Qt.OpaqueMode)
            painter.setBackground(QColor(255, 255, 255))
            painter.setOpacity(0.5)
            x = overlayRect.right() - self.overlayTextXOffset
            y = overlayRect.bottom() - self.overlayTextYOffset
            painter.drawText(QPointF(x, y), self.overlayText)
        # draw Overlay Image
        if self.overlayTextEnabled:
            painter.setOpacity(1.0)
            x = overlayRect.left() + self.overlayImageXOffset
            y = overlayRect.bottom() - self.overlayImageYOffset
            painter.drawImage(QPointF(x, y), self.overlayImage)

        return result
  
    def setOverlayText(self, text, x, y):
        self.overlayText = QString(text)
        self.overlayTextXOffset = x
        self.overlayTextYOffset = y
        self.overlayTextEnabled = True

    def setOverlayImage(self, image, x, y):
        self.overlayImage = QImage(image)
        self.overlayImageXOffset = x
        self.overlayImageYOffset = y
        self.overlayImageEnabled = True


