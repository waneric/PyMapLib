# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
"""
RpcServer.py  -  RPC Server to show geohub.maps library
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
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
#from threading import Thread
from PyQt4.QtCore import (QThread)
#from qgis.gui import *

class ServerThread(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.daemon = True
        self.host = "localhost"
        self.port = 6001
        self.requestHandler = SimpleXMLRPCRequestHandler
        self.xmlRpcServer = SimpleXMLRPCServer((self.host, self.port), self.requestHandler)

    def run(self):
        self.xmlRpcServer.serve_forever()