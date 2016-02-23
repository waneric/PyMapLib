# -*- coding: utf-8 -*-
"""

Layer.py  -  base layer for gabbs maps

======================================================================
AUTHOR:  Wei Wan, Purdue University

EMAIL:   rcac-help@purdue.edu

Copyright (c) 2016  Purdue University

See the file "license.terms" for information on usage and
redistribution of this file, and for a DISCLAIMER OF ALL WARRANTIES.

======================================================================

"""

class LayerTypeId:
    VECTOR = 0
    RASTER = 1
    POSTGIS = 2
    SPATIAL_LITE = 3
    MSSQL_SPATIAL = 4
    ORACLE_SPATIAL = 5
    WMS = 6
    WCS = 7
    WFS = 8
    DELIMITED_TEXT = 9
    TMS = 10

class LayerTypeName:
    VECTOR = 'VECTOR'
    RASTER = 'RASTER'
    POSTGIS = 'POSTGIS'
    SPATIAL_LITE = 'SPATIAL_LITE'
    MSSQL_SPATIAL = 'MSSQL_SPATIAL'
    ORACLE_SPATIAL = 'ORACLE_SPATIAL'
    WMS = 'WMS'
    WCS = 'WCS'
    WFS = 'WFS'
    DELIMITED_TEXT = 'DELIMITED_TEXT'
    TMS = 'TMS'

class MapTypeId:
    GOOGLE_TERRAIN = 0
    GOOGLE_ROADMAP = 1
    GOOGLE_HYBRID = 2
    GOOGLE_SATELLITE = 3
    OSM = 4
    #OCM => 5,
    #OCM_LANDSCAPE => 6,
    #OCM_PUBLIC_TRANSPORT => 7,
    #YAHOO_STREET => 8,
    #YAHOO_HYBRID => 9,
    #YAHOO_SATELLITE => 10,
    #BING_ROAD => 11,
    #BING_AERIAL => 12,
    #BING_AERIAL_WITH_LABELS => 13,
    #APPLE_IPHOTO => 14

class MapTypeName:
    GOOGLE_TERRAIN = 'GOOGLE_TERRAIN'
    GOOGLE_ROADMAP = 'GOOGLE_ROADMAP'
    GOOGLE_HYBRID = 'GOOGLE_HYBRID'
    GOOGLE_SATELLITE = 'GOOGLE_SATELLITE'
    OSM = 'OSM'
    OCM = 'OCM'
    OCM_LANDSCAPE= 'OCM_LANDSCAPE'
    OCM_TRANSPORT = 'OCM_TRANSPORT'