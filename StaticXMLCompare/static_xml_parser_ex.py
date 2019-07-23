#!/usr/bin/python
# -*- coding:utf8 -*-

from lxml import etree
from static_xml_parser import StaticXMLParser
from static_data_defines import ElementData


class StaticXMLParseEx(StaticXMLParser) :
    '基于lxml的静态数据解析器'

    def __init__(self, xmlFile):
        super(StaticXMLParseEx, self).__init__(xmlFile)
        self._xmlEncoding = ""

    def parse(self):
        #fileEncoding = self.readXmlEncode(self._xmlFile)
        try :
            #parserImp = etree.XMLParser(encoding=fileEncoding)
            #xmlTree = etree.parse(self._xmlFile, parser = parserImp)
            xmlTree = etree.parse(self._xmlFile)
            #print("xml-encoding=%s" %(xmlTree.docinfo.encoding))
            self._xmlEncoding = xmlTree.docinfo.encoding.lower()
            if ("utf-8" == xmlTree.docinfo.encoding.lower()) :
                self._isUTF8 = True
            else :
                self._isUTF8 = False

            xmlRoot = xmlTree.getroot()
            xmlElementList = xmlTree.xpath("/static-data/element-list/element")
            elementPos = 0
            for xmlElement in xmlElementList:
                elementData = ElementData()
                # elementData.elementName = xmlElement.getAttribute("name")
                # elementData.elementType = xmlElement.getAttribute("data-type")
                elementData.elementName = xmlElement.get("name")
                elementData.elementType = xmlElement.get("data-type")
                primaryKey = xmlElement.attrib.get("primay-key")
                elementData.isPrimaryKey = False if (primaryKey != "true") else True
                elementData.elementIndex = elementPos
                self._elementDict[elementPos] = elementData
                elementPos += 1
            # 解析XML静态数据中的行与列数据
            xmlRowList = xmlTree.xpath("/static-data/data/row")
            for xmlRow in xmlRowList:
                xmlColList = xmlRow.findall("col")
                rowData = []
                for xmlCol in xmlColList:
                    rowData.append(xmlCol.text)
                self._staticData.append(rowData)
        except:
            raise

    def readXmlEncode(self, xmlFile):
        with open(xmlFile, "r") as fileHandle :
            fileHandle.seek(0, 0)
            headDeclare = fileHandle.readline()
            headDeclare = headDeclare.lower()
            if (headDeclare.find("utf-8") != -1) :
                return "utf-8"
            else :
                return "gbk"

    def getXmlEncoding(self):
        return self._xmlEncoding


    def getKeyTuple(self):
        '计算每行的关键字'
        hasPrimaryKey = False
        multiKey = False
        keyTupleExp = ""
        keyIndex = []
        for elementKey, elementValue in self.getElement().items():
            if elementValue.isPrimaryKey == True:
                if (hasPrimaryKey == False):
                    hasPrimaryKey = True
                    keyTupleExp += "(rowContext[%d]" % elementKey
                    keyIndex.append(elementKey)
                else:
                    if (multiKey == False):
                        multiKey = True
                    keyTupleExp += ", rowContext[%d]" % elementKey
                    keyIndex.append(elementKey)
        if (hasPrimaryKey == True):
            keyTupleExp += ")"
        else:
            keyTupleExp = "(rowContext[0])"
        return keyTupleExp

if (__name__ == "__main__"):
    staticParser = StaticXMLParseEx("./data/[PUB]AlarmType-STD.xml")
    staticParser.parse()
