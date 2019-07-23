#!/usr/bin/python
# -*- coding:utf8 -*-

import os
import re
import collections
from static_data_defines import StaticDataFileInfo


class StaticFileScanner(object):
    '文件搜索静态数据结构'

    def __init__(self, scanPath, matchPattern, leftTrip=""):
        self._scanPath = scanPath
        self._matchPattern = matchPattern
        self._staticFileInfo = collections.OrderedDict()
        self._reXMLPatter = re.compile(matchPattern)
        self._leftTrip = leftTrip

    def scan(self):
        self._staticFileInfo = self._doScan(self._scanPath)

    def _doScan(self, scanPath):
        '运行主函数，收集目录下符合条件的文件，准备比较'
        staticFileInfo = collections.OrderedDict()
        for dir, subdirs, fileList in os.walk(scanPath):
            # print "directory = %s | subdir = %s | filename = %s" %(dir, subdirs, fs)
            for fname in fileList:
                matcher = self._reXMLPatter.match(fname)
                if matcher != None:
                    fileFullPath = "%s/%s" % (dir, fname)
                    #dataSetName = matcher.group(1)
                    if (not os.path.exists(fileFullPath)):
                        continue
                    relPos = 0
                    if (len(self._leftTrip) > 0) :
                        relPos = fileFullPath.find(self._leftTrip)
                    fileRelPath = fileFullPath[relPos:]
                    fileInfo = StaticDataFileInfo()
                    fileInfo.staticDataPath = fileFullPath
                    fileInfo.staticDataRelPath = fileRelPath
                    fileInfo.staticFileName = fname
                    staticFileInfo[fileRelPath] = fileInfo

        return staticFileInfo

    def getScanInfo(self):
        return self._staticFileInfo




if (__name__ == "__main__"):
    patternXML = r'^\[PUB\](\w+)-STD\.xml'
    patternMerge = r'^(\[PUB\](\w+)-STD\.xml).merge$'
    patternAll = r'^\[PUB\](\w+)-STD\.(xml$|xml.merge$)'
    scanner = StaticFileScanner(r"D:\DevelopTrunk_V4R0_1\UNM2000\server\data\xml", patternMerge)
    scanner.scan()
    staticFileInfo = scanner.getScanInfo()

    mergePattern = re.compile(patternMerge)
    for scanKey, scanInfo in staticFileInfo.items():
        print("relative path = %s, fullpath = %s" %(scanKey, scanInfo.staticDataPath))
        matcher = mergePattern.match(scanInfo.staticFileName)
        if (None != matcher) :
            for gp in matcher.groups():
                print("group = %s" %(gp))
