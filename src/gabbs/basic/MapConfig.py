# -*- coding: utf-8 -*-

"""

MapConfig.py  -  Config class for map canvas

======================================================================
AUTHOR:  Wei Wan, Purdue University

EMAIL:   rcac-help@purdue.edu

Copyright (c) 2016  Purdue University

See the file "license.terms" for information on usage and
redistribution of this file, and for a DISCLAIMER OF ALL WARRANTIES.

======================================================================
"""
import os

from gabbs.tools.xmltodict import parse as parseXmlToDict

class MapConfig(object):
    def __init__(self, filePath):
        object.__init__(self)
        self.mapProperty = self.getConfig(filePath)

    @staticmethod
    def isInt(s):
        try:
            return int(s)
        except ValueError:
            try:
                return float(s)
            except ValueError:
                return s

    @staticmethod
    def getItemValue(strDict):
        for key, val in strDict.items():
            #if not isinstance(val, str):
            #    continue
            if val == 'True':
                strDict[key] = True
            elif val == 'False':
                strDict[key] = False
            elif isinstance(val, str):
                if val.isdigit():
                    strDict[key] = MapConfig.isInt(val)
            elif '$TOOL_REPO_PATH' in val:
                strDict[key] = val.replace("$TOOL_REPO_PATH", os.environ['TOOL_REPO_PATH'])
            elif '$HOME' in val:
                strDict[key] = val.replace("$HOME", os.environ['HOME'])
        return strDict

    @staticmethod
    def stringToType(strDict):
        for key, val in strDict.items():
            if not isinstance(val, str):
                continue
            if val == 'True':
                strDict[key] = True
            elif val == 'False':
                strDict[key] = False
            elif isinstance(val, str):
                if val.isdigit():
                    strDict[key] = MapConfig.isInt(val)
            elif '$TOOL_REPO_PATH' in val:
                strDict[key] = val.replace("$TOOL_REPO_PATH", os.environ['TOOL_REPO_PATH'])
                print os.environ['TOOL_REPO_PATH']
            elif '$HOME' in val:
                strDict[key] = val.replace("$HOME", os.environ['HOME'])
                print os.environ['HOME']
        return strDict

    def getConfig(self, filePath):
        try:
            f = open(filePath, 'r')
            conf = f.read()
        except:
            return None
        finally:
            f.close()
        r = parseXmlToDict(conf)
        return r

    def getMapContainerConfig(self):
        emptyDict = {}
        try:
            root = self.mapProperty["gabbsmap"]["container"]
            root = MapConfig.getItemValue(root)
        except KeyError:
            return emptyDict
        return root

    def getMapConfig(self):
        emptyDict = {}
        try:
            root = self.mapProperty["gabbsmap"]["layer"]["map"]
            root = MapConfig.getItemValue(root)
        except KeyError:
            return emptyDict
        return root

    def getVectorConfig(self):
        emptyDict = {}
        try:
            root = self.mapProperty["gabbsmap"]["layer"]["vector"]
            root = MapConfig.getItemValue(root)
        except KeyError:
            return emptyDict
        return root

    def getRasterConfig(self):
        emptyDict = {}
        try:
            root = self.mapProperty["gabbsmap"]["layer"]["raster"]
            root = self.getItemValue(root)
        except KeyError:
            return emptyDict
        return root

    def getDelimitedTextConfig(self):
        emptyDict = {}
        try:
            root = self.mapProperty["gabbsmap"]["layer"]["delimitedtext"]
            root = MapConfig.getItemValue(root)
        except KeyError:
            return emptyDict
        return root