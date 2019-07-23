#!/usr/bin/python
# -*- coding:utf8 -*-

import xml.etree.ElementTree as ET
import re
from lxml import etree
import collections
import logging
import chardet

from static_data_defines import ElementData

class StaticXMLParser(object):
    'XML文件解析器'

    def __init__(self, xmlFile):
        self._xmlFile = xmlFile
        #
        self._elementDict = collections.OrderedDict()
        self._staticData = []
        self._isUTF8 = False

    def isUTF8(self, xmlFile):
        bUTF8 = False
        with open(xmlFile, "rb") as fileHandle:
            #fileHandle = open(xmlFile, "rb")
            encodeLine = fileHandle.readline()
            result = chardet.detect(encodeLine)
            encodeLine = encodeLine.lower()
            fileHandle.seek(0, 0)
            bUTF8 = True if result["encoding"] == "utf-8" else False
            encodeLine = str(encodeLine)
            if encodeLine.find("utf-8") != -1:
                bUTF8 = True
        self._isUTF8 = bUTF8
        return bUTF8

    def decode(self, xmlFile):
        '转换编码格式'
        rawContent = ""
        try :
            bUTF8 = self.isUTF8(xmlFile)
            mode = "rb" if bUTF8 else "r"
            with open(xmlFile, mode) as fileHandle :
                rawContent = fileHandle.read()
                if (not bUTF8) :
                    rawContent = re.sub('encoding="GBK"', 'encoding="UTF-8"', rawContent)
                    rawContent.encode("UTF-8")
        except UnicodeDecodeError:
            # 按utf8解析文件.
            logging.getLogger("compare").warning("Decode Again file://%s" %(xmlFile))
            #with codecs.open(xmlFile, "rb", "utf-8") as codecsHandle :
            #    rawContent = codecsHandle.read()
            #    rawContent = rawContent.replace('encoding="GBK"', 'encoding="UTF-8"', rawContent)
        except:
            logging.getLogger("compare").error("Decode file://%s Occur Exception." %(xmlFile))
        return rawContent

    def parse(self):
        try :
            context = self.decode(self._xmlFile)
            #domTree = xml.dom.minidom.parseString(rawContent)
            #xmlRoot = domTree.documentElement
            #xmlElementList = xmlRoot.getElementsByTagName("element-list")
            if (context == "") :
                return
            domTree = ET.fromstring(context)
            xmlRoot =  domTree #domTree.getroot()
            xmlElementList = xmlRoot.findall("element-list/element")
            #记录静态数据中的元素类型
            elementPos = 0
            for xmlElement in xmlElementList:
                elementData = ElementData()
                #elementData.elementName = xmlElement.getAttribute("name")
                #elementData.elementType = xmlElement.getAttribute("data-type")
                elementData.elementName = xmlElement.get("name")
                elementData.elementType = xmlElement.get("data-type")
                primaryKey = xmlElement.attrib.get("primay-key")
                elementData.isPrimaryKey = False if (primaryKey != "true") else True
                elementData.elementIndex = elementPos
                self._elementDict[elementPos] = elementData
                elementPos += 1
            #解析XML静态数据中的行与列数据
            xmlDataList = xmlRoot.findall("data")
            for xmlTbl in xmlDataList:
                xmlRowList = xmlTbl.findall("row")
                for xmlRow in xmlRowList:
                    xmlColList = xmlRow.findall("col")
                    rowData = []
                    for xmlCol in xmlColList :
                        rowData.append(xmlCol.text)
                    self._staticData.append(rowData)
        except:
            raise
            #logging.getLogger("compare").error("Parse Error: file://%s" %self._xmlFile)

    def getData(self):
        '获取解析后的静态数据'
        return self._staticData

    def getElement(self):
        '获取文件基本信息'
        return self._elementDict

    def isUTF8Code(self):
        return self._isUTF8


if (__name__ == "__main__"):
    pass