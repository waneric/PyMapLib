# -*- coding: utf-8 -*-
"""

MapTool.py  -  base class for map tool

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

from gabbs.controls.MapControlProperty import *
from gabbs.controls.MapToolAction import MapToolFeatureAction
from gabbs.controls.MapToolSelect import(MapToolSelectSingle,
                                         MapToolSelectRectangle,
                                         MapToolSelectPolygon,
                                         MapToolSelectFreehand,
                                         MapToolSelectRadius)
import gabbs.controls.MapToolSelectUtils as MapToolSelectUtils

import gabbs.resources_rc
from gabbs.MapUtils import iface, debug_trace


class MapTool(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.canvas = iface.mapCanvas
        self.window = iface.mainWindow
        self.mapToolBar = None

    def addMapToolPan(self, size, style):
        self.mapToolBar = iface.mapToolBar
        if size == mapControlStyle.SMALL:
            tools = ['PAN']
        elif size == mapControlStyle.LARGE:
            tools = ['PAN']
        else:
            tools = ['PAN']
        mapToolButtons = []
        for tool in tools:
            button = mapToolButton()
            if tool == "PAN":
                button.name = "PAN"
                button.action = QAction(QIcon(':/gabbs/resources/img/pan.png'),QString("Pan"), self.window)
                button.mapFunction = self.pan
                button.checkable = True
            mapToolButtons.append(button)

        for button in mapToolButtons:
            if button.checkable is True:
                button.action.setCheckable(True)
                # Connect the trigger signal to a slot.)
            button.action.triggered.connect(button.mapFunction)
            if button.name == "PAN":
                self.toolPan = QgsMapToolPan(self.canvas)
                self.toolPan.setAction(button.action)
            # Add button to toolbar
            self.mapToolBar.addAction(button.action)

    def addMapToolZoom(self, size, style, option):
        self.mapToolBar = iface.mapToolBar
        style = mapControlStyle.DROPDOWN_MENU
        if size == zoomControlStyle.SMALL:
            tools = ['ZOOMIN', 'ZOOMOUT']
        elif size == zoomControlStyle.LARGE:
            tools = ['ZOOMIN', 'ZOOMOUT', 'ZOOMHOME', 'ZOOMFULL', 'ZOOMLAYER']
        elif size == zoomControlStyle.CUSTOM:
            if len(option) > 0:
                tools = option
            else:
                tools = ['ZOOMIN', 'ZOOMOUT']
        else:
            tools = ['ZOOMIN', 'ZOOMOUT']

        mapToolButtons = []
        for tool in tools:
            button = mapToolButton()
            if tool == "ZOOMIN":
                button.name = "ZOOMIN"
                button.action = QAction(QIcon(':/gabbs/resources/img/zoom-in.png'), QString("Zoom In"), self.window)
                button.mapFunction = self.zoomIn
                button.checkable = True
            elif tool == "ZOOMOUT":
                button.name = "ZOOMOUT"
                button.action = QAction(QIcon(':/gabbs/resources/img/zoom-out.png'), QString("Zoom Out"), self.window)
                button.mapFunction = self.zoomOut
                button.checkable = True
            elif tool == "ZOOMHOME":
                button.name = "ZOOMHOME"
                button.action = QAction(QIcon(':/gabbs/resources/img/zoom-home.png'), QString("Zoom Home"),self.window)
                button.mapFunction = self.zoomHome
            elif tool == "ZOOMFULL":
                button.name = "ZOOMFULL"
                button.action = QAction(QIcon(':/gabbs/resources/img/zoom-full.png'), QString("Zoom Full"),self.window)
                button.mapFunction = self.zoomFull
            elif tool == "ZOOMLAYER":
                button.name = "ZOOMLAYER"
                button.action = QAction(QIcon(':/gabbs/resources/img/zoom-layer.png'),QString("Zoom To Layer"), self.window)
                button.mapFunction = self.zoomLayer
            mapToolButtons.append(button)

        if style == mapControlStyle.DROPDOWN_MENU:
            self.popupMenu = QMenu(self.window)

        for button in mapToolButtons:
            if button.checkable is True:
                button.action.setCheckable(True)
                # Connect the trigger signal to a slot.)
            button.action.triggered.connect(button.mapFunction)
            if button.name == "PAN":
                self.toolPan = QgsMapToolPan(self.canvas)
                self.toolPan.setAction(button.action)
            elif button.name == "ZOOMIN":
                self.toolZoomIn = QgsMapToolZoom(self.canvas, False) # false = in
                self.toolZoomIn.setAction(button.action)
            elif button.name == "ZOOMOUT":
                self.toolZoomOut = QgsMapToolZoom(self.canvas, True) # true = out
                self.toolZoomOut.setAction(button.action)
            elif button.name == "ZOOMHOME":
                pass
            elif button.name == "ZOOMFULL":
                pass
            elif button.name == "ZOOMLAYER":
                pass

            # Add button to toolbar
            if style == mapControlStyle.DROPDOWN_MENU:
                self.popupMenu.addAction(button.action)
            elif style == mapControlStyle.HORIZONTAL_BAR:
                self.mapToolBar.addAction(button.action)
            else:
                self.mapToolBar.addAction(button.action)

        if style == mapControlStyle.DROPDOWN_MENU:
            self.toolButton = QToolButton()
            self.toolButton.setMenu(self.popupMenu)
            self.toolButton.setDefaultAction(mapToolButtons[0].action)
            self.toolButton.setPopupMode(QToolButton.InstantPopup)
            self.mapToolBar.addWidget(self.toolButton)

    def addMapToolSelect(self, size, style, option):
        self.mapToolBar = iface.mapToolBar
        if size == selectControlStyle.SMALL:
            tools = ['RECTANGLE']
        elif size == selectControlStyle.LARGE:
            tools = ["SINGLE", 'RECTANGLE', 'POLYGON', 'FREEHAND', 'RADIUS']
        elif size == selectControlStyle.CUSTOM:
            if len(option) > 0:
                tools = option
            else:
                tools = ['RECTANGLE']
        else:
            tools = ['RECTANGLE']

        mapToolButtons = []
        for tool in tools:
            button = mapToolButton()
            button.checkable = True
            if tool == "SINGLE":
                button.name = "SINGLE"
                button.action = QAction(QIcon(':/gabbs/resources/img/select.png'),QString("Select"), self.window)
                button.mapFunction = self.selectSingle
            elif tool == "RECTANGLE":
                button.name = "RECTANGLE"
                button.action = QAction(QIcon(':/gabbs/resources/img/select-rectangle.png'), QString("Select Rectangle"), self.window)
                button.mapFunction = self.selectRectangle
            elif tool == "POLYGON":
                button.name = "POLYGON"
                button.action = QAction(QIcon(':/gabbs/resources/img/select-polygon.png'), QString("Select Polygon"), self.window)
                button.mapFunction = self.selectPolygon
            elif tool == "FREEHAND":
                button.name = "FREEHAND"
                button.action = QAction(QIcon(':/gabbs/resources/img/select-freehand.png'), QString("Select Freehand"), self.window)
                button.mapFunction = self.selectFreehand
            elif tool == "RADIUS":
                button.name = "RADIUS"
                button.action = QAction(QIcon(':/gabbs/resources/img/select-radius.png'), QString("Select Radius"), self.window)
                button.mapFunction = self.selectRadius
            mapToolButtons.append(button)

        if style == mapControlStyle.DROPDOWN_MENU:
            self.popupMenu = QMenu(self.window)

        for button in mapToolButtons:
            if button.checkable is True:
                button.action.setCheckable(True)
                # Connect the trigger signal to a slot
            button.action.triggered.connect(button.mapFunction)
            if button.name == "SINGLE":
                self.toolSelect = MapToolSelectSingle(iface.mapCanvas)
                self.toolSelect.setAction(button.action)
            elif button.name == "RECTANGLE":
                self.toolSelectRectangle = MapToolSelectRectangle(iface.mapCanvas)
                self.toolSelectRectangle.setAction(button.action)
            elif button.name == "POLYGON":
                self.toolSelectPolygon = MapToolSelectPolygon(iface.mapCanvas)
                self.toolSelectPolygon.setAction(button.action)
            elif button.name == "FREEHAND":
                self.toolSelectFreehand = MapToolSelectFreehand(iface.mapCanvas)
                self.toolSelectFreehand.setAction(button.action)
            elif button.name == "RADIUS":
                self.toolSelectRadius = MapToolSelectRadius(iface.mapCanvas)
                self.toolSelectRadius.setAction(button.action)
            # Add button to toolbar
            if style == mapControlStyle.DROPDOWN_MENU:
                self.popupMenu.addAction(button.action)
            elif style == mapControlStyle.HORIZONTAL_BAR:
                self.mapToolBar.addAction(button.action)
            else:
                self.mapToolBar.addAction(button.action)

        if style == mapControlStyle.DROPDOWN_MENU:
            self.toolButton = QToolButton()
            self.toolButton.setMenu(self.popupMenu)
            self.toolButton.setDefaultAction(mapToolButtons[0].action)
            self.toolButton.setPopupMode(QToolButton.InstantPopup)
            self.mapToolBar.addWidget(self.toolButton)

    def addMapToolAction(self, size, style):
        self.mapToolBar = iface.mapToolBar
        tools = ['FEATURE_ACTION']
        mapToolButtons = []
        for tool in tools:
            button = mapToolButton()
            if tool == "FEATURE_ACTION":
                button.name = "FEATURE_ACTION"
                button.action = QAction(QIcon(':/gabbs/resources/img/mAction.png'),QString("Feature Action"), self.window)
                button.mapFunction = self.featureAction
                button.checkable = True
            mapToolButtons.append(button)

        for button in mapToolButtons:
            if button.checkable is True:
                button.action.setCheckable(True)
                # Connect the trigger signal to a slot.)
            button.action.triggered.connect(button.mapFunction)
            if button.name == "FEATURE_ACTION":
                self.toolFeatureAction = MapToolFeatureAction(self.canvas)
                self.toolFeatureAction.setAction(button.action)
            # Add button to toolbar
            self.mapToolBar.addAction(button.action)

    def pan(self):
        self.canvas.setMapTool(self.toolPan)

    def zoomIn(self):
        self.canvas.setMapTool(self.toolZoomIn)

    def zoomOut(self):
        self.canvas.setMapTool(self.toolZoomOut)

    def zoomHome(self):
        # Scale the map
        if iface.mapZoomScale:
            iface.mapCanvas.zoomScale(iface.mapZoomScale)
        # Center the map
        if iface.mapCenterPoint:
            iface.mapCanvas.setCenter(iface.mapCenterPoint)

    def zoomFull(self):
        self.canvas.zoomToFullExtent()

    def zoomLayer(self):
        # TO-DO NOT WORKING
        lyr = self.canvas.currentLayer()
        lyrCrs = lyr.crs()
        if lyrCrs != iface.coordRefSys:
            coordTrans = QgsCoordinateTransform(lyrCrs, iface.coordRefSys)
            extent = coordTrans.transform(lyr.extent(), QgsCoordinateTransform.ForwardTransform)
            #extent.scale( 1.05 )
            self.canvas.setExtent(extent)

    def selectSingle(self):
        self.canvas.setMapTool(self.toolSelect)

    def selectRectangle(self):
        self.canvas.setMapTool(self.toolSelectRectangle)

    def selectPolygon(self):
        self.canvas.setMapTool(self.toolSelectPolygon)

    def selectFreehand(self):
        self.canvas.setMapTool(self.toolSelectFreehand)

    def selectRadius(self):
        self.canvas.setMapTool(self.toolSelectRadius)

    def featureAction(self):
        self.canvas.setMapTool(self.toolFeatureAction)


class mapToolButton(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.icon = None
        self.name = " "
        self.action = None
        self.mapTool = None
        self.mapFunction = None
        self.checkable = False