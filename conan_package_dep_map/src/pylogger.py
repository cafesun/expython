#!/usr/bin/python
# -*- coding:utf8 -*-

import os, sys, argparse, re
import logging
import logging.handlers

LOG_FORMAT = "[%(asctime)s][%(levelname)s][%(process)d][%(thread)d]%(message)s"

def initLogger(logname, level = logging.DEBUG):
    '''初始化日志设置'''
    handleConsole = logging.StreamHandler(sys.stdout)

    fileName = "../log/%s.log" %(logname)
    handleFile = logging.FileHandler(filename=fileName)
    fomatter = logging.Formatter(LOG_FORMAT)
    handleConsole.setFormatter(fomatter)
    handleFile.setFormatter(fomatter)
    logger = logging.getLogger(logname)
    logger.addHandler(handleConsole)
    logger.addHandler(handleFile)
    logger.setLevel(level)

def getLogger() :
    return logging.getLogger("pkgscanner")
