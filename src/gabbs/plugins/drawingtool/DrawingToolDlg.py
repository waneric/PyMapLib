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

Author: Wan Wei
Date: 2015-11-06
Version: 0.1.0
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import *

from qgis.core import *
from qgis.gui import *

from ui_WidgetDrawingTool import Ui_WidgetDrawingTool

class DrawingToolDlg(QDialog, Ui_WidgetDrawingTool):
    def __init__(self, iface):
        super(DrawingToolDlg, self).__init__(iface.mainWindow)
        self.setupUi(self)
        self.iface = iface
        self.canvas = self.iface.mapCanvas
        self.rectangle = QgsRectangle(0.0,0.0,0.0,0.0)
        self.numCorners = 0
        self.hasRectangle = False
        self.isEmittingPoint = False # indicates whether rubber band points are being captured

        # Set up the rubber band parameters
        self.lineColor = QColor(255,0,0)
        self.lineWidth = 2

        # Init rubberBand
        self.emitPoint = QgsMapToolEmitPoint(self.canvas)
        QObject.connect(self.emitPoint, 
                        SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"), 
                        self.drawingRectangle)

        #self.label = QLabel(self)
        #self.label.setGeometry(QRect(10, 120, 181, 31))

    def drawingRectangle(self, point, button):
        if self.hasRectangle: # just adjusting corners
            self.adjustRectangle(point)
        elif self.numCorners == 0: # no points yet - set first point
            self.numCorners = 1
            self.xStart = point.x()
            self.yStart = point.y()
        else: # have one corner, adding second one
            # create the rubber band to be used to display the clip area and set up it's initial limits
            self.rubberBand=QgsRubberBand(self.canvas)
            self.rubberBand.setColor(self.lineColor)
            self.rubberBand.setWidth(self.lineWidth)
            self.rectangle.setXMinimum(min(self.xStart,point.x()))
            self.rectangle.setYMinimum(min(self.yStart,point.y()))
            self.rectangle.setXMaximum(max(self.xStart,point.x()))
            self.rectangle.setYMaximum(max(self.yStart,point.y()))
            self.numCorners = 2
            self.adjustRectangle(point)
            self.hasRectangle = True

        self.updateCoordinates()

    def adjustRectangle(self, point):
        """
        Adjusts the clip rectangle according to the input point and redraws the rubber band
        """
        if self.hasRectangle:
            self.rubberBand.reset()
            if abs(self.rectangle.xMinimum() - point.x()) < abs(self.rectangle.xMaximum() - point.x()):
                # closest to the left - move that
                self.rectangle.setXMinimum(point.x())
            else:
                # closest to the right - move that
                self.rectangle.setXMaximum(point.x())
            if abs(self.rectangle.yMinimum() - point.y()) < abs(self.rectangle.yMaximum() - point.y()):
                # closest to the bottom - move that
                self.rectangle.setYMinimum(point.y())
            else:
                # closest to the top - move that
                self.rectangle.setYMaximum(point.y())
        # draw the new clip rectangle
        self.rubberBand.addPoint(QgsPoint(self.rectangle.xMaximum(), self.rectangle.yMaximum()))
        self.rubberBand.addPoint(QgsPoint(self.rectangle.xMaximum(), self.rectangle.yMinimum()))
        self.rubberBand.addPoint(QgsPoint(self.rectangle.xMinimum(), self.rectangle.yMinimum()))
        self.rubberBand.addPoint(QgsPoint(self.rectangle.xMinimum(), self.rectangle.yMaximum()))
        self.rubberBand.addPoint(QgsPoint(self.rectangle.xMaximum(), self.rectangle.yMaximum()))

    def setDrawingTool(self):
        if not self.isEmittingPoint and \
            self.canvas.mapTool() != self.emitPoint:
                self.canvas.setMapTool(self.emitPoint)
                self.isEmittingPoint = True

    def resetDrawingTool(self):
        if self.isEmittingPoint and \
            self.canvas.mapTool() == self.emitPoint:
                self.canvas.unsetMapTool(self.emitPoint)
                self.isEmittingPoint = False
        if self.hasRectangle:
            self.rubberBand.reset()
            self.rubberBand.removeLastPoint()
            self.canvas.refresh()
            self.rubberBand = ''
            self.hasRectangle = False
            self.numCorners == 0
            self.rectangle = QgsRectangle(0.0,0.0,0.0,0.0)

        self.labelButtomRight.setText(' ')
        self.labelUpLeft.setText(' ')

    def updateCoordinates(self):
        self.labelButtomRight.setText('X ' + str(self.rectangle.xMaximum()) + ' ' + \
                                      'Y ' + str(self.rectangle.yMinimum()))
        self.labelUpLeft.setText('X ' + str(self.rectangle.xMinimum()) + ' ' + \
                                 'Y ' + str(self.rectangle.yMaximum()))

                        
"""
    def getDrawingBounds(self):
        self.label.setText(str(self.rectangle.xMinimum()) + ' ' + \
                           str(self.rectangle.yMaximum()) + ' ' + \
                           str(self.rectangle.xMaximum()) + ' ' + \
                           str(self.rectangle.yMinimum()))
"""
