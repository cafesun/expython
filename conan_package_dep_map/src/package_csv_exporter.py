#!/usr/bin/python
# -*- coding:utf8 -*-

import argparse
from pylogger import getLogger
from pylogger import initLogger
from package_analyser import ConanPkgAnalyzer
from db_sqlite_serializer import DBSqlite3Serializer


class CSVExporter(object):

    def __init__(self, db):
        self.__db = db

    def export(self):
        pass

