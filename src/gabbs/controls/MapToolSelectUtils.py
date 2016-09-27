# -*- coding: utf-8 -*-

"""

MapToolSelectUtils.py  -  utilitis for map selecting tool

======================================================================
AUTHOR:  Wei Wan, Purdue University

EMAIL:   rcac-help@purdue.edu

Copyright (c) 2016  Purdue University

See the file "license.terms" for information on usage and
redistribution of this file, and for a DISCLAIMER OF ALL WARRANTIES.

======================================================================

"""
import sys
from PyQt4.QtCore import (Qt)
from PyQt4.QtGui import  (QMouseEvent,
                          QApplication)
from qgis.core import (QGis,
                       QgsMapLayer,
                       QgsVectorLayer,
                       QgsFeature,
                       QgsGeometry,
                       QgsCsException,
                       QgsCoordinateTransform,
                       QgsFeatureIterator,
                       QgsFeatureRequest,
                       QgsRenderContext)

from qgis.gui import  (QgsMessageBar,
                       QgsMapCanvas,
                       QgsRubberBand)
from gabbs.MapUtils import iface, debug_trace
#include "qgsmaptoolselectutils.h"
#include "qgisapp.h"
#include "qgsmessagebar.h"   OK
#include "qgsmapcanvas.h"    OK
#include "qgsvectorlayer.h"  ok
#include "qgsfeature.h"      ok
#include "qgsgeometry.h"     ok
#include "qgsrubberband.h"   ok
#include "qgscsexception.h"  ok
#include "qgslogger.h"       ok
#include "qgis.h"
#include <QMouseEvent> OK
#include <QApplication> OK

QgsAttributeList = []

def getCurrentVectorLayer(canvas):
    """
    get active layer
    """
    vlayer = canvas.currentLayer()
    if vlayer == None or vlayer.type() != QgsMapLayer.VectorLayer:
        """
        QgisApp.instance().messageBar().pushMessage(
                QObject.tr( "No active vector layer" ),
                QObject.tr( "To select features, choose a vector layer in the legend" ),
                QgsMessageBar.INFO,
                QgisApp.instance(.messageTimeout())
       """
        return None
    return vlayer

def setRubberBand(canvas, selectRect, rubberBand):

    transform = canvas.getCoordinateTransform()
    ll = transform.toMapCoordinates( selectRect.left(), selectRect.bottom() )
    lr = transform.toMapCoordinates( selectRect.right(), selectRect.bottom() )
    ul = transform.toMapCoordinates( selectRect.left(), selectRect.top() )
    ur = transform.toMapCoordinates( selectRect.right(), selectRect.top() )

    if (rubberBand):
        rubberBand.reset(QGis.Polygon)
        rubberBand.addPoint(ll, False)
        rubberBand.addPoint(lr, False)
        rubberBand.addPoint(ur, False)
        rubberBand.addPoint(ul, True)

def expandSelectRectangle(selectRect, vlayer, point):
    boxSize = 0
    if (vlayer.geometryType() != QGis.Polygon):
    #if point or line use an artificial bounding box of 10x10 pixels
    #to aid the user to click on a feature accurately
        boxSize = 5
    else:
    #otherwise just use the click point for polys
        boxSize = 1

    selectRect.setLeft(point.x() - boxSize)
    selectRect.setRight(point.x() + boxSize)
    selectRect.setTop(point.y() - boxSize)
    selectRect.setBottom(point.y() + boxSize)

def setSelectFeatures(canvas, selectGeometry, doContains, doDifference, singleSelect=None):
    """
    QgsMapCanvas* canvas,
    QgsGeometry* selectGeometry,
    bool doContains,
    bool doDifference,
    bool singleSelect 
    """
    if selectGeometry.type() != QGis.Polygon:
        return

    vlayer = getCurrentVectorLayer(canvas)

    if vlayer == None:
        return

    #toLayerCoordinates will throw an exception for any 'invalid' points in
    #the rubber band.
    #For example, if you project a world map onto a globe using EPSG 2163
    #and then click somewhere off the globe, an exception will be thrown.
    selectGeomTrans = QgsGeometry(selectGeometry)

    if canvas.mapSettings().hasCrsTransformEnabled():
        try:
            ct = QgsCoordinateTransform(canvas.mapSettings().destinationCrs(), vlayer.crs())
            selectGeomTrans.transform( ct )
        except QgsCsException as cse:
            Q_UNUSED(cse)
            #catch exception for 'invalid' point and leave existing selection unchanged
            """
            QgsLogger::warning( "Caught CRS exception " + QString( __FILE__ ) + ": " + QString::number( __LINE__ ) );
            QgisApp::instance()->messageBar()->pushMessage(
            QObject::tr( "CRS Exception" ),
            QObject::tr( "Selection extends beyond layer's coordinate system" ),
            QgsMessageBar::WARNING,
            QgisApp::instance()->messageTimeout() );
            """
            return

    QApplication.setOverrideCursor(Qt.WaitCursor)
    """
    QgsDebugMsg( "Selection layer: " + vlayer->name() );
    QgsDebugMsg( "Selection polygon: " + selectGeomTrans.exportToWkt() );
    QgsDebugMsg( "doContains: " + QString( doContains ? "T" : "F" ) );
    QgsDebugMsg( "doDifference: " + QString( doDifference ? "T" : "F" ) );
    """

    context = QgsRenderContext().fromMapSettings(canvas.mapSettings())
    r = vlayer.rendererV2()

    if r:
        r.startRender(context, vlayer.pendingFields())

    request = QgsFeatureRequest()
    request.setFilterRect(selectGeomTrans.boundingBox())
    request.setFlags(QgsFeatureRequest.ExactIntersect)

    if r:
        request.setSubsetOfAttributes(r.usedAttributes(), vlayer.pendingFields())
    else:
        request.setSubsetOfAttributes(QgsAttributeList)

    fit = vlayer.getFeatures(request)

    newSelectedFeatures = [] #QgsFeatureIds
    f = QgsFeature() 
    closestFeatureId = 0 #QgsFeatureId 
    foundSingleFeature = False
    #double closestFeatureDist = std::numeric_limits<double>::max();
    closestFeatureDist = sys.float_info.max

    while fit.nextFeature(f):
        # make sure to only use features that are visible
        if r and not r.willRenderFeature( f ):
            continue;
        g = QgsGeometry(f.geometry())
        if doContains:
            if not selectGeomTrans.contains(g):
                continue
        else:
            if not selectGeomTrans.intersects(g):
                continue
        if singleSelect:
            foundSingleFeature = True
            distance = float(g.distance(selectGeomTrans))
            if ( distance <= closestFeatureDist ):
                closestFeatureDist = distance
                closestFeatureId = f.id()
        else:
            newSelectedFeatures.insert(0, f.id())

    if singleSelect and foundSingleFeature:
        newSelectedFeatures.insert(0, closestFeatureId)
    if r:
        r.stopRender(context)
    #QgsDebugMsg( "Number of new selected features: " + QString::number( newSelectedFeatures.size() ) 

    if doDifference:
        layerSelectedFeatures = vlayer.selectedFeaturesIds()

        selectedFeatures = [] #QgsFeatureIds 
        deselectedFeatures = []# QgsFeatureIds

        # i = QgsFeatureIds.const_iterator(newSelectedFeatures.constEnd())
        # while i != newSelectedFeatures.constBegin():
        #     i = i - 1 
        #     if layerSelectedFeatures.contains(i):
        #         deselectedFeatures.insert(0, i)
        #     else:
        #         selectedFeatures.insert(0, i)

        for item in newSelectedFeatures:
            if item in layerSelectedFeatures:
                deselectedFeatures.insert(0, item)
            else:
                selectedFeatures.insert(0, item)


        vlayer.modifySelection(selectedFeatures, deselectedFeatures)
    else:
        vlayer.setSelectedFeatures(newSelectedFeatures)

    QApplication.restoreOverrideCursor()

    """
    fit = QgsFeatureIterator(vlayer.getFeatures( \
              QgsFeatureRequest().setFilterRect(selectGeomTrans.boundingBox()).setFlags(QgsFeatureRequest.ExactIntersect).setSubsetOfAttributes( \
                  QgsAttributeList)))
 
    fit = QgsFeatureIterator(vlayer.getFeatures( \
              QgsFeatureRequest().setFilterRect(selectGeomTrans.boundingBox()).setFlags(QgsFeatureRequest.ExactIntersect).setSubsetOfAttributes( \
                  QgsAttributeList())))
    """

def setSelectFeaturesEvent(canvas, selectGeometry, event):
    """
    QgsMapCanvas* canvas, QgsGeometry* selectGeometry, QMouseEvent * e 
    """
    if (event.modifiers() & Qt.ShiftModifier):
        doContains = True
    else:
        doContains = False

    if (event.modifiers() & Qt.ControlModifier):
        doDifference = True
    else:
        doDifference = False

    setSelectFeatures(canvas, selectGeometry, doContains, doDifference)
