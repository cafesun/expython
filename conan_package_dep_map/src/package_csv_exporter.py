#!/usr/bin/python
# -*- coding:utf8 -*-

import argparse
import os
from pylogger import getLogger
from pylogger import initLogger
from package_analyser import ConanPkgAnalyzer
from db_sqlite_serializer import DBSqlite3Serializer
from collections import OrderedDict


class CSVExporter(object):

    def __init__(self, db):
        self.__db = db

    def export(self):
        '''导出所有版本分支的包信息'''
        # {key=packagename;value={key=版本: packageInfo}}
        #prepare data
        packageTbl = OrderedDict()
        branchSet = set(self.__db.getBranches())
        if (len(branchSet) == 0) :
            return
        packageNameSet = self.__db.getAllPackageName()
        #构建 二维表 行=包名 列=版本名称
        for branch in branchSet:
            branchPkgMap = {}
            self.__db.queryEx(branch, branchPkgMap)
            for pkgName in packageNameSet:
                packageSubTbl = packageTbl.get(pkgName)
                if (None == packageSubTbl) :
                    #add new row
                    packageSubTbl = OrderedDict()
                    pkgInfo = branchPkgMap.get(pkgName)
                    packageSubTbl[branch] = pkgInfo
                    packageTbl[pkgName] = packageSubTbl
                else :
                    pkgInfo = branchPkgMap.get(pkgName)
                    packageSubTbl[branch] = pkgInfo
        # write to csv
        csvPath = "../data/export.csv"
        #if (os.path.exists(csvPath)) :
        #    os.remove(csvPath)

        with open(csvPath, "w") as exportFile:
            # write header
            strHeader = "package name"
            for branch in branchSet:
                strHeader = "%s, %s," %(strHeader, branch)
            exportFile.write(strHeader)
            exportFile.write("\n")
            for itPkg, subTbl in packageTbl.items():
                dataLine = "%s" %itPkg
                for version, verInstance in subTbl.items():
                    versionStr = "None"
                    if (None != verInstance):
                        versionStr = verInstance.version
                    dataLine = "%s, %s," % (dataLine, versionStr)
                exportFile.write(dataLine)
                exportFile.write("\n")

    def exportEx(self):
        branchSet = set(self.__db.getBranches())
        if (len(branchSet) == 0) :
            return
        packageExtTbl = OrderedDict()
        self.prepare("ext", packageExtTbl)

        packageCoreTbl = OrderedDict()
        self.prepare("core", packageCoreTbl)

        packagePlatformTbl = OrderedDict()
        self.prepare("platform", packagePlatformTbl)

        packageMsmpTbl = OrderedDict()
        self.prepare("msmp", packageMsmpTbl)

        # write to csv
        csvPath = "../data/export.csv"
        # if (os.path.exists(csvPath)) :
        #    os.remove(csvPath)

        with open(csvPath, "w") as exportHandle:
            # write header
            strHeader = "package name"
            for branch in branchSet:
                strHeader = "%s, %s," % (strHeader, branch)
            exportHandle.write(strHeader)
            exportHandle.write("\n")
            self.saveTo(packageExtTbl, exportHandle)
            self.saveTo(packageCoreTbl, exportHandle)
            self.saveTo(packagePlatformTbl, exportHandle)
            self.saveTo(packageMsmpTbl, exportHandle)

    def saveTo(self, packageTbl, exportFile):
        for itPkg, subTbl in packageTbl.items():
            dataLine = "%s" % itPkg
            for version, verInstance in subTbl.items():
                versionStr = "None"
                if (None != verInstance):
                    versionStr = verInstance.version
                dataLine = "%s, %s," % (dataLine, versionStr)
            exportFile.write(dataLine)
            exportFile.write("\n")

    def prepare(self, user, packageTbl):
        '''导出所有版本分支的包信息'''
        # {key=packagename;value={key=版本: packageInfo}}
        #prepare data
        branchSet = set(self.__db.getBranches())
        if (len(branchSet) == 0) :
            return
        packageNameSet = self.__db.getAllPackageName(user)
        #构建 二维表 行=包名 列=版本名称
        for branch in branchSet:
            branchPkgMap = {}
            self.__db.queryEx(branch, branchPkgMap)
            for pkgName in packageNameSet:
                packageSubTbl = packageTbl.get(pkgName)
                if (None == packageSubTbl) :
                    #add new row
                    packageSubTbl = OrderedDict()
                    pkgInfo = branchPkgMap.get(pkgName)
                    packageSubTbl[branch] = pkgInfo
                    packageTbl[pkgName] = packageSubTbl
                else :
                    pkgInfo = branchPkgMap.get(pkgName)
                    packageSubTbl[branch] = pkgInfo



