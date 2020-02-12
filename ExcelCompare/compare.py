import xlwings as xw
import os, sys

def parseBasicExcel(mapData) :
    try :
        app = xw.App(visible=False, add_book=False)
        excelTblPath = r"E:\Data\Excel\基础功能测试需求-设计需求关系.xlsx"
        excelTbl = app.books.open(excelTblPath)
        print("open " + excelTblPath + " OK!")
        iSheetsCount = excelTbl.sheets.count
        print("sheet count is %d" %iSheetsCount)
        mainSheet = excelTbl.sheets[0]
        nRows = mainSheet.used_range.last_cell.row
        nCols = mainSheet.used_range.last_cell.column
        for iRow in range(1, nRows + 1) :
            keyValue = mainSheet.range(iRow, 1).value
            value = mainSheet.range(iRow, 2).value
            color = mainSheet.range(iRow, 2).color
            if (color != (255, 255, 0)) : # 黄底
                continue
            mapData[keyValue.strip()] = "Y"
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


def parseMarketExcel(mapData) :
    try :
        app = xw.App(visible=False, add_book=False)
        excelTblPath = r"E:\Data\Excel\市场需求—设计需求—测试用例关系导出.xlsx"
        excelTbl = app.books.open(excelTblPath)
        print("open " + excelTblPath + " OK!")
        iSheetsCount = excelTbl.sheets.count
        print("sheet count is %d" %iSheetsCount)
        mainSheet = excelTbl.sheets[0]
        nRows = mainSheet.used_range.last_cell.row
        nCols = mainSheet.used_range.last_cell.column
        for iRow in range(1, nRows + 1) :
            keyValue = mainSheet.range(iRow, 5).value
            value = mainSheet.range(iRow, 1).value
            if (keyValue == None or keyValue == "") :
                continue
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


if __name__ == "__main__":
    app = xw.App(visible=False, add_book=True)
    mapBasic = {}
    mapMarket = {}
    mapDiff = {}
    parseBasicExcel(mapBasic)
    parseMarketExcel(mapMarket)
    iCount = 0
    for key, value in mapBasic.items() :
        if (mapMarket.get(key) == None) :
            print(key)
            mapDiff[++iCount] = key
    excelDiffPath = r"E:\Data\Excel\excel-diff.xlsx"
    excelDiffTbl = app.books.open(excelDiffPath)
    diffSheet = excelDiffTbl.sheets[0]
    for iRow in range(1, iCount + 1) :
        diffSheet.range(iRow, 1).value = mapDiff[iRow]
    excelDiffTbl.save()
    excelDiffTbl.close()
    app.quit()

