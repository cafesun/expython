import sqlite3
import os
from collections import OrderedDict
from pylogger import getLogger
from package_defines import PackageInfo

class DBSqlite3Serializer(object):
    def __init__(self):
        self.__dbname = "../data/conanpkgs_info.db"
        self.__conn = None

    def open(self):
        cursor = None
        try :
            self.__conn = sqlite3.connect(self.__dbname)
            cursor = self.__conn.cursor()
            cursor.execute("select * from sqlite_master where type ='table' and name='t_conan_pkginfo'")
            varExist = cursor.fetchone()
            if (varExist == None) :
                self.__create_tbl()
            return True
        except StandardError as ex:
            getLogger().error("Open DB Failed(%s)" %(str(ex)))
            if (cursor != None) :
                cursor.close()
            if (self.__conn != None) :
                self.__conn.close()
            return False

    def close(self):
        self.__conn.close()

    def set(self, pkgInfoList):
        cursor = self.__conn.cursor()
        insertTblSql = '''
                    insert or replace into t_conan_pkginfo(cbranch, cid, cname, cversion, ctype, cchannel) values(
                    ?, ?, ?, ?, ?, ?)
                '''
        for itData in pkgInfoList :
            pkgId = itData.getPkgID()
            bindVars = (itData.branch, pkgId, itData.packageName, itData.version, itData.user, itData.channel)
            cursor.execute(insertTblSql, bindVars)
        self.__conn.commit()
        cursor.close()

    def delete(self, pkgInfoList):
        cursor = self.__conn.cursor()
        deleteTblSql = '''
                            delete from t_conan_pkginfo where cbranch=? and cid=?
                        '''
        for itData in pkgInfoList:
            pkgId = itData.getPkgID()
            bindVars = (itData.branch, pkgId)
            cursor.execute(deleteTblSql, bindVars)
        self.__conn.commit()
        cursor.close()

    def getAllPackageID(self):
        '''获取所有包的ID'''
        packageIDList = []
        cursor = self.__conn.cursor()
        queryTblSql = '''
                                            select distinct(cid) from t_conan_pkginfo
                                        '''
        cursor.execute(queryTblSql)
        row = cursor.fetchone()
        while (None != row):
            packageID = row[0]
            packageIDList.append(packageID)
            row = cursor.fetchone()
        cursor.close()
        return set(packageIDList)

    def getAllPackageName(self):
        '''获取所有包的名称'''
        packageNameList = []
        cursor = self.__conn.cursor()
        queryTblSql = '''
                                            select distinct(cname) from t_conan_pkginfo
                                        '''
        cursor.execute(queryTblSql)
        row = cursor.fetchone()
        while (None != row):
            packageName = row[0]
            packageNameList.append(packageName)
            row = cursor.fetchone()
        cursor.close()
        return set(packageNameList)

    def getBranches(self):
        '''获取所有的分支名称'''
        branchList = []
        cursor = self.__conn.cursor()
        queryTblSql = '''
                                      select distinct(cbranch) from t_conan_pkginfo
                                  '''
        cursor.execute(queryTblSql)
        row = cursor.fetchone()
        while (None != row):
            branch = row[0]
            branchList.append(branch)
            row = cursor.fetchone()
        cursor.close()
        return branchList

    def query(self, branch, result):
        '''查询指定分支下的所有包信息，返回的map  key为packageID'''
        cursor = self.__conn.cursor()
        queryTblSql = '''
                              select cbranch, cid, cname, cversion, ctype, cchannel from t_conan_pkginfo where cbranch=?
                          '''
        cursor.execute(queryTblSql, (branch, ))
        row = cursor.fetchone()
        while (None != row) :
            packageInfo = PackageInfo()
            package.branch = row[0]
            package.packageFullName = row[1]
            package.packageName = row[2]
            package.version = row[3]
            package.user = row[4]
            package.channel = row[5]
            result[package.packageFullName] = package
            row = cursor.fetchone()
        cursor.close()

    def queryEx(self, branch, result):
        '''查询指定分支下的所有包信息,返回的map key为package Name'''
        cursor = self.__conn.cursor()
        queryTblSql = '''
                              select cbranch, cid, cname, cversion, ctype, cchannel from t_conan_pkginfo where cbranch=?
                          '''
        cursor.execute(queryTblSql, (branch, ))
        row = cursor.fetchone()
        while (None != row) :
            package = PackageInfo()
            package.branch = row[0]
            package.packageFullName = row[1]
            package.packageName = row[2]
            package.version = row[3]
            package.user = row[4]
            package.channel = row[5]
            result[package.packageName] = package
            row = cursor.fetchone()
        cursor.close()

    def queryAll(self, result):
        '''查询所有包信息'''
        cursor = self.__conn.cursor()
        queryTblSql = '''
                               select cbranch, cid, cname, cversion, ctype, cchannel from t_conan_pkginfo 
                           '''
        cursor.execute(queryTblSql)
        row = cursor.fetchone()
        while (None != row):
            package = PackageInfo()
            package.branch = row[0]
            package.packageFullName = row[1]
            package.packageName = row[2]
            package.version = row[3]
            package.user = row[4]
            package.channel = row[5]
            row = cursor.fetchone()
            result.append(package)
        cursor.close()

    def __create_tbl(self):
        if (None == self.__conn) :
            return False
        cursor = self.__conn.cursor()
        createTblSql = '''
            create table t_conan_pkginfo (
                cbranch TEXT,
                cid TEXT,
                cname TEXT,
                cversion TEXT,
                ctype TEXT,
                cchannel TEXT,
                primary key(cbranch, cid))
        '''
        cursor.execute(createTblSql)
        self.__conn.commit()
        cursor.close()
        return True



if __name__ == "__main__" :
    db = DBSqlite3Serializer()
    db.open()
    packageList = []
    for i in range(1, 101) :
        package = PackageInfo()
        package.branch = "V4R2"
        package.user = "platform"
        package.channel = "test"
        package.packageName = "test"
        package.version = "1.0.%d" %i
        packageList.append(package)

    db.set(packageList)
    #db.commit()
    queryResult = {}
    db.query("V4R2", queryResult)
    print("1st Query V4R2 Count=%d" %(len(queryResult)))
    queryResult = {}
    db.query("V4R1", queryResult)
    print("2nd Query V4R1 Count=%d" %(len(queryResult)))
    queryAllResult = []
    db.queryAll(queryAllResult)
    print("3rd Query All V4R2 Count=%d" %(len(queryAllResult)))

    db.delete(packageList)
    queryAllResult = []
    db.queryAll(queryAllResult)
    print("After Delete V4R2 Count=%d" %(len(queryAllResult)))
    db.close()