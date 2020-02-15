#!/usr/bin/python
# -*- coding:utf8 -*-

import os
import pydot
from package_defines import PackageInfo
from pylogger import getLogger
#import graphviz
#import os

class ConanPkgDotAnalyzer(object):
    '''conan包分析器'''
    def __init__(self, scanpath, branch=""):
        self.__scanpath = scanpath
        self.__branch = branch
        self.__packageDict = {}

    def analyse(self):
        '''解析dot文件'''
        if self.__scanpath[-1:]=='/':
            dependencyDotPath = self.__scanpath + "dependency.dot"
        else:
            dependencyDotPath = self.__scanpath + "/dependency.dot"
        if (not os.path.exists(dependencyDotPath)) :
            getLogger().fatal("No dependencyDot file found")
            return False
        dots = pydot.graph_from_dot_file(dependencyDotPath)
        dot = dots[0]
        edges = dot.get_edge_list()

        packageDict = {}
        for itEdge in edges:
            edge = itEdge
            objDict = edge.obj_dict
            pointTpl = objDict["points"]
            curNode = pointTpl[0]
            packageDict[curNode] = "t"
            subNodes = pointTpl[1]["nodes"]
            for itSubNode in subNodes.keys():
                packageDict[itSubNode] = "t"
        for itPkgName in packageDict.keys():
            pkgInfo = self.analyzePkg(itPkgName)
            if (None != pkgInfo) :
                self.__packageDict[itPkgName] = pkgInfo


    def analyzePkg(self, packageID):
        '''parser package info from package name'''
        packageInfo = PackageInfo.extract(packageID)
        if (None == packageInfo) :
            return packageInfo
        packageInfo.branch = self.__branch
        if (self.__branch == "") :
            packageInfo.branch = packageInfo.channel
        return packageInfo

    def getResult(self):
        return self.__packageDict

if __name__ == "__main__" :
    print("parse dot file")
    parser = ConanPkgDotAnalyzer("../data")
    parser.analyse()
    packageMap = parser.getResult()
    for itKey, pkginfo in packageMap.items():
        print("package=%s name=%s version=%s user=%s channel=%s"
              %(itKey, pkginfo.packageName, pkginfo.version, pkginfo.user, pkginfo.channel))
 #   dotFile = open(r"../data/dependency.dot", "r")
 #   dotContext = dotFile.read()
 #   graphviz.Source(dotContext)


#    nodes = dot.get_node_list()
#    for it in nodes:
#       print(it)
