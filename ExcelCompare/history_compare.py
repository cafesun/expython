import xlwings as xw
import os, sys

class CompareData(object):
    '对应 xml中的elment字段'
    def __init(self):
        self.designID = ""
        self.marketID = ""
        self.replacedID = ""
        self.date = ""

    def get_designID(self):
        return self.designID

    def set_designID(self, strDesignID):
        self.designID = strDesignID

    def get_marketID(self):
        return self.get_marketID()

    def set_marketID(self, strMrketID):
        self.marketID = strMrketID

    def get_replacedID(self):
        return self.replacedID;

    def set_replacedID(self, strReplacedID):
        self.replacedID = strReplacedID

    def __eq__(self, other):
        if other == None :
            return False
        rhsDesignID = other.get_designID()
        rhsMarketID = other.get_marketID()
        rhsReplacedID = other.get_replacedID()
        return (self.designID == rhsDesignID and
                self.marketID == rhsMarketID and
                self.replacedID == rhsReplacedID)


def parseNoExistExcel(excelName, mapData) :
    try :
        app = xw.App(visible=False, add_book=False)
        excelTblPath = r"E:\Data\Excel\%s"  %excelName
        excelTbl = app.books.open(excelTblPath)
        print("open " + excelTblPath + " OK!")
        iSheetsCount = excelTbl.sheets.count
        print("sheet count is %d" %iSheetsCount)
        mainSheet = excelTbl.sheets[0]
        nRows = mainSheet.used_range.last_cell.row
        nCols = mainSheet.used_range.last_cell.column
        for iRow in range(1, nRows + 1) :
            keyValue = mainSheet.range(iRow, 1).value
            mapData[keyValue.strip()] = ""
            #print(value.color)
    except ValueError as exValue:
        print("exception is %s" %exValue)
    except:
        print("open excel failed!")
    finally:
        excelTbl.close()
        print("excel tbl close!")
        app.quit()
        print("excel quit!")


def parseHistoryExcel(excelName, mapData, nKeyCol, nDataCol, bChangeMarketID) :
    try :
        app = xw.App(visible=False, add_book=False)
        excelTblPath = r"E:\Data\Excel\%s"  %excelName
        excelTbl = app.books.open(excelTblPath)
        print("open " + excelTblPath + " OK!")
        iSheetsCount = excelTbl.sheets.count
        print("sheet count is %d" %iSheetsCount)
        mainSheet = excelTbl.sheets[0]
        nRows = mainSheet.used_range.last_cell.row
        nCols = mainSheet.used_range.last_cell.column
        if (nKeyCol > nCols) :
            raise Exception("key cols index is over range")
        if (nDataCol > nCols) :
            raise Exception("data cols index is over range")
        for iRow in range(1, nRows + 1) :
            keyValue = mainSheet.range(iRow, nKeyCol).value   # design ID
            dataValue = mainSheet.range(iRow, nDataCol).value  # market ID
            if (keyValue == None or keyValue =="") :
                continue
            if (bChangeMarketID) :
                if (dataValue.find("NWML-") != -1) :
                    dataValue = dataValue.replace("NWML-", "PRML-")
                else :
                    continue
            mapData[keyValue.strip()] = dataValue.strip()
            #print(value.color)
    except ValueError as exValue:
        print("exception is %s" %exValue)
    except:
        print("open excel failed!")
    finally:
        excelTbl.close()
        print("excel tbl close!")
        app.quit()
        print("excel quit!")


def parseMarketExcelEx(excelName, nKeyCol, nDataCol , mapData) :
    try :
        app = xw.App(visible=False, add_book=False)
        excelTblPath = r"E:\Data\Excel\%s" %excelName
        excelTbl = app.books.open(excelTblPath)
        print("open " + excelTblPath + " OK!")
        iSheetsCount = excelTbl.sheets.count
        print("sheet count is %d" %iSheetsCount)
        mainSheet = excelTbl.sheets[0]
        nRows = mainSheet.used_range.last_cell.row
        nCols = mainSheet.used_range.last_cell.column
        if (nKeyCol > nCols) :
            raise Exception("key cols index is over range")
        if (nDataCol > nCols) :
            raise Exception("data cols index is over range")
        for iRow in range(1, nRows + 1) :
            keyValue = mainSheet.range(iRow, nKeyCol).value
            value = mainSheet.range(iRow, nDataCol).value
            if (keyValue == None or keyValue == "") :
                continue
            if (value == None) :
                value = ""
            mapData[keyValue.strip()] = value.strip()
            #print(value.color)
    except ValueError as exValue:
        print("exception is %s" %exValue)
    except:
        print("open excel failed!")
    finally:
        excelTbl.close()
        print("excel tbl close!")
        app.quit()
        print("excel quit!")

def makeCompareData(key, mapOld, mapMarketID, strDate) :
    if (mapOld.get(key) != None) :
            compareData = CompareData()
            compareData.designID = key
            compareData.date = strDate
            compareData.marketID = mapOctber.get(key)
            if (compareData.marketID == None):
                return None
            if (mapMarketID.get(compareData.marketID) != None) :
                compareData.replacedID = mapMarketID[compareData.marketID]
            else :
                compareData.replacedID = ""
            return compareData
    else :
        return None

if __name__ == "__main__":
    #app = xw.App(visible=False, add_book=True)
    mapOctber = {}
    mapNovember = {}
    mapDecember = {}
    mapNoExist = {}
    mapMarket = {}
    mapCompare = {}

    parseHistoryExcel("市场需求-设计需求关联关系-1025.xlsx", mapOctber, 8, 1, True)
    parseHistoryExcel("市场需求-设计需求关联关系-1130.xlsx", mapNovember, 8, 1, False)
    parseHistoryExcel("市场需求-设计需求关联关系-1130.xlsx", mapDecember, 8, 1, False)
    parseNoExistExcel("manual_diff.xlsx", mapNoExist)
    parseMarketExcelEx("市场需求—设计需求—测试用例关系导出.xlsx", 1, 5, mapMarket)
    iCount = 0
    print("自动扫描多出来的设计项：")
    for key in mapNoExist.keys() :
        if (mapOctber.get(key) != None) :
            mapNoExist[key] = "1025"
            compareData = makeCompareData(key, mapOctber, mapMarket, "1025")
            if (compareData != None) :
                mapCompare[key] = compareData
                continue
        if (mapNovember.get(key) != None):
            mapNoExist[key] = "1130"
            compareData = makeCompareData(key, mapNovember, mapMarket, "1130")
            if (compareData != None) :
                mapCompare[key] = compareData
                continue
        if (mapDecember.get(key) != None):
            mapNoExist[key] = "1220"
            mapNoExist[key] = "1130"
            compareData = makeCompareData(key, mapNovember, mapMarket, "1130")
            if (compareData != None) :
                mapCompare[key] = compareData
                continue
        else :
            continue
    for key, data in mapCompare.items():
        print("%s \t %s \t %s \t %s" %(key, data.marketID, data.replacedID, data.date))


