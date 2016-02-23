# -*- coding: utf-8 -*-

"""
map event.py  -  map event file for gabbs maps
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

from gabbs.basic.MapProperty import *
from gabbs.layers.LayerProperty import *
from gabbs.layers.Overlay import (Vector,
                                  Raster,
                                  DelimitedText)
from gabbs.MapUtils import iface, debug_trace

"""
bounds_changed
center_changed
                       click
                       dblclick
drag
dragend
dragstart
heading_changed
idle
maptypeid_changed
                       mousemove
                       mouseout
                       mouseover
projection_changed
resize
                       rightclick
tilesloaded
tilt_changed
zoom_changed"""
#QEvent::MouseButtonDblClick	4	Mouse press again (QMouseEvent).
#QEvent::MouseButtonPress	2	Mouse press (QMouseEvent).
#QEvent::MouseButtonRelease	3	Mouse release (QMouseEvent).
#QEvent::MouseMove

@staticmethod
def defaultHandler():
    pass

class MapEvent:
    MouseButtonRelease = defaultHandler
    MouseButtonDblClick = defaultHandler
    MouseRightButtonRelease = defaultHandler
    MouseMove = defaultHandler
    HoverLeave = defaultHandler
    HoverMove = defaultHandler

class MapAction:
    MouseButtonRelease = defaultHandler
    MouseButtonDblClick = defaultHandler
    MouseRightButtonRelease = defaultHandler
    MouseMove = defaultHandler
    HoverLeave = defaultHandler
    HoverMove = defaultHandler
"""
QgsAction::Generic, tr( "Echo attribute's value" ), "echo \"[% \"MY_FIELD\" %]\"", "", true );
QgsAction::Generic, tr( "Run an application" ), "ogr2ogr -f \"ESRI Shapefile\" \"[% \"OUTPUT_PATH\" %]\" \"[% \"INPUT_FILE\" %]\"", "", true );
QgsAction::GenericPython, tr( "Get feature id" ), "QtGui.QMessageBox.information(None, \"Feature id\", \"feature id is [% $id %]\")", "", false );
QgsAction::GenericPython, tr( "Selected field's value (Identify features tool)" ), "QtGui.QMessageBox.information(None, \"Current field's value\", \"[% $currentfield %]\")", "", false );
QgsAction::GenericPython, tr( "Clicked coordinates (Run feature actions tool)" ), "QtGui.QMessageBox.information(None, \"Clicked coords\", \"layer: [% $layerid %]\\ncoords: ([% $clickx %],[% $clicky %])\")", "", false );
QgsAction::OpenUrl, tr( "Open file" ), "[% \"PATH\" %]", "", false );
QgsAction::OpenUrl, tr( "Search on web based on attribute's value" ), "http://www.google.com/search?q=[% \"ATTRIBUTE\" %]", "", false );
"""

def addAction(actionLayer, actionType, actionName, actionSript):
    layer = actionLayer.getLayer()
    actions = layer.actions()
    if not layer or layer.type() != QgsMapLayer.VectorLayer:
        return
    if actionType == 'generic':
        type = QgsAction.Generic
    elif actionType == 'python':
        type = QgsAction.GenericPython
    elif actionType == 'open':
        type = QgsAction.OpenUrl
    else:
        type = QgsAction.Generic

    name = QString(actionName)
    action = QString(actionSript)
    #icon = QIcon()
    if (not name.isEmpty() and not action.isEmpty()):
        actions.addAction(type, name, action, False) #item.checkState() == Qt.Checked
        actions.setDefaultAction(0)
        #actionLayer.attributeAction = actions
        #QgsMapLayerActionRegistry.instance().addMapLayerAction(mapActions[0])
        #QgsMapLayerActionRegistry.instance().setDefaultActionForLayer(QgsMapLayer(layer), mapActions)

def addListener(eventCaller, eventSignal, eventHandler):
    lyrId = eventCaller.layerTypeId
    if lyrId == LayerTypeId.VECTOR or lyrId == LayerTypeId.DELIMITED_TEXT:
        eCaller = eventCaller.getLayer()
        if not eCaller:
            return
        addVectorListener(eCaller, eventSignal, eventHandler)
    elif lyrId == LayerTypeId.RASTER:
        pass
    elif lyrId == LayerTypeId.TMS:
        addMapListener(eventSignal, eventHandler)

def addVectorListener(eCaller, eSignal, eHandler):
    if eSignal == "select":
        eCaller.selectionChanged.connect(eventHandler)
        #QObject.connect(lyr, SIGNAL("selectionChanged (const QgsFeatureIds, const QgsFeatureIds, const bool)"), __selectedEventHandler(event))

def addMapListener(eSignal, eHandler):
    if eSignal == "click":
        MapEvent.MouseButtonRelease = eHandler
    elif eSignal == "dbclick":
        MapEvent.MouseButtonDblClick = eHandler
    elif eSignal == "rightclick":
        MapEvent.MouseRightButtonRelease = eHandler
    elif eSignal == "mousemove":
        MapEvent.MouseMove = eHandler
    #elif eSignal == "mouseenter":
    #    MapEvent.HoverEnter = eventHandler
    elif eSignal == "mouseout":
        MapEvent.HoverLeave = eHandler
    elif eSignal == "mouseover":
        MapEvent.HoverMove = eHandler

"""
void 	currentLayerChanged (QgsMapLayer *layer)
 	Emitted when the current layer is changed. More...
 
void 	destinationCrsChanged ()
 	Emitted when map CRS has changed. More...
 
void 	extentsChanged ()
 	Emitted when the extents of the map change. More...
 
void 	hasCrsTransformEnabledChanged (bool flag)
 	Emitted when on-the-fly projection has been turned on/off. More...
 
void 	keyPressed (QKeyEvent *e)
 	Emit key press event. More...
 
void 	keyReleased (QKeyEvent *e)
 	Emit key release event. More...
 
void 	layersChanged ()
 	Emitted when a new set of layers has been received. More...
 
void 	layerStyleOverridesChanged ()
 	Emitted when the configuration of overridden layer styles changes. More...
 
void 	mapCanvasRefreshed ()
 	Emitted when canvas finished a refresh request. More...
 
void 	mapToolSet (QgsMapTool *tool)
 	Emit map tool changed event. More...
 
void 	mapToolSet (QgsMapTool *newTool, QgsMapTool *oldTool)
 	Emit map tool changed with the old tool. More...
 
void 	mapUnitsChanged ()
 	Emmitted when map units are changed. More...
 
void 	renderComplete (QPainter *)
 	Emitted when the canvas has rendered. More...
 
void 	renderStarting ()
 	Emitted when the canvas is about to be rendered. More...
 
void 	rotationChanged (double)
 	Emitted when the rotation of the map changes. More...
 
void 	scaleChanged (double)
 	Emitted when the scale of the map changes. More...
 
void 	selectionChanged (QgsMapLayer *layer)
 	Emitted when selection in any layer gets changed. More...
 
Q_DECL_DEPRECATED void 	setProgress (int, int)
 	Let the owner know how far we are with render operations. More...
 
void 	xyCoordinates (const QgsPoint &p)
 	Emits current mouse position. More...
 
void 	zoomLastStatusChanged (bool)
 	Emitted when zoom last status changed. More...
 
void 	zoomNextStatusChanged (bool)
"""
"""
some_action.triggered.connect(functools.partial(some_callback, param1, param2))
             result = QObject.connect(self.clickTool, SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"), self.handleMouseDown)
             QMessageBox.information( self.iface.mainWindow(),"Info", "connect = %s"%str(result) )
def handleMouseDown(self, point, button):
        QMessageBox.information( self.iface.mainWindow(),"Info", "X,Y = %s,%s" % (str(point.x()),str(point.y())) )"""