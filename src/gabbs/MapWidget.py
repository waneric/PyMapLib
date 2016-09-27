# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
"""
MapWidget.py  - xembedwidget to use map library
---------------------
date                 : August 2015
copyright            : (C) 2015 by Wei Wan
email                : wanw at purdue dot edu
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

import sys
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from gabbs.maps import *

from ui_MapWidget import Ui_MainWindow

class MapWidget(QX11EmbedWidget, Ui_MainWindow):
    # Signals
    vectorLayerAdded = pyqtSignal(dict)
    rasterLayerAdded = pyqtSignal(dict)
    delimitedTextLayerAdded = pyqtSignal(dict)
    layerRemoved = pyqtSignal(dict)
    getSelectedAttributes = pyqtSignal()
    returnCode = None
    returnValue = None

    def __init__(self, wndId, filePath):
        QX11EmbedWidget.__init__(self)
        self.setupUi(self)
        #debug_trace()
        self.mapConfig = MapConfig(filePath)
        # Create a Map Container, aka map canvas
        canvasProp = self.mapConfig.getMapContainerConfig()
        #canvasProp['pluginControl'] = 'valuetool'
        self.mapContainer = MapContainer(canvasProp)
        self.mapLayout.addWidget(self.mapContainer)

        # Create a Map object
        mapProp =  self.mapConfig.getMapConfig()
        if mapProp:
            self.map = Map(mapProp)
            self.mapContainer.addLayer(self.map)

        # Create a Vector object
        polygonProp = self.mapConfig.getVectorConfig()
        if polygonProp:
            self.polygon = Vector(polygonProp)
            self.mapContainer.addLayer(self.polygon)

        # Connect signal and slot
        self.vectorLayerAdded.connect(self.onVectorLayerAdded, 
                                      Qt.BlockingQueuedConnection)
        self.rasterLayerAdded.connect(self.onRasterLayerAdded,
                                      Qt.BlockingQueuedConnection)
        self.delimitedTextLayerAdded.connect(self.onDelimitedTextLayerAdded,
                                             Qt.BlockingQueuedConnection)
        self.getSelectedAttributes.connect(self.onGetSelectedAttributes,
                                                 Qt.BlockingQueuedConnection)
        self.layerRemoved.connect(self.onLayerRemoved,
                                                 Qt.BlockingQueuedConnection)
        self.embedded.connect(self.connectInfo)
        self.containerClosed.connect(self.closeInfo)

        self.embedInto(wndId)

        self.mapServerThread = ServerThread()
        self.mapServerThread.xmlRpcServer.register_function(
                                 self.gbsAddRasterLayerWrapper, 'gbsAddRasterLayer')
        self.mapServerThread.xmlRpcServer.register_function(
                                 self.gbsAddVectorLayerWrapper, 'gbsAddVectorLayer')
        self.mapServerThread.xmlRpcServer.register_function(
                                 self.gbsAddDelimitedTextLayerWrapper, 'gbsAddDelimitedTextLayer')
        self.mapServerThread.xmlRpcServer.register_function(
                                 self.gbsRemoveLayerWrapper, 'gbsRemoveLayer')
        self.mapServerThread.xmlRpcServer.register_function(
                                 self.gbsGetSelectedAttributesWrapper, 'gbsGetSelectedAttributes')
        self.mapServerThread.start()

    # Slot
    @pyqtSlot()
    def connectInfo(self):
        print "MapWidget Connected..."

    @pyqtSlot()
    def closeInfo(self):
        print "MapWidget Disconnected...\nShut Down..."

    @pyqtSlot(dict)
    def onVectorLayerAdded(self, layerProp):
        vectorProp = MapConfig.stringToType(dict(layerProp))
        layer = Vector(vectorProp)
        if not layer:
            return ReturnCode.CREATE_LAYER_ERROR
        self.mapContainer.addLayer(layer)

        self.returnCode = ReturnCode.SUCCESS

    @pyqtSlot(dict)
    def onRasterLayerAdded(self, layerProp):
        rasterProp = MapConfig.stringToType(dict(layerProp))
        layer = Raster(rasterProp)
        if not layer:
            self.returnValue = ReturnCode.CREATE_LAYER_ERROR
            return
        self.mapContainer.addLayer(layer)

        self.returnValue = str(layer.getLayer().id())

    @pyqtSlot(dict)
    def onDelimitedTextLayerAdded(self, layerProp):
        delimitedTextProp = MapConfig.stringToType(dict(layerProp))
        layer = DelimitedText(delimitedTextProp)
        if not layer:
            return ReturnCode.CREATE_LAYER_ERROR
        self.mapContainer.addLayer(layer)

        self.returnCode = ReturnCode.SUCCESS

    @pyqtSlot(dict)
    def onLayerRemoved(self, layerProp):
        prop = dict(layerProp)
        layerId = prop["layerId"]
        gbsRemoveLayerById(layerId)

        self.returnValue = ReturnCode.SUCCESS

    @pyqtSlot()
    def onGetSelectedAttributes(self):
        pass

    """Public Api functions for rpc call
    """
    def gbsAddVectorLayerWrapper(self, layerProp):
        """ create and add a vector layer to  map container
        """
        self.vectorLayerAdded.emit(layerProp)
        return self.returnCode

    def gbsAddRasterLayerWrapper(self, layerProp):
        """create and add a raster layer to  map container
        """
        self.rasterLayerAdded.emit(layerProp)
        return self.returnValue

    def gbsAddDelimitedTextLayerWrapper(self, layerProp):
        """ create and add a DelimitedText layer to  map container
        """
        self.delimitedTextLayerAdded.emit(layerProp)
        return self.returnCode

    def gbsRemoveLayerWrapper(self, layerProp):
        """ remove layer from  map container
        """
        self.layerRemoved.emit(layerProp)
        return self.returnValue

    def gbsGetSelectedAttributesWrapper(self):
        self.getSelectedAttributes.emit()
        return self.returnValue

def main(argv):
    # create Qt application
    app = QApplication(argv)

    # Initialize gabbs maps libraries
    gbsLoadLibrary()

    wndId = int(sys.argv[1])
    configFile = sys.argv[2]

    wnd = MapWidget(wndId, configFile)
    # wnd.move(100,100)
    #wnd.resize(300, 300)
    wnd.show()

    # run!
    retval = app.exec_()
  
    # Exit gabbs maps libraries
    gbsUnloadLibrary()

    sys.exit(retval)

if __name__ == "__main__":
    main(sys.argv)

