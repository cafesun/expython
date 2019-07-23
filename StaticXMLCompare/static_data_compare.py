#!/usr/bin/python
# -*- coding:utf8 -*-


import os, sys, argparse, re
import collections
import operator
import logging
import logging.handlers
from static_data_defines import ElementNotMatchEx
from static_xml_parser import StaticXMLParser
from static_data_defines import StaticDataFileInfo
from copy import deepcopy


class CompareResultEx(object) :
    """排序比较后的结果"""
    def __init__(self, isUTF8, xmlFile, srcOnlyDict, dstOnlyDict, changedSrcDict, changedDstDict) :
        self._isUTF8 = isUTF8
        self._xmlFile = xmlFile
        self._srcOnlyStaticData = deepcopy(srcOnlyDict)
        self._dstOnlyStaticData = deepcopy(dstOnlyDict)
        self._changedSrcStaticData = deepcopy(changedSrcDict)
        self._changedDstStaticData = deepcopy(changedDstDict)

    def writeToFile(self, outputFile, dataSet):
        '将数据写入文件'
        with open(outputFile, "wb+", os.O_TRUNC | os.O_APPEND) as fileHnd:
            for srcKey, srcData in dataSet.items():
                strData = "\t\t<row>\n"
                for itData in srcData:
                    strData += "\t\t\t<col>%s</col>\n" % (itData)
                strData += "\t\t</row>\n"
                if not self._isUTF8:
                    strData = strData.encode("GBK")
                    fileHnd.write(strData)
                else:
                    byteData = bytes(strData, encoding="utf8")
                    fileHnd.write(byteData)


    def dump(self):
        '将比较结果各自写入不同的文件.'
        #fileEncoding = "utf-8" if self._isUTF8 else "gbk"
        if (len(self._srcOnlyStaticData.items()) != 0) :
            srcOnlyFileName = self._xmlFile + ".src"
            self.writeToFile(srcOnlyFileName, self._srcOnlyStaticData)

        # 暂不输出dst多出来的部分
        #if (len(self._dstOnlyStaticData.items()) != 0) :
        #    dstOnlyFileName = self._xmlFile + ".dst"
        #    self.writeToFile(dstOnlyFileName, self._dstOnlyStaticData)

        if (len(self._changedSrcStaticData.items()) != 0) :
            srcChangeFileName = self._xmlFile + ".srcdiff"
            self.writeToFile(srcChangeFileName, self._changedSrcStaticData)

        if (len(self._changedDstStaticData.items()) != 0) :
            dstChangeFileName = self._xmlFile + ".dstdiff"
            self.writeToFile(dstChangeFileName, self._changedDstStaticData)


class StaticXMLManager(object):
    def __init__(self, args):
        self._args = args
        self._reXMLPatter = re.compile(r'^\[PUB\](\w+)-STD\.xml')
        self._srcStaticFileInfo = collections.OrderedDict()
        self._dstStaticFileInfo = collections.OrderedDict()


    def doScan(self, scanPath):
        '运行主函数，收集目录下符合条件的文件，准备比较'
        staticFileInfo = {}
        for dir, subdirs, fileList in os.walk(scanPath):
            # print "directory = %s | subdir = %s | filename = %s" %(dir, subdirs, fs)
            for fname in fileList:
                matcher = self._reXMLPatter.match(fname)
                if matcher != None :
                    fileFullPath = "%s/%s" % (dir, fname)
                    dataSetName = matcher.group(1)
                    if (not os.path.exists(fileFullPath)):
                        continue
                    #logging.getLogger("compare").debug("file://%s" % (fileFullPath))
                    #staticXMLParser = StaticXMLParser(fileFullPath)
                    #staticXMLParser.parse()
                    #self._xmlFileDict[fname] = staticXMLParser
                    relPos = fileFullPath.find("xml")
                    fileRelPath = fileFullPath[relPos:]
                    fileInfo = StaticDataFileInfo()
                    fileInfo.staticDataName = dataSetName
                    fileInfo.staticDataPath = fileFullPath
                    fileInfo.staticDataRelPath = fileRelPath
                    staticFileInfo[fileRelPath] = fileInfo
        return staticFileInfo

    def scan(self):
        '扫描源目录和目标目录,比较源目录和目标目录都有的文件，对于源目录有，目标目录没有的文件则只提示'
        self._srcStaticFileInfo = self.doScan(self._args.sourcepath)
        self._dstStaticFileInfo = self.doScan(self._args.destpath)
        for srcFile, srcFileInfo in self._srcStaticFileInfo.items() :
            dstFile = self._dstStaticFileInfo.get(srcFile)
            if (None == dstFile) :
                #源目录有，目标目录没有，打印文件名称
                logging.getLogger("compare").debug("source unique file://%s" %(srcFile))
            else:
                #源码目录和目标目录都存在对应的文件，则进行比较
                try :
                    logging.getLogger("compare").debug("begin comparing staticdata[%s]" % srcFileInfo.staticDataRelPath)
                    cmpResult = self.compare(srcFileInfo.staticDataPath, dstFile.staticDataPath)
                    cmpResult.dump()
                    logging.getLogger("compare").debug("end comparing staticdata[%s]" % srcFileInfo.staticDataRelPath)
                except ElementNotMatchEx as ex:
                    logging.getLogger("compare").error("occur exception %s" % (str(ex)))
                except:
                    raise
                    #logging.getLogger("compare").debug("processing file://%s occur exception" % (srcFileInfo.staticDataRelPath))
                    #continue

    def compare(self, srcFile, dstFile):
        '比较源XML和目标XML差异'
        srcXMLPaser = StaticXMLParser(srcFile)
        dstXMLPaser = StaticXMLParser(dstFile)
        srcXMLPaser.parse()
        dstXMLPaser.parse()
        srcElementDict = srcXMLPaser.getElement()
        dstElementDict = dstXMLPaser.getElement()

        cmpRet = operator.eq(srcElementDict, dstElementDict)
        if (True != cmpRet) :
            logging.getLogger("compare").warning("ElementList are different srcfile://%s dstfile://%s" %(srcFile, dstFile))
            if (srcFile.find("[PUB]OperationRelation-STD.xml") != -1) :
                return self.compareOperationRelation(srcXMLPaser, dstXMLPaser, dstFile) #特殊处理
            if (srcFile.find("[PUB]OperationTypeName-STD.xml") != -1) :
                return self.compareOperationTypeName(srcXMLPaser, dstXMLPaser, dstFile) #特殊处理
        srcElementList = list(srcElementDict.values())
        dstElementList = list(dstElementDict.values())
        srcMoreElementList = []
        dstMoreElementList = []
        self.getMoreElement(
            cmpRet, srcElementList, dstElementList, srcMoreElementList, dstMoreElementList)

        lambdaExp = ""
        hasPrimaryKey = False
        multiKey = False
        keyTupleExp = ""
        keyIndex = []
        for elementKey, elementValue in srcXMLPaser.getElement().items() :
            if elementValue.isPrimaryKey == True :
                if (hasPrimaryKey == False) :
                    hasPrimaryKey = True
                    lambdaExp = "lambda x:(x[%d]" % (elementKey)
                    keyTupleExp += "(rowContext[%d]" %elementKey
                    keyIndex.append(elementKey)
                else :
                    if (multiKey == False) :
                        multiKey = True
                    lambdaExp += ", x[%d]" % (elementKey)
                    keyTupleExp += ", rowContext[%d]" %elementKey
                    keyIndex.append(elementKey)
        if (hasPrimaryKey == True) :
            lambdaExp += ")"
            keyTupleExp +=")"
        else :
            lambdaExp = "lambda x:x[0]"
            keyTupleExp = "(%s)"

        srcContext = {}
        for srcRow in srcXMLPaser.getData() :
            rowContext = []
            for srcCol in srcRow :
                rowContext.append(srcCol)
            #rowContext.append("</row>")
            if (hasPrimaryKey) :
                if (multiKey) :
                    keyTuple = eval(keyTupleExp)
                    srcContext[keyTuple] = rowContext
                else :
                    srcContext[rowContext[keyIndex[0]]] = rowContext
            else :
                srcContext[rowContext[0]] = rowContext

         #srcContext.sort(key=eval(lambdaExp))

        dstContext = {}
        for dstRow in dstXMLPaser.getData():
            rowContext = []
            for dstCol in dstRow:
                rowContext.append(dstCol)
            # rowContext.append("</row>")
            if (hasPrimaryKey):
                if (multiKey):
                    keyTuple = eval(keyTupleExp)
                    dstContext[keyTuple] = rowContext
                else:
                    dstContext[rowContext[keyIndex[0]]] = rowContext
            else:
                dstContext[rowContext[0]] = rowContext

        self.mergeMore(srcMoreElementList, dstMoreElementList, srcContext, dstContext)
        return self.doCompare(srcContext, dstContext, dstFile, dstXMLPaser.isUTF8Code())

    def doCompare(self, srcContext, dstContext, dstFile, isUTF8):
        # 比较排序后的源数据和目标数据
        srcOnlyContext = {}
        dstOnlyContext = {}
        changedSrcContext = {}
        changedDstContext = {}
        for srcKey, srcData in srcContext.items():
            dstData = dstContext.get(srcKey)
            if (None == dstData) :
                srcOnlyContext[srcKey] = srcData
            else:
                if (operator.eq(srcData, dstData) != True):
                    changedSrcContext[srcKey] = srcData
                    changedDstContext[srcKey] = dstData

        for dstKey, dstData in dstContext.items() :
            srcData = srcContext.get(dstKey)
            if (None == srcData) :
                dstOnlyContext[dstKey] = dstData

        cmpResult = CompareResultEx(isUTF8, dstFile, srcOnlyContext, dstOnlyContext, changedSrcContext, changedDstContext)
        return cmpResult

    def compareOperationRelation(self, srcXMLParser, dstXMLParser, dstFile):
        '''[PUB]OperationRelation-STD.xml 特殊处理'''
        srcElementDict = srcXMLParser.getElement()
        dstElementDict = dstXMLParser.getElement()
        #以传输的格式为准,原则是接入向传输合并.
        if (srcElementDict[0].getName() != "operationid" or
                dstElementDict[0].getName() != "dependoperationid") :
            raise ElementNotMatchEx("[PUB]OperationRelation-STD.xml", "cannot process element different!")

        #需要把接入的源文件转换成与传输一致.
        srcContext = {}
        for srcRow in srcXMLParser.getData():
            tempRowContext = []
            for srcCol in srcRow:
                tempRowContext.append(srcCol)
            # rowContext.append("</row>")
            if (None == srcContext.get(tempRowContext[-1])) :
                varContext = []
                varContext.append(tempRowContext[0])
                srcContext[tempRowContext[-1]] = varContext
            else :
                srcContext[tempRowContext[-1]].append(tempRowContext[0])
        # 将列转换为,分割的已排序的字符串.
        for srcCtxKey, srcCtx in srcContext.items():
            srcCtx.sort()
            bFirst = True
            strContext = ""
            for itSrcCtx in srcCtx:
                if (bFirst) :
                    bFirst = False
                    strContext += itSrcCtx
                else :
                    strContext += ","
                    strContext += itSrcCtx
            srcCtx.clear()
            srcCtx.append(srcCtxKey)
            srcCtx.append(strContext)

        dstContext = {}
        for dstRow in dstXMLParser.getData():
            rowContext = []
            for dstCol in dstRow:
                rowContext.append(dstCol)
            splitContext = rowContext[-1].split()
            splitContext.sort()
            bFirst = True
            strContext = ""
            for itSplit in splitContext :
                if (bFirst) :
                    bFirst = False
                    strContext += itSplit
                else :
                    strContext += ","
                    strContext.append(itSplit)
            rowContext[-1] = strContext
            dstContext[rowContext[0]] = rowContext

        return self.doCompare(srcContext, dstContext, dstFile, dstXMLParser.isUTF8Code())

    def compareOperationTypeName(self, srcXMLParser, dstXMLParser, dstFile):
        '''[PUB]OperationTypeName-STD.xml 特殊处理'''
        srcElementDict = srcXMLParser.getElement()
        dstElementDict = dstXMLParser.getElement()
        #以传输的格式为准,原则是接入向传输合并.
        nSrcElementListSize = len(list(srcElementDict.values()))
        nDstElementListSize = len(list(dstElementDict.values()))
        srcElementPosMap = collections.OrderedDict()
        dstElementPosMap = collections.OrderedDict()
        bDstMore = True if nSrcElementListSize < nDstElementListSize else False
        if (nSrcElementListSize == nDstElementListSize) :
            raise ElementNotMatchEx("[PUB]OperationTypeName-STD.xml", "cannot process element different!")
        else :
            if (bDstMore) :
                # 为将要补全的新srcContext计算补全列的映射关系
                for dstElementKey, dstElement in dstElementDict.items():
                    bFound = False
                    for srcElement in srcElementDict.values():
                        if (srcElement.getName() == dstElement.getName()) :
                            srcElementPosMap[dstElementKey] = srcElement.getIndex()
                            bFound = True
                            break
                    if (not bFound) :
                        srcElementPosMap[dstElementKey] = (-1) * dstElementKey
            else :
                # 为将要补全的新dstContext计算补全列的映射关系
                for srcElementKey, srcElement in srcElementDict.items():
                    bFound = False
                    for dstElement in dstElementDict.values():
                        if (dstElement.getName() == srcElement.getName()) :
                            dstElementPosMap[srcElementKey] = dstElement.getIndex()
                            bFound = True
                            break
                    if (not bFound) :
                        dstElementPosMap[srcElementKey] = (-1) * srcElementKey

        srcContext = {}
        dstContext = {}
        # 将缺的列，按对侧的值补齐.
        if (bDstMore) :
            #源侧缺列，先将宿侧数据解析完
            for dstRow in dstXMLParser.getData():
                rowContext = []
                for dstCol in dstRow:
                    rowContext.append(dstCol)
                dstContext[rowContext[0]] = rowContext

            for srcRow in srcXMLParser.getData():
                tmpRowContext = []
                rowContext = []
                for srcCol in srcRow:
                    tmpRowContext.append(srcCol)
                #按照dst列，补齐src数据
                dstRow = dstContext.get(tmpRowContext[0])
                if (None != dstRow) :
                    for srcPosKey, srcPosValue in srcElementPosMap.items():
                        if srcPosValue < 0 :
                            rowContext.append(dstRow[(-1) * srcPosValue])
                        else :
                            rowContext.append(tmpRowContext[srcPosValue])
                else:
                    for srcPosKey, srcPosValue in srcElementPosMap.items():
                        if srcPosValue < 0 :
                            rowContext.append("")
                        else :
                            rowContext.append(tmpRowContext[srcPosValue])
                srcContext[rowContext[0]] = rowContext

        else :
            #宿侧缺列,先将源侧数据解析完
            for srcRow in srcXMLParser.getData():
                rowContext = []
                for srcCol in srcRow:
                    rowContext.append(srcCol)
                srcContext[rowContext[0]] = rowContext

            for dstRow in dstXMLParser.getData():
                tmpRowContext = []
                rowContext = []
                for dstCol in dstRow:
                    tmpRowContext.append(dstCol)
                #按照dst列，补齐src数据
                srcRow = srcContext.get(tmpRowContext[0])
                if (None != srcRow) :
                    for dstPosKey, dstPosValue in dstElementPosMap.items():
                        if dstPosValue < 0 :
                            rowContext.append(srcRow[(-1) * dstPosValue])
                        else :
                            rowContext.append(tmpRowContext[dstPosValue])
                else:
                    for dstPosKey, dstPosValue in srcElementPosMap.items():
                        if dstPosValue < 0 :
                            rowContext.append("")
                        else :
                            rowContext.append(tmpRowContext[dstPosValue])
                dstContext[rowContext[0]] = rowContext
        return self.doCompare(srcContext, dstContext, dstFile, dstXMLParser.isUTF8Code())

    def mergeMore(self, srcMoreElementList, dstMoreElementList, srcContext, dstContext):
        '依据element列表，补充缺少列那一方的数据'
        # 补充数据，对于缺少列的情况，则从比较数据中有对应列的数据生成
        bMerge = False
        if (0 != len(srcMoreElementList) or  0!= len(dstMoreElementList)) :
            bMerge = True
        if (bMerge) :
            logging.getLogger("compare").debug("beging do merge")
        for srcMore in srcMoreElementList:
            moreIndex = srcMore.getIndex()
            for srcCtxKey, srcCtx in srcContext.items():
                dstCtx = dstContext.get(srcCtxKey)
                if (None == dstCtx):
                    # src里面多的列对应的key在dst中没有，则这部分数据需要整个合并.
                    continue
                else:
                    # src里面多的列可以在dst中找到对应的key,则在dst中后面新增列
                    dstCtx.append(srcCtx[moreIndex])
            # 对于dst中有，src中没有的列，则也要补充数据.
            for dstCtxKey, dstCtx in dstContext.items():
                srcCtx = srcContext.get(dstCtxKey)
                if (None == srcCtx):
                    # dst里面行对应的key在src中没有，则这部分数据补充空数据.
                    dstCtx.append("")

        # 补充数据，对于缺少列的情况，则从比较数据中有对应列的数据生成
        for dstMore in dstMoreElementList:
            moreIndex = dstMore.getIndex()
            for dstCtxKey, dstCtx in dstContext.items():
                srcCtx = srcContext.get(dstCtxKey)
                if (None == srcCtx):
                    # dst里面多的列对应的key在src中没有，则这部分数据需要整个合并.
                    continue
                else:
                    # dst里面多的列可以在src中找到对应的key,则在src中后面新增列
                    srcCtx.append(dstCtx[moreIndex])
            # 对于src中有，dst中没有的列，则也要补充数据.
            for srcCtxKey, srcCtx in srcContext.items():
                dstCtx = dstContext.get(srcCtxKey)
                if (None == dstCtx):
                    # dst里面行对应的key在src中没有，则这部分数据补充空数据.
                    srcCtx.append("")
        if (bMerge) :
            logging.getLogger("compare").debug("end do merge")

    def getMoreElement(self, cmpRet, srcElementList, dstElementList,
                       srcMoreElementList, dstMoreElementList):
        '计算两边XML多或者少的列'
        if (len(srcElementList) == 0 or len(dstElementList) == 0) :
            raise ElementNotMatchEx("", "Element cannot be empty!")
        if (cmpRet != True):
            for srcElementValue in srcElementList:
                if (srcElementValue not in dstElementList) :
                    srcMoreElementList.append(srcElementValue)
            for dstElementValue in dstElementList:
                if (dstElementValue not in srcElementList):
                    dstMoreElementList.append(dstElementValue)

        srcElementListSize = len(srcElementList)
        dstElementListSize = len(dstElementList)
        if (len(srcMoreElementList) != 0 and len(dstMoreElementList) != 0):
            # 如果两边的element都各不相同，则抛异常，通过人工判断解决.
            raise ElementNotMatchEx("", "both elements are completely different!")
        # 如果中间插入列，也报异常
        for srcMore in srcMoreElementList:
            if srcMore.getIndex() < dstElementListSize:
                raise ElementNotMatchEx("", "src xml has mid-insert element!")
        for dstMore in dstMoreElementList:
            if dstMore.getIndex() < srcElementListSize:
                raise ElementNotMatchEx("", "dst xml has mid-insert element!")

def main():
    logging.getLogger("compare").debug("begin parse the static data:\n")
    parser = argparse.ArgumentParser()
    parser.add_argument("--sourcepath", "-s", help="source static data path", type=str, default=".", nargs="?")
    parser.add_argument("--destpath", "-d", help="dest static data path", type=str, default=".")
    parser.add_argument("--ignorepath", "-i", help="ignore scan path", type=str, default="")
#    parser.add_argument("path", help="package root dir", type=str, default=".")
    args = parser.parse_args()
#    args.path = os.path.abspath(args.path)
#    os.chdir(args.path)
    logging.getLogger("compare").debug("soure path = %s\n" %(args.sourcepath))
    logging.getLogger("compare").debug("dest path = %s\n" %(args.destpath))
    logging.getLogger("compare").debug("ignore path = %s" %(args.ignorepath))
    staticDataMgr = StaticXMLManager(args)
    staticDataMgr.scan()


if (__name__ == "__main__"):
    LOG_FORMAT = "[%(asctime)s][%(levelname)s][%(process)d][%(thread)d]%(message)s"

    handleConsole = logging.StreamHandler(sys.stdout)
    handleFile = logging.FileHandler(filename="./log/compare.log")
    fomatter = logging.Formatter(LOG_FORMAT)
    handleConsole.setFormatter(fomatter)
    handleFile.setFormatter(fomatter)
    #handleConsole.setLevel(logging.DEBUG)
    #handleFile.setLevel(logging.DEBUG)
    logger = logging.getLogger("compare")
    logger.addHandler(handleConsole)
    logger.addHandler(handleFile)
    logger.setLevel(logging.WARNING)
    
    #logging.basicConfig(filename="./compare.log", level=logging.DEBUG, format=LOG_FORMAT)
    logger.debug("begin compare")
    main()
    logger.debug("end compare")

