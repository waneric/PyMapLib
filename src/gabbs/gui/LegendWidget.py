# -*- coding: utf-8 -*-

"""
legendwidget.py  -  legendwidget file for gabbs maps

======================================================================
AUTHOR:  Wei Wan, Purdue University

EMAIL:   rcac-help@purdue.edu

Copyright (c) 2016  Purdue University

See the file "license.terms" for information on usage and
redistribution of this file, and for a DISCLAIMER OF ALL WARRANTIES.

======================================================================

"""

from os.path import isfile

from PyQt4.QtCore import Qt, SIGNAL, QPoint, QSize, QFileInfo, QSettings, QVariant, QMetaType, pyqtSlot
from PyQt4.QtGui import ( QTreeWidget, QTreeWidgetItem, QPixmap, QIcon, QFont, QColor,
                          QMenu, QColorDialog, QImage, QFileDialog, QMessageBox )

from qgis.core import QGis, QgsMapLayerRegistry
from qgis.gui import QgsMapCanvasLayer
from qgis.core import *
from gabbs.gui.dlgLayerProperties import LayerProperties
from gabbs.gui.DlgLayerStyle import DlgLayerStyle

import gabbs.resources_rc
from gabbs.MapUtils import iface, debug_trace
#from resources_rc import *

resources_prefix = ":/gabbs/resources/img/"

class LegendItem(QTreeWidgetItem):
    """ Provide a widget to show and manage the properties of one single layer """
    def __init__(self, parent, canvasLayer):
        QTreeWidgetItem.__init__(self)
        self.legend = parent
        self.canvasLayer = canvasLayer
        self.canvasLayer.layer().setLayerName( self.legend.normalizeLayerName( unicode( self.canvasLayer.layer().name() ) ) )
        self.setText(0, self.canvasLayer.layer().name())
        self.isVect = (self.canvasLayer.layer().type() == 0) # 0: Vector, 1: Raster
        self.layerId = self.canvasLayer.layer().id()
        self.setSizeHint(0, QSize(24, 24))
        self.setCheckState(0, Qt.Checked)

        pm = QPixmap(22, 22)
        icon = QIcon()

        if self.isVect:
            renderer = self.canvasLayer.layer().rendererV2() 
            sym = renderer.symbols()[0]
            img = QImage(sym.asImage(QSize(22, 22)))
            pix = pm.fromImage(img)
            icon.addPixmap(pix, QIcon.Normal, QIcon.On)
            self.vectorLayerSymbology(self.canvasLayer.layer())
        else:
            pm = self.canvasLayer.layer().previewAsPixmap(QSize(22, 22))
            icon.addPixmap(pm)
            self.rasterLayerSymbology(self.canvasLayer.layer())

        self.setIcon(0, icon)
        self.setToolTip(0, self.canvasLayer.layer().attribution())
        layerFont = QFont()
        layerFont.setBold(True)
        self.setFont(0, layerFont)

    def nextSibling( self ):
        """ Return the next layer item """
        return self.legend.nextSibling( self )

    def storeAppearanceSettings( self ):
        """ Store the appearance of the layer item """
        self.__itemIsExpanded = self.isExpanded()

    def restoreAppearanceSettings( self ):
        """ Restore the appearance of the layer item """
        self.setExpanded( self.__itemIsExpanded )

    def changeSymbologySettings(self, theMapLayer, itemList):
        if not theMapLayer:
            return
        # Remove previous symbology items
        self.takeChildren()
        # Add the new symbology items
        for i in range(len(itemList)):
            self.child = QTreeWidgetItem(self)
            self.child.setSizeHint(0, QSize(18, 18))
            self.child.setText(0, unicode(itemList[i][0]))
            iconChild = QIcon()
            iconChild.addPixmap(itemList[i][1])
            self.child.setIcon(0, iconChild)

    def vectorLayerSymbology(self, layer):
        renderer = layer.rendererV2()
        # Do nothing if only single symbol
        if renderer.type() == "singleSymbol":
            return

        # Add the new items
        itemList = [] # Simbology List
        label = ''
        sym = renderer.symbols()

        for idx, it in enumerate(sym):
            values = ''
            if renderer.type() == "graduatedSymbol":
                rng = renderer.ranges()[idx]
                label = rng.label()
                if not label.isEmpty():
                    values += label
            elif renderer.type() == "categorizedSymbol":
                cat = renderer.categories()[idx]
                label = cat.label()
                if not label.isEmpty():
                    values += label
            img = QImage()
            img = it.asImage(QSize(16, 16))
            pix = QPixmap(16, 16)
            pix = QPixmap().fromImage(img)
            itemList.append([values, pix])

        self.changeSymbologySettings(layer, itemList)

    def rasterLayerSymbology(self, layer):
        # Add the new items
        itemList = []
        label = ''
        color = QColor()
        renderer = layer.renderer()
        rtype = renderer.type()
        #if rtype == "paletted":
        #   rtype == "singlebandgray"
        if rtype == "singlebandpseudocolor":
            shader = renderer.shader().rasterShaderFunction()
            if isinstance(shader, QgsColorRampShader):
                colorRampItems = shader.colorRampItemList()
                for it in colorRampItems:
                    # Get Qpair
                    label = it.label
                    color = it.color
                    pix = QPixmap(16, 16)
                    pix.fill(color)
                    itemList.append([label, pix])

        self.changeSymbologySettings(layer, itemList)


class Legend( QTreeWidget ):
    """
      Provide a widget that manages map layers and their symbology as tree items
    """
    def __init__(self, parent):
        QTreeWidget.__init__(self, parent)
        self.setObjectName("theMapLegend")
        self.pyQGisApp = parent
        self.canvas = iface.mapCanvas
        self.layers = self.getLayerSet()
        self.propertyDlgFlag = False
        self.bMousePressedFlag = False
        self.itemBeingMoved = None

        # QTreeWidget properties
        self.setSortingEnabled(False)
        self.setDragEnabled(False)
        self.setAutoScroll(True)
        self.setHeaderHidden(True)
        self.setRootIsDecorated(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        self.connect(self, SIGNAL("customContextMenuRequested(QPoint)" ),
                     self.showMenu)
        self.connect(QgsMapLayerRegistry.instance(), SIGNAL("layerWasAdded(QgsMapLayer *)"),
                     self.addLayerToLegend)
        self.connect(QgsMapLayerRegistry.instance(), SIGNAL("removedAll()"),
                     self.removeAll)
        self.connect(self, SIGNAL("itemChanged(QTreeWidgetItem *,int)"),
                     self.updateLayerStatus)
        self.connect(self, SIGNAL("currentItemChanged(QTreeWidgetItem *, QTreeWidgetItem *)"),
                     self.currentItemChanged)

    def getLayers(self):
        lyrs = []
        for lyr in self.layers:
            lyrs.append(lyr.layer())
        return lyrs

    def setCanvas( self, canvas ):
        """ Set the base canvas """
        self.canvas = canvas

    def setPropertyDlg(self, flag):
        self.propertyDlgFlag = flag

    def showMenu( self, pos ):
        """ Show a context menu for the active layer in the legend """
        if not self.propertyDlgFlag:
            return

        item = self.itemAt( pos )
        if item:
            if self.isLegendLayer( item ):
                self.setCurrentItem( item )
                self.menu = self.getMenu( item.isVect, item.canvasLayer )
                self.menu.popup( QPoint( self.mapToGlobal( pos ).x() + 5, self.mapToGlobal( pos ).y() ) )

    def getMenu( self, isVect, canvasLayer ):
        """ Create a context menu for a layer """
        menu = QMenu()
        #menu.addAction(QIcon( resources_prefix + "mActionZoomToLayer.png" ), "Zoom to layer extent", self.zoomToLayer)

        self.actionOV = menu.addAction("Show in overview", self.showInOverview)
        self.actionOV.setCheckable(True)
        self.actionOV.setChecked(canvasLayer.isInOverview())

        menu.addSeparator()
        menu.addAction(QIcon(resources_prefix + "mIconProperties.png" ), "Properties...", self.setLayerProperties)
        menu.addAction(QIcon( resources_prefix + "symbology.png" ), "Style...", self.setLayerStyle)

        menu.addAction(QIcon( resources_prefix + "mActionFileOpen.png" ), "Load style...", self.loadSymbologyFile)
        menu.addAction(QIcon( resources_prefix + "mActionFileSave.png" ), "Save style as...", self.saveSymbologyFile)

        menu.addSeparator()
        menu.addAction(QIcon( resources_prefix + "collapse.png" ), "Collapse all", self.collapseAll)
        menu.addAction(QIcon( resources_prefix + "expand.png" ), "Expand all", self.expandAll)

        menu.addSeparator()
        menu.addAction(QIcon( resources_prefix + "removeLayer.png" ), "Remove layer", self.removeCurrentLayer)
        return menu

    def mousePressEvent(self, event):
        """ Mouse press event to manage the layers drag """
        if ( event.button() == Qt.LeftButton ):
            self.lastPressPos = event.pos()
            self.bMousePressedFlag = True
        QTreeWidget.mousePressEvent( self, event )

    def mouseMoveEvent(self, event):
        """ Mouse move event to manage the layers drag """
        if ( self.bMousePressedFlag ):
            # Set the flag back such that the else if(mItemBeingMoved)
            # code part is passed during the next mouse moves
            self.bMousePressedFlag = False

            # Remember the item that has been pressed
            item = self.itemAt( self.lastPressPos )
            if ( item ):
                if ( self.isLegendLayer( item ) ):
                    self.itemBeingMoved = item
                    self.storeInitialPosition() # Store the initial layers order
                    self.setCursor( Qt.SizeVerCursor )
                else:
                    self.setCursor( Qt.ForbiddenCursor )
        elif ( self.itemBeingMoved ):
            p = QPoint( event.pos() )
            self.lastPressPos = p

            # Change the cursor
            item = self.itemAt( p )
            origin = self.itemBeingMoved
            dest = item

            if not item:
                self.setCursor( Qt.ForbiddenCursor )

            if ( item and ( item != self.itemBeingMoved ) ):
                if ( self.yCoordAboveCenter( dest, event.y() ) ): # Above center of the item
                    if self.isLegendLayer( dest ): # The item is a layer
                        if ( origin.nextSibling() != dest ):
                            self.moveItem( dest, origin )
                        self.setCurrentItem( origin )
                        self.setCursor( Qt.SizeVerCursor )
                    else:
                        self.setCursor( Qt.ForbiddenCursor )
                else: # Below center of the item
                    if self.isLegendLayer( dest ): # The item is a layer
                        if ( self.itemBeingMoved != dest.nextSibling() ):
                            self.moveItem( origin, dest )
                        self.setCurrentItem( origin )
                        self.setCursor( Qt.SizeVerCursor )
                    else:
                        self.setCursor( Qt.ForbiddenCursor )

    def mouseReleaseEvent( self, event ):
        """ Mouse release event to manage the layers drag """
        QTreeWidget.mouseReleaseEvent( self, event )
        self.setCursor( Qt.ArrowCursor )
        self.bMousePressedFlag = False

        if ( not self.itemBeingMoved ):
            #print "*** Legend drag: No itemBeingMoved ***"
            return

        dest = self.itemAt( event.pos() )
        origin = self.itemBeingMoved
        if ( ( not dest ) or ( not origin ) ): # Release out of the legend
            self.checkLayerOrderUpdate()
            return

        self.checkLayerOrderUpdate()
        self.itemBeingMoved = None

    @pyqtSlot(QgsMapLayer)
    def addLayerToLegend(self, canvasLayer):
        """ Slot. Create and add a legend item based on a layer """
        legendLayer = LegendItem(self, QgsMapCanvasLayer(canvasLayer))
        self.addLayer(legendLayer)

    def addLayer(self, legendLayer):
        """ Add a legend item to the legend widget """
        self.insertTopLevelItem(0, legendLayer)
        #self.expandItem(legendLayer)
        self.setCurrentItem(legendLayer)
        self.updateLayerSet()

    def updateLayerStatus( self, item ):
        """ Update the layer status """
        if ( item ):
            if self.isLegendLayer( item ): # Is the item a layer item?
                for i in self.layers:
                    if i.layer().id() == item.layerId:
                        if item.checkState( 0 ) == Qt.Unchecked:
                            i.setVisible( False )
                        else:
                            i.setVisible( True )
                        self.canvas.setLayerSet( self.layers )
                        return

    def currentItemChanged( self, newItem, oldItem ):
        """ Slot. Capture a new currentItem and emit a SIGNAL to inform the new type 
            It could be used to activate/deactivate GUI buttons according the layer type
        """
        layerType = None

        if self.currentItem():
            if self.isLegendLayer( newItem ):
                layerType = newItem.canvasLayer.layer().type()
                self.canvas.setCurrentLayer( newItem.canvasLayer.layer() )
            else:
                layerType = newItem.parent().canvasLayer.layer().type()
                self.canvas.setCurrentLayer( newItem.parent().canvasLayer.layer() )

        self.emit( SIGNAL( "activeLayerChanged" ), layerType )

    def zoomToLayer(self):
        """ Slot. Manage the zoomToLayer action in the context Menu """
        self.zoomToLegendLayer(self.currentItem())

    def removeCurrentLayer(self):
        """ Slot. Manage the removeCurrentLayer action in the context Menu """
        QgsMapLayerRegistry.instance().removeMapLayer( self.currentItem().canvasLayer.layer().id() )
        self.removeLegendLayer( self.currentItem() )
        self.updateLayerSet()

    # public
    def removeLayer(self, layerId):
        """ Manage the remove layer action based on layer id"""
        QgsMapLayerRegistry.instance().removeMapLayer(layerId)
        root = self.invisibleRootItem()
        child_count = root.childCount()
        for i in range(child_count):
            item = root.child(i)
            if item.layerId == layerId:
                self.removeLegendLayer(item)
                self.updateLayerSet()
                return

    # public
    def hideLayer(self, layerId):
        """ Hide the layer based on layer id"""
        root = self.invisibleRootItem()
        child_count = root.childCount()
        for i in range(child_count):
            item = root.child(i)
            if item.layerId == layerId:
                if item.checkState( 0 ) == Qt.Checked:
                    item.setCheckState(0, Qt.Unchecked)
                    self.updateLayerStatus(item)
                return

    # public
    def showLayer(self, layerId):
        """ Show the layer based on layer id"""
        root = self.invisibleRootItem()
        child_count = root.childCount()
        for i in range(child_count):
            item = root.child(i)
            if item.layerId == layerId:
                if item.checkState( 0 ) == Qt.Unchecked:
                    item.setCheckState(0, Qt.Checked)
                    self.updateLayerStatus(item)
                return

    def setLayerProperties(self):
        """ Slot. Open a dialog to set the layer properties """
        if self.currentItem():
            item = self.currentItem()
            self.dlgProperties = None
            self.dlgProperties = LayerProperties( self.pyQGisApp, item.canvasLayer.layer() )
            self.connect( self.dlgProperties, SIGNAL( "layerNameChanged(PyQt_PyObject)" ), self.updateLayerName )
            self.dlgProperties.mostrar()

    def updateLayerName(self, layer):
        """ Update the layer name in the legend """
        for i in range( self.topLevelItemCount() ):
            if self.topLevelItem( i ).layerId == layer.id():
                layer.setLayerName( self.createUniqueName( unicode( layer.name() ) ) )
                self.topLevelItem( i ).setText( 0, layer.name() )
                break

    def setLayerStyle(self):
        """ Slot. Open a dialog to set the layer styles """
        if self.currentItem():
            item = self.currentItem()
            dlg = DlgLayerStyle(self.pyQGisApp, item.canvasLayer.layer())
            dlg.exec_()

    def loadSymbologyFile(self):
        """ Load a QML file to set the layer style """
        settings = QSettings()
        ultimaRutaQml = settings.value( 'Paths/qml', QVariant('.') ).toString()
        symPath = QFileDialog.getOpenFileName(self, "Open a style file (.qml)",
            ultimaRutaQml, "QGIS Layer Style File (*.qml)")

        if isfile(symPath):
            layer = self.currentItem().canvasLayer.layer()
            res = layer.loadNamedStyle(symPath)
            if res[1]:
                self.refreshLayerSymbology(self.currentItem().canvasLayer.layer())
                self.showMessage(self, 'Load style',
                    'New style has been applied to the layer ' +
                        self.currentItem().text(0) + '.', QMessageBox.Information )
                # Immediately refresh layer
                if hasattr(layer, "setCacheImage"):
                    layer.setCacheImage(None)
                layer.triggerRepaint()
            else:
                self.showMessage( self, 'Load style',
                    'Error loading style file. Please check if match the layer ' + 
                        self.currentItem().text(0) + '.', QMessageBox.Warning )

            symInfo = QFileInfo(symPath)
            settings.setValue('Paths/qml', QVariant( symInfo.absolutePath()))

    def saveSymbologyFile(self):
        """ Save a QML file to set the layer style """
        settings = QSettings()
        ultimaRutaQml = settings.value( 'Paths/qml', QVariant('.') ).toString()
        symPath = QFileDialog.getSaveFileName( self, "Save layer properties as a style file",
            ultimaRutaQml, "QGIS Layer Style File (*.qml)" )

        if symPath:
            symInfo = QFileInfo( symPath )
            settings.setValue( 'Paths/qml', QVariant( symInfo.absolutePath() ) )

            if not symPath.toUpper().endsWith( '.QML' ):
                symPath += '.qml'

            res = self.currentItem().canvasLayer.layer().saveNamedStyle( symPath )

            if res[ 1 ]:
                self.refreshLayerSymbology( self.currentItem().canvasLayer.layer() )
                self.showMessage( self, 'Save style file',
                    'The style file has been saved succesfully.',
                    QMessageBox.Information )
            else:
                self.showMessage( self, 'Save style file',
                    res[ 0 ], QMessageBox.Warning )

    def showMessage( self, parent, title, desc, icon=None ):
        """ Method to create messages to be shown to the users """
        msg = QMessageBox( parent )
        msg.setText( desc )
        msg.setWindowTitle( title )
        if icon:
            msg.setIcon( icon )
        msg.addButton( 'Close', QMessageBox.RejectRole )
        msg.exec_()

    def zoomToLegendLayer( self, legendLayer ):
        """ Zoom the map to a layer extent """
        for i in self.layers:
            if i.layer().id() == legendLayer.layerId:
                srcExtent = i.layer().extent()
                x1 = srcExtent.xMaximum()
                y1 = srcExtent.yMaximum()
                x2 = srcExtent.xMinimum()
                y2 = srcExtent.yMinimum()
                point1 = self.canvas.getCoordinateTransform().toMapCoordinates(x1, y1)
                point2 = self.canvas.getCoordinateTransform().toMapCoordinates(x2, y2)
                destExtent = QgsRectangle(point1, point2)
                destExtent.scale(1.05)
                self.canvas.setExtent(destExtent)
                self.canvas.refresh()
                break

    def removeLegendLayer( self, legendLayer ):
        """ Remove a layer item in the legend """
        if self.topLevelItemCount() == 1:
            self.clear()
        else: # Manage the currentLayer before the remove
            indice = self.indexOfTopLevelItem( legendLayer )
            if indice == 0:
                newCurrentItem = self.topLevelItem( indice + 1 )
            else:
                newCurrentItem = self.topLevelItem( indice - 1 )

            self.setCurrentItem( newCurrentItem )
            self.takeTopLevelItem( self.indexOfTopLevelItem( legendLayer ) )

    def setStatusForAllLayers( self, visible ):
        """ Show/Hide all layers in the map """
        # Block SIGNALS to avoid setLayerSet for each item status changed
        self.blockSignals(True)

        status = Qt.Checked if visible else Qt.Unchecked
        for i in range( self.topLevelItemCount() ):
            self.topLevelItem( i ).setCheckState( 0, status )
            self.topLevelItem( i ).canvasLayer.setVisible( visible )

        self.blockSignals(False)

        self.updateLayerSet() # Finally, update the layer set

    def removeAll( self ):
        """ Remove all legend items """
        self.clear()
        self.updateLayerSet()

    def allLayersInOverview( self, visible ):
        """ Show/Hide all layers in Overview """
        for i in range( self.topLevelItemCount() ):
            self.topLevelItem( i ).canvasLayer.setInOverview( visible )
        self.updateLayerSet()
        self.canvas.updateOverview()

    def showInOverview( self ):
        """ Toggle the active layer in Overview Map """
        self.currentItem().canvasLayer.setInOverview( not( self.currentItem().canvasLayer.isInOverview() ) )
        self.updateLayerSet()
        self.canvas.updateOverview()

    def updateLayerSet( self ):
        """ Update the LayerSet and set it to canvas """
        self.layers = self.getLayerSet()
        self.canvas.setLayerSet( self.layers )

    def getLayerSet( self ):
        """ Get the LayerSet by reading the layer items in the legend """
        layers = []
        for i in range( self.topLevelItemCount() ):
            layers.append( self.topLevelItem( i ).canvasLayer )
        return layers

    def activeLayer( self ):
        """ Return the selected layer """
        if self.currentItem():
            if self.isLegendLayer( self.currentItem() ):
                return self.currentItem().canvasLayer
            else:
                return self.currentItem().parent().canvasLayer
        else:
            return None

    def collapseAll( self ):
        """ Collapse all layer items in the legend """
        for i in range( self.topLevelItemCount() ):
            item = self.topLevelItem( i )
            self.collapseItem( item )

    def expandAll( self ):
        """ Expand all layer items in the legend """
        for i in range( self.topLevelItemCount() ):
            item = self.topLevelItem( i )
            self.expandItem( item )

    def isLegendLayer( self, item ):
        """ Check if a given item is a layer item """
        return not item.parent()

    def storeInitialPosition( self ):
        """ Store the layers order """
        self.__beforeDragStateLayers = self.getLayerIDs()

    def getLayerIDs( self ):
        """ Return a list with the layers ids """
        layers = []
        for i in range( self.topLevelItemCount() ):
            item = self.topLevelItem( i )
            layers.append( item.layerId )
        return layers

    def nextSibling( self, item ):
        """ Return the next layer item based on a given item """
        for i in range( self.topLevelItemCount() ):
            if item.layerId == self.topLevelItem( i ).layerId:
                break
        if i < self.topLevelItemCount():                                            
            return self.topLevelItem( i + 1 )
        else:
            return None

    def moveItem( self, itemToMove, afterItem ):
        """ Move the itemToMove after the afterItem in the legend """
        itemToMove.storeAppearanceSettings() # Store settings in the moved item
        self.takeTopLevelItem( self.indexOfTopLevelItem( itemToMove ) )
        self.insertTopLevelItem( self.indexOfTopLevelItem( afterItem ) + 1, itemToMove )
        itemToMove.restoreAppearanceSettings() # Apply the settings again

    def checkLayerOrderUpdate( self ):
        """
            Check if the initial layers order is equal to the final one.
            This is used to refresh the legend in the release event.
        """
        self.__afterDragStateLayers = self.getLayerIDs()
        if self.__afterDragStateLayers != self.__beforeDragStateLayers:
            self.updateLayerSet()
            #print "*** Drag legend layer done. Updating canvas ***"

    def yCoordAboveCenter( self, legendItem, ycoord ):
        """
            Return a bool to know if the ycoord is in the above center of the legendItem

            legendItem: The base item to get the above center and the below center
            ycoord: The coordinate of the comparison
        """
        rect = self.visualItemRect( legendItem )
        height = rect.height()
        top = rect.top()
        mid = top + ( height / 2 )
        if ( ycoord > mid ): # Bottom, remember the y-coordinate increases downwards
            return False
        else: # Top
            return True

    def normalizeLayerName( self, name ):
        """ Create an alias to put in the legend and avoid to repeat names """
        # Remove the extension
        if len( name ) > 4:
            if name[ -4 ] == '.':
                name = name[ :-4 ]
        return self.createUniqueName( name )

    def createUniqueName( self, name ):
        """ Avoid to repeat layers names """
        import re
        name_validation = re.compile( "\s\(\d+\)$", re.UNICODE ) # Strings like " (1)"

        bRepetida = True
        i = 1
        while bRepetida:
            bRepetida = False

            # If necessary add a sufix like " (1)" to avoid to repeat names in the legend
            for j in range( self.topLevelItemCount() ):
                item = self.topLevelItem( j )
                if item.text( 0 ) == name:
                    bRepetida = True
                    if name_validation.search( name ): # The name already have numeration
                        name = name[ :-4 ]  + ' (' + str( i ) + ')'
                    else: # Add numeration because the name doesn't have it
                        name = name + ' (' + str( i ) + ')'
                    i += 1
        return name

    def refreshLayerSymbology( self, layer ):
        """ Refresh the layer symbology. For plugins. """
        for i in range( self.topLevelItemCount() ):
            item = self.topLevelItem( i )
            if layer.id() == item.layerId:
                if layer.type() == QgsMapLayer.VectorLayer:
                    item.vectorLayerSymbology(layer)
                elif layer.type() == QgsMapLayer.RasterLayer:
                    item.rasterLayerSymbology(layer)
                self.canvas.refresh()
                break

    def removeLayers( self, layerIds ):
        """ Remove layers from their ids. For plugins. """
        for layerId in layerIds:
            QgsMapLayerRegistry.instance().removeMapLayer( layerId )

            # Remove the legend item
            for i in range( self.topLevelItemCount() ):
                item = self.topLevelItem( i )
                if layerId == item.layerId:
                    self.removeLegendLayer( item )
                    break

        self.updateLayerSet()
