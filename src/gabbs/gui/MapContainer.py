# -*- coding: utf-8 -*-

"""

MapContainer.py  -  window program and mapcanvas to show maps library

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

from gabbs.basic.MapCanvas import MapCanvas
from gabbs.layers.Map import Map
from gabbs.controls.MapTool import MapTool
from gabbs.controls.MapTip import MapTip
from gabbs.events.MapEvent import MapEvent
from gabbs.events.PythonUtils import (PythonRunnerImpl,
                                      PythonUtilsImpl)
from gabbs.gui.LegendWidget import Legend
from gabbs.gui.ui_MapContainer import Ui_MainWindow

from gabbs.plugins.valuetool.valuetool import ValueTool
from gabbs.plugins.drawingtool.drawingtool import DrawingTool

import gabbs.resources_rc
from gabbs.MapUtils import iface, debug_trace

class MapContainer(QMainWindow, Ui_MainWindow):
    def __init__(self, option):
        QMainWindow.__init__(self)
        self.setupUi(self)
        #self.setWindowTitle("ShapeViewer")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.option = option
        self.canvas = MapCanvas()
        iface.mainWindow = self
        iface.mapCanvas = self.canvas

        self.setCanvasProperty()
        self.setCanvasCrs()

        self.setCentralWidget(self.canvas)
        #self.canvas.show()

        """ Create the map legend widget and associate to the canvas """
        self.mapToolBar = None
        self.mapTool = MapTool()
        self.mapTip = MapTip()
        self.setMapControl()

        iface.pythonUtils = PythonRunnerImpl()
        QgsPythonRunner.setInstance(iface.pythonUtils)

        self.plugins = {}
        self.setPlugin()

    """ event filter for window events
    """
    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseMove:
            pos = event.pos()
            x = pos.x()
            y = pos.y()
            #p = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
            self.statusBar().showMessage("x: %s, y: %s" % (x, y))
        return QMainWindow.eventFilter(self, source, event)

    def setCanvasProperty(self):
        if 'canvasColor' in self.option:
            color = self.option['canvasColor']
            qColor = gabbs.MapUtils.getQColor(color)
            self.canvas.setCanvasColor(qColor)
        if 'backgroundColor' in self.option:
            debug_trace()
            color = self.option['backgroundColor']
            self.setStyleSheet("background-color: %s;" %color)
        self.canvas.setWheelAction(QgsMapCanvas.WheelNothing)
        self.canvas.setParallelRenderingEnabled(True)
        #self.canvas.setCachingEnabled(True)

    def coordRefSys(self, epsg):
        coordRefSys = QgsCoordinateReferenceSystem()
        if QGis.QGIS_VERSION_INT >= 10900:
            idEpsgRSGoogle = "EPSG:%d" % epsg
            createCrs = coordRefSys.createFromOgcWmsCrs(idEpsgRSGoogle)
        else:
            idEpsgRSGoogle = epsg
            createCrs = coordRefSys.createFromEpsg(idEpsgRSGoogle)
        if not createCrs:
            google_proj_def = "+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 "
            google_proj_def += "+units=m +nadgrids=@null +wktext +no_defs"
            isOk = coordRefSys.createFromProj4(google_proj_def)
            if not isOk:
                return None
        return coordRefSys

    def canvasCrs(self):
        if QGis.QGIS_VERSION_INT >= 20300:
            #crs = self.canvas.mapRenderer().destinationCrs()
            crs = self.canvas.mapSettings().destinationCrs()
        elif QGis.QGIS_VERSION_INT >= 10900:
            crs = self.canvas.mapRenderer().destinationCrs()
        else:
            crs = self.canvas.mapRenderer().destinationSrs()
        return crs

    def setCanvasCrs(self):
        # use Mercator as default
        epsgList = [3857]
        coordRefSys = self.coordRefSys(epsgList[0])
        canvasCrs = self.canvasCrs()
        if canvasCrs != coordRefSys:
            coordTrans = QgsCoordinateTransform(canvasCrs, coordRefSys)
            extMap = self.canvas.extent()
            extMap = coordTrans.transform(extMap, QgsCoordinateTransform.ForwardTransform)
            if QGis.QGIS_VERSION_INT >= 20300:
                self.canvas.setDestinationCrs(coordRefSys)
            elif QGis.QGIS_VERSION_INT >= 10900:
                self.canvas.mapRenderer().setDestinationCrs(coordRefSys)
            else:
                self.canvas.mapRenderer().setDestinationSrs(coordRefSys)
            self.canvas.freeze(False)
            #self.canvas.setMapUnits(coordRefSys.mapUnits())
            self.canvas.setMapUnits(QGis.Meters)
            self.canvas.setExtent(extMap)

        # On the fly
        if QGis.QGIS_VERSION_INT >= 20300:
            self.canvas.setCrsTransformEnabled(True)
        else:
            self.canvas.mapRenderer().setProjectionsEnabled(True)
        # Store refCrs to iface
        iface.coordRefSys = coordRefSys

    def addMapToolBar(self):
        if self.mapToolBar is None:
        # make sure isinstance(self.window, QMainWindow):
            self.mapToolBar = QToolBar("MapTool")
            self.mapToolBar.setFloatable(False)
            self.mapToolBar.setMovable(False)
            self.addToolBar(Qt.RightToolBarArea, self.mapToolBar)
            iface.mapToolBar = self.mapToolBar

    def addStatusBar(self):
        self.statusBar()
        self.statusBar().showMessage("x:    , y:    ")

    def setMapControl(self):
        if 'layerControl' in self.option:
            if self.option['layerControl'] == True:
                propertyFlag = False
                if 'layerControlOptions' in self.option:
                    if 'property' in self.option['layerControlOptions']:
                        if self.option['layerControlOptions']['property'] == 'ON':
                            propertyFlag = True
                self.addMapToolBar()
                self.setLegendWidget(True, propertyFlag)
            else:
                self.setLegendWidget(False, False)
        if 'panControl' in self.option:
            if self.option['panControl'] == True:
                size = 'DEFAULT'
                style = 'DROPDOWN_MENU'
                if 'panControlOptions' in self.option:
                    if 'size' in self.option['panControlOptions']:
                        size =  self.option['panControlOptions']['size']
                    if 'style' in self.option['panControlOptions']:
                        style =  self.option['panControlOptions']['style']
                self.addMapToolBar()
                self.mapTool.addMapToolPan(size, style)
        if 'zoomControl' in self.option:
            if self.option['zoomControl'] == True:
                size = 'DEFAULT'
                style = 'DROPDOWN_MENU'
                option = []
                if 'zoomControlOptions' in self.option:
                    if 'size' in self.option['zoomControlOptions']:
                        size =  self.option['zoomControlOptions']['size']
                    if 'style' in self.option['zoomControlOptions']:
                        style =  self.option['zoomControlOptions']['style']
                    if 'option' in self.option['zoomControlOptions']:
                        option = self.option['zoomControlOptions']['option'].replace(" ", "").split(',')
                self.addMapToolBar()
                self.mapTool.addMapToolZoom(size, style, option)
        if 'selectControl' in self.option:
            if self.option['selectControl'] == True:
                size = 'DEFAULT'
                style = 'DROPDOWN_MENU'
                option = []
                if 'selectControlOptions' in self.option:
                    if 'size' in self.option['selectControlOptions']:
                        size =  self.option['selectControlOptions']['size']
                    if 'style' in self.option['selectControlOptions']:
                        style =  self.option['selectControlOptions']['style']
                    if 'option' in self.option['selectControlOptions']:
                        option = self.option['selectControlOptions']['option'].replace(" ", "").split(',')
                self.addMapToolBar()
                self.mapTool.addMapToolSelect(size, style, option)
        if 'overviewControl' in self.option:
            if self.option['overviewControl'] == True:
                self.addMapToolBar()
                self.setOverviewWidget()
        if 'actionControl' in self.option:
            if self.option['actionControl'] == True:
                self.addMapToolBar()
                self.mapTool.addMapToolAction(size, style)
        if 'statusControl' in self.option:
            if self.option['statusControl'] == True:
                pass
                #self.addStatusBar()
                #self.canvas.viewport().installEventFilter(self)
        if 'mapTipControl' in self.option:
            if self.option['mapTipControl'] == True:
                self.addMapToolBar()
                self.setMapTip()

    def setLegendWidget(self, ctrlFlag=False, propFlag=False):
        # Create the docking legend, no floating style, start with hide
        self.legend = Legend(self)
        self.legend.setPropertyDlg(propFlag)
        iface.mapLegend = self.legend
        self.LegendDock = QDockWidget("Layers", self)
        self.LegendDock.setFeatures(QDockWidget.DockWidgetClosable)
        self.LegendDock.setObjectName("legend")
        self.LegendDock.setAllowedAreas(Qt.RightDockWidgetArea)
        self.LegendDock.setWidget(self.legend )
        self.LegendDock.setContentsMargins(6, 6, 6, 6)
        self.addDockWidget(Qt.RightDockWidgetArea, self.LegendDock)

        if ctrlFlag is True:
            self.legendAction = self.LegendDock.toggleViewAction()
            self.legendAction.setObjectName('lengendAction')
            self.legendAction.setIcon(QIcon(':/gabbs/resources/img/layer.png'))
            self.legendAction.setText(QString("Layers"))
            self.mapToolBar.addAction(self.legendAction)

        self.LegendDock.hide()

    def setOverviewWidget(self):
        # Create the overview object
        self.overview = QgsMapOverviewCanvas(self, self.canvas)
        self.overview.destinationSrsChanged()
        self.overview.hasCrsTransformEnabled(True)
        #self.overview.setBackgroundColor(QColor(255, 255, 255))

        self.canvas.enableOverviewMode(self.overview)
        iface.mapOverview = self.overview

        # Create the docking widget, no floating style, start with hide
        self.OverviewDock = QDockWidget("Overview", self)
        self.OverviewDock.setFeatures(QDockWidget.DockWidgetClosable)
        self.OverviewDock.setObjectName("Overview")
        self.OverviewDock.setAllowedAreas(Qt.RightDockWidgetArea)
        self.OverviewDock.setWidget(self.overview)
        self.OverviewDock.setContentsMargins (6, 6, 6, 6)
        self.addDockWidget(Qt.RightDockWidgetArea, self.OverviewDock)

        self.OverviewAction = self.OverviewDock.toggleViewAction()
        self.OverviewAction.setObjectName('OverviewAction')
        self.OverviewAction.setIcon(QIcon(':/gabbs/resources/img/overview.png'))
        self.OverviewAction.setText(QString("Overview"))

        self.mapToolBar.addAction(self.OverviewAction)
        self.OverviewDock.hide()

    def setMapTip(self):
        action = QAction(QIcon(':/gabbs/resources/img/mActionMapTips.png'),QString("Map Tip"), iface.mainWindow)
        action.setCheckable(True)
        action.toggled.connect(self.onToggledMapTip)
        self.mapToolBar.addAction(action)

    def onToggledMapTip(self, checked):
        if checked:
            self.mapTip.turnOnMapTips()
        else:
            self.mapTip.turnOffMapTips()

    def setPlugin(self):
        if 'pluginControl' in self.option:
            plugins = self.option['pluginControl'].replace(" ", "").split(',')
            for val in plugins:
                if val == 'valuetool':
                    self.addMapToolBar()
                    plugin = ValueTool(iface)
                    plugin.initGui()
                    self.plugins[val] = plugin
                if val == 'drawingtool':
                    self.addMapToolBar()
                    plugin = DrawingTool(iface)
                    plugin.initGui()
                    self.plugins[val] = plugin

    """ Public member functions
    """
    def addLayer(self, layer):
        if not layer.layer:
            return
        if not layer.layer.isValid():
            return
        # Set extent to the extent of our layer
        #if isinstance(layer, Map):
        #    self.canvas.setExtent(newQgsLayer.extent())
        """Handle layers being added to the registry so they show up in canvas.
        """
        """
        currentLayers = self.canvas.layers()
        finalLayers = []
        finalLayers.append(QgsMapCanvasLayer(newQgsLayer))
        for lyr in currentLayers:
            finalLayers.append(QgsMapCanvasLayer(lyr))
        self.canvas.setLayerSet(finalLayers)
        """
        QgsMapLayerRegistry.instance().addMapLayer(layer.layer)
        layer.addLayerCallback()

    def removeLayer(self, layer):
        qgsLayer = layer.getLayer()
        if qgsLayer is not None:
            lyrId = qgsLayer.id()
            QgsMapLayerRegistry.instance().removeMapLayer(lyrId)
            #layer.remove()
            layer = None

    def removeAllLayers(self):
        """Remove layers from the canvas before they get deleted."""
        self.canvas.setLayerSet([])
  
    def newProject(self):
        """Create new project."""
        QgsMapLayerRegistry.instance().removeAllMapLayers()