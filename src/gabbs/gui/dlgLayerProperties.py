# -*- coding: utf-8 -*-

"""
dlgLayerProperties.py  -  overlay file for geohub maps

======================================================================
AUTHOR:  Wei Wan, Purdue University

EMAIL:   rcac-help@purdue.edu

Copyright (c) 2016  Purdue University

See the file "license.terms" for information on usage and
redistribution of this file, and for a DISCLAIMER OF ALL WARRANTIES.

======================================================================
"""

from PyQt4.QtCore import Qt, SIGNAL, QVariant
from PyQt4.QtGui import QDialog

from gabbs.gui.ui_dlgLayerProperties import Ui_LayerProperties

class LayerProperties( QDialog, Ui_LayerProperties ):
    """ Open a dialog to manage the layer properties """
    def __init__( self, parent, layer ):
        self.parent = parent
        QDialog.__init__( self, self.parent )
        self.setupUi( self )
        self.layer = layer
        self.updateControls()

        self.connect( self.chkScale, SIGNAL( "stateChanged(int)" ), self.chkScaleChanged )
        self.connect( self, SIGNAL( "accepted()" ), self.apply )
        self.connect( self, SIGNAL( "rejected()" ), self.close )

    def updateControls( self ):
        """ Set the appropriate value/state for controls """
        self.txtLayerName.setText( self.layer.name() )

        if self.layer.type() == 0: # Vector Layer
            self.lblDisplayField.setVisible( True )
            self.cboDisplayFieldName.setVisible( True )
            self.cboDisplayFieldName.setEnabled( True )
            """
            self.fields = self.layer.pendingFields().toList()
            for ( key, field ) in self.fields.iteritems():
                #if not field.type() == QVariant.Double:
                    # self.displayName = self.vectorLayer.attributeDisplayName( key )
                self.cboDisplayFieldName.addItem( field.name(), QVariant( key ) )"""

            self.fields = self.layer.pendingFields().toList()
            for field in self.fields:
                #if not field.type() == QVariant.Double:
                    # self.displayName = self.vectorLayer.attributeDisplayName( key )
                self.cboDisplayFieldName.addItem( field.name(), QVariant( field.name() ) )

            idx = self.cboDisplayFieldName.findText( self.layer.displayField() )
            self.cboDisplayFieldName.setCurrentIndex( idx )
        else:
            self.lblDisplayField.setVisible( False )
            self.cboDisplayFieldName.setVisible( False )
            self.cboDisplayFieldName.setEnabled( False )

        if self.layer.hasScaleBasedVisibility():
            self.chkScale.setCheckState( Qt.Checked )
            self.chkScaleChanged( 1 ) 
            self.initialScaleDependency = True
        else:
            self.chkScale.setCheckState( Qt.Unchecked )
            self.chkScaleChanged( 0 ) 
            self.initialScaleDependency = False

        self.initialMaxScale = self.layer.minimumScale() # To know if refresh the canvas
        self.initialMinScale = self.layer.maximumScale()
        self.maxScaleSpinBox.setValue( self.layer.minimumScale() )
        self.minScaleSpinBox.setValue( self.layer.maximumScale() )

    def chkScaleChanged( self, state ):
        """ Slot. """
        if state:
            self.lblMaxScale.setEnabled( True )
            self.lblMinScale.setEnabled( True )
            self.maxScaleSpinBox.setEnabled( True )
            self.minScaleSpinBox.setEnabled( True )            
        else:
            self.lblMaxScale.setEnabled( False )
            self.lblMinScale.setEnabled( False )
            self.maxScaleSpinBox.setEnabled( False )
            self.minScaleSpinBox.setEnabled( False )            

    def apply( self ):
        """ Apply the new symbology to the vector layer """
        newLayerName = self.txtLayerName.text()
        if newLayerName:
            if not newLayerName == self.layer.name():
                self.layer.setLayerName( newLayerName )
                self.emit( SIGNAL( "layerNameChanged(PyQt_PyObject)" ), self.layer )

        if self.cboDisplayFieldName.isEnabled():
            self.layer.setDisplayField( self.cboDisplayFieldName.currentText() )

        if self.chkScale.checkState() == Qt.Checked:
            self.layer.toggleScaleBasedVisibility( True )
            self.layer.setMaximumScale( self.minScaleSpinBox.value() )
            self.layer.setMinimumScale( self.maxScaleSpinBox.value() )
            finalScaleDependency = True
        else:
            self.layer.toggleScaleBasedVisibility( False )
            finalScaleDependency = False

        if ( not self.initialScaleDependency == finalScaleDependency ) or \
           ( finalScaleDependency and ( ( not self.initialMaxScale == self.maxScaleSpinBox.value() ) or \
            ( not self.initialMinScale == self.minScaleSpinBox.value() ) ) ):
            self.parent.canvas.refresh() # Scale dependency changed, so refresh

    def mostrar( self ):
        """ Show the modal dialog """
        self.exec_()

