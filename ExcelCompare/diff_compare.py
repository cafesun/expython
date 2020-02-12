import xlwings as xw
import os, sys

def parseDiffExcel(excelName, mapData) :
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



if __name__ == "__main__":
    #app = xw.App(visible=False, add_book=True)
    mapAuto = {}
    mapManual = {}
    mapDiff = {}

    parseDiffExcel("auto_diff.xlsx", mapAuto)
    parseDiffExcel("manual_diff.xlsx", mapManual)
    iCount = 0
    print("自动扫描多出来的设计项：")
    for key, value in mapAuto.items() :
        if (mapManual.get(key) == None) :
            print(key)
            mapDiff[++iCount] = key
    print("自动扫描少的设计项：")
    for key, value in mapManual.items():
        if (mapAuto.get(key) == None):
            print(key)
            mapDiff[++iCount] = key
    #excelDiffPath = r"E:\Data\Excel\excel-diff.xlsx"
    #excelDiffTbl = app.books.open(excelDiffPath)
    #diffSheet = excelDiffTbl.sheets[0]
    #for iRow in range(1, iCount + 1) :
    #    diffSheet.range(iRow, 1).value = mapDiff[iRow]
    #excelDiffTbl.save()
    #excelDiffTbl.close()
    #app.quit()

