#!/usr/bin/python
# -*- coding:utf8 -*-

from abc import ABC, abstractmethod

class DBSerializerIf(object):
    '''数据库抽象接口'''

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def set(self):
        pass

    @abstractmethod
    def set(self, pkgInfoList):
        pass

    @abstractmethod
    def delete(self, pkgInfoList):
        pass

    @abstractmethod
    def getAllPackageID(self, user=""):
        pass

    @abstractmethod
    def getAllPackageName(self, user=""):
        pass

    @abstractmethod
    def getBranches(self):
        pass

    @abstractmethod
    def query(self, branch, result):
        pass

    @abstractmethod
    def queryEx(self, branch, result, user=""):
        pass

    @abstractmethod
    def queryAll(self, result):
        pass