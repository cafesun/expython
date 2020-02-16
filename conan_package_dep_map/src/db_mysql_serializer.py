import mysql.connector

import os
from collections import OrderedDict
from pylogger import getLogger
from package_defines import PackageInfo
from db_serializer_if import DBSerializerIf

class DBMySqlSerializer(DBSerializerIf):
    def __init__(self, host, user, passwd):
        self.__host = host
        self.__user = user
        self.__passwd = passwd
        self.__conn = None
        self.__dbname = "conanpkgs_info"

    def __createDB(self):
        cursor = self.__conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS %s DEFAULT CHARSET utf8 COLLATE utf8_general_ci" %self.__dbname)
        cursor.close()

    def __checkDB(self):
        bDBExist = False
        self.__conn = mysql.connector.connect(host=self.__host, user=self.__user, passwd=self.__passwd)
        cursor = self.__conn.cursor(buffered=True)
        cursor.execute("SHOW DATABASES")
        row = cursor.fetchone()
        while (row != None):
            varDB = row[0]
            if (varDB == "conanpkgs_info"):
                bDBExist = True
                break
            else :
                row = cursor.fetchone()
        cursor.close()
        if (False == bDBExist):
            self.__createDB()
        self.__conn.close()
        self.__conn = mysql.connector.connect(host=self.__host, user=self.__user,
                                                 passwd=self.__passwd, database=self.__dbname)
        if (False == bDBExist):
            self.__create_tbl()

    def open(self):
        cursor = None
        try :
            self.__checkDB()
            return True
        except mysql.connector.Error as e:
            getLogger().error("Connect to DB Failed (%s)" %e.message)
        except :
            getLogger().error("Open DB Failed!")
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
                    replace into t_conan_pkginfo(cbranch, cid, cname, cversion, ctype, cchannel) values(
                    %s, %s, %s, %s, %s, %s)
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
                            delete from t_conan_pkginfo where cbranch=%s and cid=%s
                        '''
        for itData in pkgInfoList:
            pkgId = itData.getPkgID()
            bindVars = (itData.branch, pkgId)
            cursor.execute(deleteTblSql, bindVars)
        self.__conn.commit()
        cursor.close()

    def getAllPackageID(self, user=""):
        '''获取所有包的ID'''
        packageIDList = []
        cursor = self.__conn.cursor()
        if (user == ""):
            queryTblSql = '''select distinct(cid) from t_conan_pkginfo'''
            cursor.execute(queryTblSql)
        else:
            queryTblSql = '''select distinct(cid) from t_conan_pkginfo where ctype=%s'''
            cursor.execute(queryTblSql, (user, ))
        row = cursor.fetchone()
        while (None != row):
            packageID = row[0]
            packageIDList.append(packageID)
            row = cursor.fetchone()
        cursor.close()
        return set(packageIDList)

    def getAllPackageName(self, user=""):
        '''获取所有包的名称'''
        packageNameList = []
        cursor = self.__conn.cursor()
        if (user == "") :
            queryTblSql = '''select distinct(cname) from t_conan_pkginfo'''
            cursor.execute(queryTblSql)
        else :
            queryTblSql = '''select distinct(cname) from t_conan_pkginfo where ctype=%s'''
            cursor.execute(queryTblSql, (user,))
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
                              select cbranch, cid, cname, cversion, ctype, cchannel from t_conan_pkginfo where cbranch=%s
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

    def queryEx(self, branch, result, user=""):
        '''查询指定分支下的所有包信息,返回的map key为package Name'''
        cursor = self.__conn.cursor()
        queryTblSql = '''
                              select cbranch, cid, cname, cversion, ctype, cchannel from t_conan_pkginfo where cbranch=%s
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
          CREATE TABLE t_conan_pkginfo (
            cbranch VARCHAR(128),
            cid VARCHAR(512),
            cname VARCHAR(128) NOT NULL,
            cversion VARCHAR(128) NOT NULL,
            ctype VARCHAR(128) NOT NULL,
            cchannel VARCHAR(128) NOT NULL,
            PRIMARY KEY(cbranch, cid)) ENGINE=INNODB DEFAULT CHARSET=utf8
                '''
        cursor.execute(createTblSql)
        self.__conn.commit()
        cursor.close()
        return True



if __name__ == "__main__" :
    db = DBMySqlSerializer()
    db.open("127.0.0.1", "root", "vislecaina")
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