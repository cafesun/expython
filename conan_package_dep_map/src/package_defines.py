#!/usr/bin/python
# -*- coding:utf8 -*-



class PackageInfo(object):
    ''' 包基本信息'''
    def __init__(self):
        self.branch = ""
        self.packageName = ""
        self.packageFullName = ""
        self.version =""
        self.channel = ""
        self.user = ""

    def getPakcageName(self):
        return self.packageName

    def getPackagePath(self):
        return self.packageFullName

    def getPkgID(self):
        pkgId = "%s/%s@%s/%s" % (self.packageName, self.version, self.user, self.channel)
        return pkgId

#    def __eq__(self, other):
#        return (self.packageName == other.getPackageName() and
#                self.moduleNames == other.getModuleNames() and
#                self.packagePath == other.getPackagePath())

#    def __lt__(self, other):
#        if (self.packageName != other.getPackageName()):
#            return self.packageName < other.getPackageName()
#        elif (self.moduleNames != other.getModuleNames()):
#            return self.moduleNames < other.getModuleNames()
#        elif (self.packagePath != other.getPackagePath()) :
#            return self.packagePath < other.getPackagePath()
#        else :
#            retur