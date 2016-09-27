"""
    /***************************************************************************
     *                                                                         *
     *   This program is free software; you can redistribute it and/or modify  *
     *   it under the terms of the GNU General Public License as published by  *
     *   the Free Software Foundation; either version 2 of the License, or     *
     *   (at your option) any later version.                                   *
     *                                                                         *
     ***************************************************************************/

    Drawing Tool - Quantum GIS python plugin for a user-selected rectangle

    Author: Wei Wan at purdue.rcac.edu
    Date: 2015-11-06
    Version: 0.1.0
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import *
from qgis.core import *
from qgis.gui import *

from gabbs.MapUtils import iface, debug_trace

class DrawingMapTool(QgsMapToolEmitPoint):
    def __init__(self, canvas):
        self.canvas = canvas
        QgsMapToolEmitPoint.__init__(self, self.canvas)

        self.mapUnitsPerPixel = self.canvas.mapUnitsPerPixel()
        self.rectangle = QgsRectangle(0.0,0.0,0.0,0.0)
        self.numCorners = 0
        self.hasRectangle = False
        self.isEmittingPoint = False

        self.fillColor = QColor(254, 178, 76, 63)
        self.borderColour = QColor(254, 58, 29, 100)

        self.rubberBand = QgsRubberBand(self.canvas, QGis.Polygon)
        self.rubberBand.setFillColor(self.fillColor)
        self.rubberBand.setBorderColor(self.borderColour)

        QObject.connect(self, 
                        SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"), 
                        self.drawRectangle)

    def drawRectangle(self, point, button):
        if button == Qt.RightButton:
            if self.isEmittingPoint == False:
                return
            self.resetMapTool()
            return
        elif button == Qt.LeftButton:
            self.isEmittingPoint = True
            if self.hasRectangle:
                self.adjustRectangle(point)
            elif self.numCorners == 0:
                self.numCorners = 1
                self.xStart = point.x()
                self.yStart = point.y()
                boxSize = 2 * self.canvas.mapUnitsPerPixel()
                self.rectangle.setXMinimum(point.x() - boxSize)
                self.rectangle.setYMinimum(point.y() - boxSize)
                self.rectangle.setXMaximum(point.x() + boxSize)
                self.rectangle.setYMaximum(point.y() + boxSize)
                self.adjustRectangle(point)
            else:
                self.rectangle.setXMinimum(min(self.xStart,point.x()))
                self.rectangle.setYMinimum(min(self.yStart,point.y()))
                self.rectangle.setXMaximum(max(self.xStart,point.x()))
                self.rectangle.setYMaximum(max(self.yStart,point.y()))
                self.numCorners = 2
                self.adjustRectangle(point)
                self.hasRectangle = True

    def adjustRectangle(self, point):
        if self.hasRectangle:
            if abs(self.rectangle.xMinimum() - point.x()) < abs(self.rectangle.xMaximum() - point.x()):
                self.rectangle.setXMinimum(point.x())
            else:
                self.rectangle.setXMaximum(point.x())
            if abs(self.rectangle.yMinimum() - point.y()) < abs(self.rectangle.yMaximum() - point.y()):
                self.rectangle.setYMinimum(point.y())
            else:
                self.rectangle.setYMaximum(point.y())

        self.rubberBand.reset(QGis.Polygon)
        self.rubberBand.addPoint(QgsPoint(self.rectangle.xMaximum(), self.rectangle.yMaximum()), False)
        self.rubberBand.addPoint(QgsPoint(self.rectangle.xMaximum(), self.rectangle.yMinimum()), False)
        self.rubberBand.addPoint(QgsPoint(self.rectangle.xMinimum(), self.rectangle.yMinimum()), False)
        self.rubberBand.addPoint(QgsPoint(self.rectangle.xMinimum(), self.rectangle.yMaximum()), False)
        self.rubberBand.addPoint(QgsPoint(self.rectangle.xMaximum(), self.rectangle.yMaximum()), True)

    def setDrawingTool(self):
        if not self.isEmittingPoint or \
            self.canvas.mapTool() != self:
                self.canvas.setMapTool(self)
                self.isEmittingPoint = True

    def resetMapTool(self):
        self.isEmittingPoint = False
        self.hasRectangle = False
        self.numCorners = 0
        self.rectangle = QgsRectangle(0.0,0.0,0.0,0.0)
        self.rubberBand.reset()
        self.rubberBand.removeLastPoint()
        self.canvas.refresh()
        #self.rubberBand = ''

    def expandRectangle(self, selectRect, point):
        boxSize = 1 * self.mapUnitsPerPixel
        selectRect.setXMinimum(point.x() - boxSize)
        selectRect.setYMinimum(point.y() - boxSize)
        selectRect.setXMaximum(point.x() + boxSize)
        selectRect.setYMaximum(point.y() + boxSize)

    def createCrsTransform(self, srcCrsId=4326, destCrsId=3857):
        srcCrs = QgsCoordinateReferenceSystem()
        srcCrs.createFromString("EPSG:4326")
        destCrs = QgsCoordinateReferenceSystem()
        destCrs.createFromString("EPSG:3857")
        crsTransform = QgsCoordinateTransform(srcCrs, destCrs)
        return crsTransform

    def getBoundingBox(self):
        if not self.rectangle.isNull():
            crsTransform = self.createCrsTransform()
            rectangle = crsTransform.transform(self.rectangle, QgsCoordinateTransform.ReverseTransform)
        else:
            rectangle = self.rectangle
        return rectangle.toRectF()