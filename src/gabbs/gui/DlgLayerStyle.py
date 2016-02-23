# -*- coding: utf-8 -*-

"""
Overlay.py  -  overlay file for geohub maps

======================================================================
AUTHOR:  Wei Wan, Purdue University

EMAIL:   rcac-help@purdue.edu

Copyright (c) 2016  Purdue University

See the file "license.terms" for information on usage and
redistribution of this file, and for a DISCLAIMER OF ALL WARRANTIES.

======================================================================

"""

from PyQt4.QtCore import Qt, SIGNAL, QVariant
from PyQt4.QtGui import QDialog, QColorDialog
from qgis.core import *
#from qgis.gui import *

from gabbs.MapUtils import iface, debug_trace
from gabbs.gui.ui_DlgLayerStyle import Ui_DlgLayerStyle

class DlgLayerStyle(QDialog, Ui_DlgLayerStyle):
    """ Open a dialog to manage the layer properties """
    def __init__(self, parent, layer):
        self.parent = parent
        QDialog.__init__(self, self.parent)
        self.setupUi(self)
        self.layer = layer
        self.color = self.getSimpleLabelColor()
        self.colorChanged = False
        self.transparency = self.getTransparency()

        self.btnChangeColor.clicked.connect(self.changeColorOnClicked)
        self.connect(self, SIGNAL( "accepted()" ), self.apply)
        self.connect(self, SIGNAL( "rejected()" ), self.close)

        if not self.color:
            self.btnChangeColor.setEnabled(False)

    def getTransparency(self):
        transparency = 0
        if self.layer.type() == QgsMapLayer.VectorLayer:
            transparency = self.layer.layerTransparency()
        elif self.layer.type() == QgsMapLayer.RasterLayer:
            opacity = self.layer.renderer().opacity()
            transparency = int((1 - opacity) * 100)
        self.sliderTransparency.setSliderPosition(transparency)
        return transparency

    def getSimpleLabelColor(self):
        if self.layer.type() == QgsMapLayer.VectorLayer:
            rederer = self.layer.rendererV2()
            # only work for QgsSingleSymbolRendererV2
            if rederer.type() == 'singleSymbol':
                qcolor = rederer.symbols()[ 0 ].color()
                color = str(qcolor.name())
                self.labelColorDisplay.setStyleSheet( \
                                           "QLabel { background-color: " + color + "; }")
                return qcolor
            else:
                return None
        else:
            return None

    def changeColorOnClicked(self):
        qcolor = QColorDialog.getColor(self.color, self.parent)
        if qcolor.isValid():
            color = str(qcolor.name())
            self.labelColorDisplay.setStyleSheet( \
                                       "QLabel { background-color: " + color + "; }")
            if self.color != qcolor:
                self.colorChanged = True
                self.color = qcolor

    def apply( self ): 
        flag = False
        """ Apply the new style to the layer """
        transparency = self.sliderTransparency.sliderPosition()
        if transparency != self.transparency:
            if self.layer.type() == QgsMapLayer.VectorLayer:
                self.layer.setLayerTransparency(transparency)
            elif self.layer.type() == QgsMapLayer.RasterLayer:
                opacity = float((100 - transparency) / 100.0)
                self.layer.renderer().setOpacity(opacity)
            flag = True

        """ Apply the new color to the layer """
        if self.colorChanged is True:
            self.layer.rendererV2().symbols()[0].setColor(self.color)
            flag = True

        if flag is True:
            if hasattr(self.layer, "setCacheImage"):
                self.layer.setCacheImage(None)
            self.layer.triggerRepaint()