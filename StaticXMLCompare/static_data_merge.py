#!/usr/bin/python
# -*- coding:utf8 -*-

import os, sys, argparse
import logging
from static_file_scanner import StaticFileScanner
from static_xml_parser_ex import StaticXMLParseEx

class StaticDataMerge(object):
    '静态数据合并类'

    def __init__(self, xmlPath, pattern):
        self._xmlPath = xmlPath
        self._scanner = StaticFileScanner(xmlPath, pattern)

    def init(self):
        self._scanner.scan()

    def hasMergeFile(self, filePath):
        mergeFilePath = filePath + ".merge"
        if (os.path.exists(mergeFilePath)) :
            return True
        else :
            return False


    def merge(self):
        staticFileInfo = self._scanner.getScanInfo()
        for fileInfo in staticFileInfo.values():
            if (not self.hasMergeFile(fileInfo.staticDataPath)):
                continue
            toMergeFilePath = fileInfo.staticDataPath + ".merge"
            bRet = self.doMerge(fileInfo.staticDataPath, toMergeFilePath)
            if (bRet) :
                logging.getLogger("merge").debug("Merge OK. file://%s" % (fileInfo.staticDataPath))
            else :
                logging.getLogger("merge").warning("Merge BAD. file://%s" % (fileInfo.staticDataPath))



    def doMerge(self, orgXmlFile, mergeXmlFile):
        try :
            orgXmlParser = StaticXMLParseEx(orgXmlFile)
            mergeXmlParser = StaticXMLParseEx(mergeXmlFile)
            orgXmlParser.parse()
            mergeXmlParser.parse()
            keyTupleExp = orgXmlParser.getKeyTuple()
            orgContext = {}
            for srcRow in orgXmlParser.getData():
                rowContext = []
                for srcCol in srcRow:
                    rowContext.append(srcCol)
                # rowContext.append("</row>")
                keyTuple = eval(keyTupleExp)
                orgContext[keyTuple] = rowContext

            # srcContext.sort(key=eval(lambdaExp))
            fileEncoding = orgXmlParser.getXmlEncoding()
            orgSrcXmlFile = orgXmlFile + ".org"
            self.dump(orgSrcXmlFile, orgXmlParser.getElement(), orgContext, fileEncoding)

            mergeContext = {}
            for dstRow in mergeXmlParser.getData():
                rowContext = []
                for dstCol in dstRow:
                    rowContext.append(dstCol)
                # rowContext.append("</row>")
                keyTuple = eval(keyTupleExp)
                mergeContext[keyTuple] = rowContext
                orgValue = orgContext.get(keyTuple)
                if (None != orgValue) :
                    orgContext[keyTuple] = rowContext
                else :
                    orgContext[keyTuple] = rowContext

            mergedXMLFile = orgXmlFile + ".merged"
            self.dump(mergedXMLFile, orgXmlParser.getElement(), orgContext, fileEncoding)
            return True
        except:
            raise
            logging.getLogger("merge").error("Merge file://%s Occur Exception!" % (orgXmlFile))
            return False


    def dump(self, xmlFile, elementList, context, xmlEncoding):
        '将内容写入文件'
        with open(xmlFile, "wb") as writeFileHandle :
            xmlDeclare = '<?xml version="1.0" encoding="%s" ?>\n' %xmlEncoding
            writeFileHandle.write(xmlDeclare)
            writeFileHandle.write("<static-data>\n")
            writeFileHandle.write("\t<element-list>\n")
            for elementKey, elementValue in elementList.items():
                if not elementValue.hasPrimaryKey() :
                    writeFileHandle.write('\t\t<element name="%s" data-type="%s"/>\n'
                                      %(elementValue.getName(), elementValue.getType()))
                else :
                    writeFileHandle.write('\t\t<element name="%s" primay-key="true" data-type="%s"/>\n'
                                          % (elementValue.getName(), elementValue.getType()))
            writeFileHandle.write("\t</element-list>\n")
            writeFileHandle.write("\t<data>\n")
            for srcKey, srcData in context.items():
                strData = "\t\t<row>\n"
                for itData in srcData:
                    strData += "\t\t\t<col>%s</col>\n" % (itData)
                strData += "\t\t</row>\n"
                if "gbk" == xmlEncoding.lower():
                    strData = strData.encode("gbk")
                    writeFileHandle.write(strData)
                else:
                    byteData = bytes(strData, encoding="utf8")
                    writeFileHandle.write(byteData)
            writeFileHandle.write("\t</data>\n")
            writeFileHandle.write("</static-data>\n")


def main():
    #DEFAULT_PATTERN = r'^(\[PUB\](\w+)-STD\.xml).merge$'
    DEFAULT_PATTERN = r'^\[PUB\](\w+)-STD\.xml$'
    logging.getLogger("merge").debug("begin merge the static data")
    parser = argparse.ArgumentParser()
    parser.add_argument("--scanpath", "-s", help="scan merge static data path", type=str, default="./data", nargs="?")
    parser.add_argument("--pattern", "-p", help="scan file pattern", type=str, default=DEFAULT_PATTERN, nargs="?")
    args = parser.parse_args()

    logging.getLogger("merge").debug("soure path = %s" % (args.scanpath))
    logging.getLogger("merge").debug("match pattern = %s" % (args.pattern))
#    args.path = os.path.abspath(args.path)
#    os.chdir(args.path)
    staticMerge = StaticDataMerge(args.scanpath, args.pattern)
    staticMerge.init()
    staticMerge.merge()





if (__name__ == "__main__"):
    LOG_FORMAT = "[%(asctime)s][%(levelname)s][%(process)d][%(thread)d]%(message)s"

    handleConsole = logging.StreamHandler(sys.stdout)
    handleFile = logging.FileHandler(filename="./log/merge.log")
    fomatter = logging.Formatter(LOG_FORMAT)
    handleConsole.setFormatter(fomatter)
    handleFile.setFormatter(fomatter)
    # handleConsole.setLevel(logging.DEBUG)
    # handleFile.setLevel(logging.DEBUG)
    logger = logging.getLogger("merge")
    logger.addHandler(handleConsole)
    logger.addHandler(handleFile)
    logger.setLevel(logging.DEBUG)

    # logging.basicConfig(filename="./compare.log", level=logging.DEBUG, format=LOG_FORMAT)
    logger.debug("begin merge")
    main()
    logger.debug("end merge")



