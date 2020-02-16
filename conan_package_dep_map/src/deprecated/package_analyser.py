#!/usr/bin/python
# -*- coding:utf8 -*-

import os, re
import collections
from pylogger import getLogger
from package_defines import PackageInfo
from deprecated.ast_pyclass_parser import ConanFileParserWarapper

class ConanPkgAnalyzer(object):
    '''conan包分析器'''
    def __init__(self, scanpath, type):
        self._scanpath = scanpath
        self._channel = ""
        self._pkgPattern = re.compile(r"(\w+)_(\w+)_(\w+)")
        self._pkgInfoMap = collections.OrderedDict()
        self._type = type

    def analyse(self):
        channelTxtPath = self._scanpath + "/channel.txt"
        if (not os.path.exists(channelTxtPath)) :
            getLogger().fatal("No channel.txt file found")
            return False
        with open(channelTxtPath, "r") as channelTxtHdr :
            self._channel = channelTxtHdr.readline()
        self.doScan(self._scanpath, self._channel, self._type)

    def getPkgName(self, dirPath):
        pos = len(self._scanpath)
        subPath = dirPath[pos + 1:]
        pkgName = subPath.split("\\")[0]
        return pkgName

    def parseType(self, pkgName, default):
        if (default != "auto") :
            return default
        if (pkgName.find("_plat_") != -1) :
            return "platform"
        elif (pkgName.find("_msmp_") != -1):
            return "msmp"
        else:
            return "unknown"

    def doScan(self, scanPath, pkgChannel, type):
        '运行主函数，收集目录下符合条件的文件，准备比较'
        pkgMap = {}
        for dir, subdirs, fileList in os.walk(scanPath):
            # print "directory = %s | subdir = %s | filename = %s" %(dir, subdirs, fs)
            if (dir == scanPath):
                continue
            pkgName = self.getPkgName(dir)
            packgeUserType = self.parseType(pkgName, self._type)
            if ("ZERO_CHECK.dir" == pkgName or "CMakeFiles" == pkgName):
                continue
            # 为了解决head-only模块的识别
            if (None == pkgMap.get(pkgName)):
                pkgMap[pkgName] = False  # 防止反复重置为False
            for fname in fileList:
                if ("conanfile.py" != fname) :
                    continue
                fullFileName = dir + "/" + fname
                parser = ConanFileParserWarapper(fullFileName)
                parser.parse()
                packageInfo = PackageInfo()
                name = parser.getAttribute("name")
                packageInfo.packageName = name
                packageInfo.channel = self._channel
                packageInfo.version = parser.getAttribute("version")
                packageInfo.packageFullName = pkgName
                packageInfo.user = packgeUserType
                if (None == name) :
                    getLogger().error("%s parse version failed!" %fullFileName)
                    continue
                self._pkgInfoMap[name] = packageInfo

    def getResult(self):
        return self._pkgInfoMap