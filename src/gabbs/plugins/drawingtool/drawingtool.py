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

    Author: Wei Wan at purdue.rcac.edu
    Date: 2015-11-06
    Version: 0.1.0
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

from DrawingMapTool import DrawingMapTool

import resources_rc

class DrawingTool:
    def __init__(self, iface):
        self.iface = iface
        self.canvas = iface.mapCanvas
        self.window = iface.mainWindow

    def initGui(self):
        self.action = QAction(QIcon(":/plugins/drawingtool/icon.png"), "Drawing Tool", self.window)
        self.action.setCheckable(True)
        QObject.connect(self.action, SIGNAL("triggered()"), self.drawing)

        self.iface.addToolBarIcon(self.action)

        self.tool = DrawingMapTool(self.canvas)
        self.tool.setAction(self.action)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)

    def drawing(self):
        self.canvas.setMapTool(self.tool)
