"""
/***************************************************************************
         Image Clipper - A QGIS plugin to extract (clip) one or more image
                         layers to a new image
                             -------------------
    begin                : 2009-08-28
    copyright            : (C) 2009 by Bob Bruce
    email                : Bob.Bruce at pobox.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# for initing the Image Clipper as plugin in Qgis
def name():
    return "Image Clipper"

def description():
    return "One or more image layers in the project are clipped (extracted) to a new image according to a rectangle drawn by the user"

def qgisMinimumVersion():
    return "1.1.0"

def version():
    return "1.2"

def authorName():
    return "Bob Bruce - Bob.Bruce@pobox.com"

def classFactory(iface):
    from drawingtool import DrawingTool
    return DrawingTool(iface)