# -*- coding: utf-8 -*-

"""
ControlProperty.py  -  property data type for map tools

======================================================================
AUTHOR:  Wei Wan, Purdue University

EMAIL:   rcac-help@purdue.edu

Copyright (c) 2016  Purdue University

See the file "license.terms" for information on usage and
redistribution of this file, and for a DISCLAIMER OF ALL WARRANTIES.

======================================================================

"""
class panControlStyle:
    SMALL = 'SMALL'     #displays a mini-pan control (only pan)
    LARGE = 'LARGE'     #displays the standard select control
    DEFAULT = 'DEFAULT' #picks the best select control based on device and map size
    HORIZONTAL_BAR = 'HORIZONTAL_BAR' #display one button for each map type
    DROPDOWN_MENU = 'DROPDOWN_MENU'   #select map type via a dropdown menu

class zoomControlStyle:
    SMALL = 'SMALL'     #displays a mini-zoom control (only + and - buttons)
    LARGE = 'LARGE'     #displays the standard zoom control
    DEFAULT = 'DEFAULT' #picks the best zoom control based on device and map size
    CUSTOM = 'CUSTOM'

class selectControlStyle:
    SMALL = 'SMALL'     #displays a mini-select control (only select rectangle)
    LARGE = 'LARGE'     #displays the standard select control 
    DEFAULT = 'DEFAULT' #picks the best select control based on device and map size
    CUSTOM = 'CUSTOM'

class mapControlStyle:
    SMALL = 'SMALL'     #displays a mini-pan control (only pan)
    LARGE = 'LARGE'     #displays the standard select control
    DEFAULT = 'DEFAULT' #picks the best select control based on device and map size
    HORIZONTAL_BAR = 'HORIZONTAL_BAR' #display one button for each map type
    DROPDOWN_MENU = 'DROPDOWN_MENU'   #select map type via a dropdown menu