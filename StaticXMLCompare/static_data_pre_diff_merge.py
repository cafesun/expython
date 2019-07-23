#!/usr/bin/python
# -*- coding:utf8 -*-

import os, sys, argparse
import logging
from static_file_scanner import StaticFileScanner
from static_xml_parser_ex import StaticXMLParseEx



class StaticDataPreMerge(object):
    '静态数据合并类'

    def __init__(self, xmlPath, pattern):
        self._xmlPath = xmlPath
        self._pattern = pattern
        self._scanner = StaticFileScanner(xmlPath, pattern)
        self._alarmTypeMap = {}
        self._pmTypeMap = {}

    def init(self):
        self._scanner.scan()
        xmlAlarmTypeFile = self._xmlPath + "/[PUB]AlarmType-STD.xml"
        xmlPMTypeFile = self._xmlPath + "/[PUB]PmType-STD.xml"
        xmlAlarmTypeParser = StaticXMLParseEx(xmlAlarmTypeFile)
        xmlPmTypeParser = StaticXMLParseEx(xmlPMTypeFile)
        xmlAlarmTypeParser.parse()
        xmlPmTypeParser.parse()

        keyAlarmTupleExp = xmlAlarmTypeParser.getKeyTuple()
        for srcRow in xmlAlarmTypeParser.getData():
            rowContext = []
            for srcCol in srcRow:
                rowContext.append(srcCol)
            # rowContext.append("</row>")
            keyTuple = eval(keyAlarmTupleExp)
            self._alarmTypeMap[keyTuple] = rowContext[6]

        keyPmTupleExp = xmlPmTypeParser.getKeyTuple()
        for srcRow in xmlPmTypeParser.getData():
            rowContext = []
            for srcCol in srcRow:
                rowContext.append(srcCol)
            # rowContext.append("</row>")
            keyTuple = eval(keyPmTupleExp)
            self._pmTypeMap[keyTuple] = rowContext[8]

    def doMerge(self, orgFile, srcDiffFile, dstDiffFile):
        pass


    def merge(self):
        staticFileInfo = self._scanner.getScanInfo()
        for fileInfo in staticFileInfo.values():
            if (not self.hasMergeFile(fileInfo.staticDataPath)):
                continue
            srcDiffFilePath = fileInfo.staticDataPath + ".srcdiff"
            if (not os.path.exists(srcDiffFilePath)):
                continue
            dstDiffFilePath = fileInfo.staticDataPath + ".dstdiff"
            if (not os.path.exists(dstDiffFilePath)):
                continue
            bRet = self.doMerge(fileInfo.staticDataPath, srcDiffFilePath, dstDiffFilePath)
            if (bRet):
                logging.getLogger("merge").debug("Pre Merge OK. file://%s" % (fileInfo.staticDataPath))
            else:
                logging.getLogger("merge").warning("Pre Merge BAD. file://%s" % (fileInfo.staticDataPath))

    def dump(self):
        pass

def main() :
    pass


if (__name__ == "__main__"):
    LOG_FORMAT = "[%(asctime)s][%(levelname)s][%(process)d][%(thread)d]%(message)s"

    DEFAULT_PATTERN = r'^\[PUB\](\w+)-STD\.xml$'
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

