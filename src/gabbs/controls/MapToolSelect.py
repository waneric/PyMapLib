# -*- coding: utf-8 -*-

"""
MapToolSelect.py  -  map tool for selecting features

======================================================================
AUTHOR:  Wei Wan, Purdue University

EMAIL:   rcac-help@purdue.edu

Copyright (c) 2016  Purdue University

See the file "license.terms" for information on usage and
redistribution of this file, and for a DISCLAIMER OF ALL WARRANTIES.

======================================================================

"""
import math
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

import MapToolSelectUtils
from gabbs.MapUtils import iface, debug_trace

class MapToolSelectSingle(QgsMapTool):
    '''
    Base class for the map select tools
    '''
    def __init__(self, canvas):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.rubberBand = None
        self.cursor = QCursor(Qt.ArrowCursor)
        self.fillColor = QColor(254, 178, 76, 63)
        self.borderColour = QColor(254, 58, 29, 100)

    # Override events
    def canvasReleaseEvent(self, event):
        vlayer = MapToolSelectUtils.getCurrentVectorLayer(self.canvas)
        if vlayer == None:
            return
        self.rubberBand = QgsRubberBand(self.canvas, QGis.Polygon)
        self.rubberBand.setFillColor(self.fillColor)
        self.rubberBand.setBorderColor(self.borderColour)
        selectRect = QRect(0, 0, 0, 0)

        MapToolSelectUtils.expandSelectRectangle(selectRect, vlayer, event.pos())
        MapToolSelectUtils.setRubberBand(self.canvas, selectRect, self.rubberBand)
        selectGeom = self.rubberBand.asGeometry()

        if (event.modifiers() & Qt.ControlModifier):
            doDifference = True
        else:
            doDifference = False
        MapToolSelectUtils.setSelectFeatures(self.canvas, selectGeom, False, doDifference, True)
        self.rubberBand.reset(QGis.Polygon)

class MapToolSelectRectangle(QgsMapTool):
    '''
    Base class for the map select tool by rectangle
    '''
    def __init__(self, canvas):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.selectRect = QRect()
        self.rubberBand = None
        self.dragging = False
        self.cursor = QCursor(Qt.ArrowCursor)
        self.fillColor = QColor(254, 178, 76, 63)
        self.borderColour = QColor(254, 58, 29, 100)

    '''reimplement of the events
    '''
    def canvasPressEvent(self, event):
        self.selectRect.setRect(0, 0, 0, 0)
        self.rubberBand = None
        self.rubberBand = QgsRubberBand(self.canvas, QGis.Polygon)
        self.rubberBand.setFillColor(self.fillColor)
        self.rubberBand.setBorderColor(self.borderColour)

    def canvasMoveEvent(self, event):
        if event.buttons() != Qt.LeftButton:
            return

        if not self.dragging:
            self.dragging = True
            self.selectRect.setTopLeft(event.pos())
        self.selectRect.setBottomRight(event.pos())
        MapToolSelectUtils.setRubberBand(self.canvas, self.selectRect, self.rubberBand)

    def canvasReleaseEvent(self, event):
        vlayer = MapToolSelectUtils.getCurrentVectorLayer(self.canvas)
        if vlayer == None:
            self.rubberBand.reset(QGis.Polygon)
            self.rubberBand = None
            self.dragging = False
            return

        #if the user simply clicked without dragging a rect
        #we will fabricate a small 1x1 pix rect and then continue
        #as if they had dragged a rect
        if not self.dragging:
            MapToolSelectUtils.expandSelectRectangle(self.selectRect, vlayer, event.pos())
        else:
        #Set valid values for rectangle's width and height
            if self.selectRect.width() == 1:
                self.selectRect.setLeft(self.selectRect.left() + 1)
            if self.selectRect.height() == 1:
                self.selectRect.setBottom(self.selectRect.bottom() + 1)

        if self.rubberBand:
            MapToolSelectUtils.setRubberBand(self.canvas, self.selectRect, self.rubberBand)
            selectGeom = self.rubberBand.asGeometry()

            if not self.dragging:
                if event.modifiers() & Qt.ControlModifier:
                    doDifference = True
                else:
                    doDifference = False
                MapToolSelectUtils.setSelectFeatures(self.canvas, selectGeom, False, doDifference, True)
            else:
                MapToolSelectUtils.setSelectFeaturesEvent(self.canvas, selectGeom, event)

            selectGeom = None
            self.rubberBand.reset(QGis.Polygon)
            self.rubberBand = None

        self.dragging = False

class MapToolSelectPolygon(QgsMapTool):
    '''
    Class for the map select tools by polygon
    '''
    def __init__(self, canvas):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.rubberBand = None
        self.cursor = QCursor(Qt.ArrowCursor)
        self.fillColor = QColor(254, 178, 76, 63)
        self.borderColour = QColor(254, 58, 29, 100)

    # Events
    def canvasPressEvent(self, event):
        if self.rubberBand == None:
            self.rubberBand = QgsRubberBand(self.canvas, QGis.Polygon)
            self.rubberBand.setFillColor(self.fillColor)
            self.rubberBand.setBorderColor(self.borderColour)

        if event.button() == Qt.LeftButton:
            self.rubberBand.addPoint(self.toMapCoordinates(event.pos()))
        else:
            if self.rubberBand.numberOfVertices() > 2:
                polygonGeom = QgsGeometry(self.rubberBand.asGeometry())
                MapToolSelectUtils.setSelectFeaturesEvent(self.canvas, polygonGeom, event)
            self.rubberBand.reset(QGis.Polygon)
            self.rubberBand = None

    def canvasMoveEvent(self, event):
        if self.rubberBand == None:
            return

        if self.rubberBand.numberOfVertices() > 0:
            self.rubberBand.removeLastPoint(0)
            self.rubberBand.addPoint(self.toMapCoordinates(event.pos()))

class MapToolSelectFreehand(QgsMapTool):
    '''
    Class for the map select tool by freehand
    '''
    def __init__(self, canvas):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.rubberBand = None
        self.dragging = False
        self.cursor = QCursor(Qt.ArrowCursor)
        self.fillColor = QColor(254, 178, 76, 63)
        self.borderColour = QColor(254, 58, 29, 100)

    '''reimplement of the events
    '''
    def canvasPressEvent(self, event):
        if event.button() != Qt.LeftButton:
            return
        if self.rubberBand == None:
            self.rubberBand = QgsRubberBand(self.canvas, QGis.Polygon )
            self.rubberBand.setFillColor(self.fillColor)
            self.rubberBand.setBorderColor(self.borderColour)
        self.rubberBand.addPoint(self.toMapCoordinates(event.pos()))
        self.dragging = True

    def canvasMoveEvent(self, event):
        if not self.dragging or self.rubberBand == None:
            return
        self.rubberBand.addPoint(self.toMapCoordinates(event.pos()))

    def canvasReleaseEvent(self, event):
        if self.rubberBand == None:
            return
        if self.rubberBand.numberOfVertices() > 2:
            shapeGeom = self.rubberBand.asGeometry()
            MapToolSelectUtils.setSelectFeaturesEvent(self.canvas, shapeGeom, event)
        self.rubberBand.reset(QGis.Polygon)
        self.rubberBand = None
        self.dragging = False


M_PI = 3.1415926535897931159979634685
RADIUS_SEGMENTS = 40

class MapToolSelectRadius(QgsMapTool):
    '''
    Class for the map select tool by radius
    '''
    def __init__(self, canvas):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.rubberBand = None
        self.dragging = False
        self.radiusCenter = None
        self.cursor = QCursor(Qt.ArrowCursor)
        self.fillColor = QColor(254, 178, 76, 63)
        self.borderColour = QColor(254, 58, 29, 100)

    '''reimplement of the events
    '''
    def canvasPressEvent(self, event):
        if event.button() != Qt.LeftButton:
            return
        self.radiusCenter = self.toMapCoordinates(event.pos())

    def canvasMoveEvent(self, event):
        if (event.buttons() != Qt.LeftButton):
            return

        if not self.dragging:
            if (self.rubberBand == None):
                self.rubberBand = QgsRubberBand(self.canvas, QGis.Polygon)
                self.rubberBand.setFillColor(self.fillColor)
                self.rubberBand.setBorderColor(self.borderColour)
            self.dragging = True
        radiusEdge = self.toMapCoordinates(event.pos())
        self.setRadiusRubberBand(radiusEdge)

    def canvasReleaseEvent(self, event):
        if (event.button() != Qt.LeftButton):
            return
        if (not self.dragging):
            if self.rubberBand == None:
                self.rubberBand = QgsRubberBand(self.canvas, QGis.Polygon)
                self.rubberBand.setFillColor(self.fillColor )
                self.rubberBand.setBorderColor(self.borderColour )
            self.radiusCenter = self.toMapCoordinates(event.pos())
            radiusEdge = self.toMapCoordinates(QPoint(event.pos().x() + 1, event.pos().y() + 1))
            self.setRadiusRubberBand(radiusEdge)

        radiusGeometry = self.rubberBand.asGeometry()
        MapToolSelectUtils.setSelectFeaturesEvent(self.canvas, radiusGeometry, event)
        self.rubberBand.reset(QGis.Polygon)
        self.rubberBand = None
        self.dragging = False

    def setRadiusRubberBand(self, radiusEdge):
        r = math.sqrt(self.radiusCenter.sqrDist(radiusEdge))
        self.rubberBand.reset(QGis.Polygon)

        for i in range(1, RADIUS_SEGMENTS + 1):
            theta = i * (2.0 * M_PI / RADIUS_SEGMENTS)
            radiusPoint = QgsPoint(self.radiusCenter.x() + r * math.cos( theta ),
                                   self.radiusCenter.y() + r * math.sin( theta ))
            self.rubberBand.addPoint(radiusPoint)