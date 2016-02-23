# -*- coding: utf-8 -*-

"""

MapToolAction.py  -  map tool for user events

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

class MapToolFeatureAction(QgsMapTool):
    '''
    Base class for the map select tools
    '''
    def __init__(self, canvas):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.rubberBand = None
        self.cursor = QCursor(Qt.ArrowCursor)

    # Override events
    def canvasReleaseEvent(self, event):

        layer = self.canvas.currentLayer()

        if not layer or layer.type() != QgsMapLayer.VectorLayer:
        #emit messageEmitted( tr( "To run an action, you must choose an active vector layer." ), QgsMessageBar.INFO );
            return

        if layer not in self.canvas.layers():
        #do not run actions on hidden layers
            return

        #QgsVectorLayer *vlayer = qobject_cast<QgsVectorLayer *>( layer );
        #if (layer.actions().size() == 0 and \
        #        len(QgsMapLayerActionRegistry.instance().mapLayerActions(layer)) == 0):
        #emit messageEmitted( tr( "The active vector layer has no defined actions" ), QgsMessageBar::INFO );
            return

        if(not self.doAction(layer, event.x(), event.y())):
        #QgisApp.instance().statusBar().showMessage(tr("No features at this position found."))
            pass

    """
    def activate(self):
        QgsMapTool.activate()

    def deactivate(self):
        QgsMapTool.deactivate()
    """

    def doAction(self, layer, x, y):
        if (not layer):
            return False

        point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
        featList = []

        #toLayerCoordinates will throw an exception for an 'invalid' point.
        #For example, if you project a world map onto a globe using EPSG 2163
        #and then click somewhere off the globe, an exception will be thrown.
        try:
        #create the search rectangle
            searchRadius = self.searchRadiusMU(self.canvas)

            r = QgsRectangle()
            r.setXMinimum(point.x() - searchRadius)
            r.setXMaximum(point.x() + searchRadius)
            r.setYMinimum(point.y() - searchRadius)
            r.setYMaximum(point.y() + searchRadius)

            r = self.toLayerCoordinates(layer, r)

            fit = layer.getFeatures(QgsFeatureRequest().setFilterRect(r).setFlags(QgsFeatureRequest.ExactIntersect))
            f = QgsFeature()
            while(fit.nextFeature(f)):
                featList.append(QgsFeature(f))
        except QgsCsException as cse:
            #Q_UNUSED(cse)
            #catch exception for 'invalid' point and proceed with no features found
            QgsDebugMsg(QString( "Caught CRS exception %1" ).arg(cse.what()))

        if len(featList) == 0:
            return False

        for feat in featList:
            if (layer.actions().defaultAction() >= 0):
            #define custom substitutions: layer id and clicked coords
                substitutionMap = {} #QMap 
                substitutionMap["$layerid"] = layer.id()
                point = self.toLayerCoordinates(layer, point)
                substitutionMap["$clickx"] = point.x()
                substitutionMap["$clicky"] = point.y()
                actionIdx = layer.actions().defaultAction()
                #layer.actions().doAction(actionIdx, feat, substitutionMap)
                self.doAttributeAction(layer, actionIdx, feat, substitutionMap)
            else:
                mapLayerAction = QgsMapLayerActionRegistry.instance().defaultActionForLayer(layer)
                if(mapLayerAction):
                    mapLayerAction.triggerForFeature(layer, feat)
        return True

    """ Reimplement method in QGIS C++ code
    """
    def doAttributeAction(self, layer, index, feat, substitutionMap):
        actions = layer.actions()
        if (index < 0 or index >= actions.size()):
            return
        action = actions.at(index)
        if (not action.runable()):
            return
        # search for expressions while expanding actions
        # no used for python binding
        #context = self.createExpressionContext(layer) 
        #context.setFeature(feat)
        #expandedAction = QString(QgsExpression.replaceExpressionText(action.action(), context, substitutionMap))
        expandedAction = QString(QgsExpression.replaceExpressionText(action.action(), feat, layer, substitutionMap))
        if (expandedAction.isEmpty()):
            return

        newAction = QgsAction(action.type(), action.name(), expandedAction, action.capture())
        self.runAttributeAction(newAction)

    def runAttributeAction(self, action):
        if (action.type() == QgsAction.OpenUrl):
            finfo = QFileInfo(action.action())
            if (finfo.exists() and finfo.isFile()):
                QDesktopServices.openUrl(QUrl.fromLocalFile(action.action()))
            else:
                QDesktopServices.openUrl(QUrl(action.action(), QUrl.TolerantMode))
        elif (action.type() == QgsAction.GenericPython):
            # TODO: capture output from QgsPythonRunner (like QgsRunProcess does)
            QgsPythonRunner.run(action.action(), QString("Python running error"))
        else:
            #The QgsRunProcess instance created by this static function
            #deletes itself when no longer needed.
            QgsRunProcess.create(action.action(), action.capture())

"""
    def createExpressionContext(self, layer):
        context = QgsExpressionContext()
        context.append(QgsExpressionContextUtils.globalScope())
        context.append(QgsExpressionContextUtils.projectScope())
        if (layer):
            context.append(QgsExpressionContextUtils.layerScope(layer))

        return context
"""