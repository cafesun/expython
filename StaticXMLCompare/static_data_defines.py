#!/usr/bin/python
# -*- coding:utf8 -*-

from enum import Enum

class FileEncoding(Enum) :
    EN_UTF_8 = 0
    EN_GBK = 1


class ElementData(object):
    '对应 xml中的elment字段'
    def __init(self):
        self.elementIndex = 0
        self.elementName=""
        self.elementType=""
        self.isPrimaryKey = False

    def __eq__(self, other):
        rhsElementIndex = other.getIndex()
        rhsElementName = other.getName()
        rhsElementType = other.getType()
        rhsIsPrimaryKey = other.hasPrimaryKey()
        return (self.elementName == rhsElementName and self.elementIndex == rhsElementIndex and
                self.elementType == rhsElementType and self.isPrimaryKey == rhsIsPrimaryKey)

    def getName(self):
        return self.elementName

    def getIndex(self):
        return self.elementIndex

    def getType(self) :
        return self.elementType

    def hasPrimaryKey(self):
        return self.isPrimaryKey

class ElementNotMatchEx(Exception):
    'Element不匹配异常'
    def __init__(self, file, what = ""):
        self._file = file
        self._what = what


    def __str__(self):
        strWhat = "Element Not Match"
        if (0 != len(self._what)) :
            strWhat += (" exception=%s" %self._what)
        if (0 != len(self._file)) :
            strWhat += (" file:// %s" %(self._file))
        return strWhat


class StaticDataFileInfo :
    '静态数据文件信息'
    def __init__(self):
        self.staticDataPath = ""
        self.staticDataName = ""
        self.staticDataRelPath = ""
        self.staticFileName = ""