#!/usr/bin/python
# -*- coding:utf8 -*-

import argparse
from pylogger import getLogger
from pylogger import initLogger
from package_analyser import ConanPkgAnalyzer
from db_sqlite_serializer import DBSqlite3Serializer

def main() :

    getLogger().debug("parsing argument")
    parser = argparse.ArgumentParser()
    parser.add_argument("--scanpath", "-s", help="scan package path", type=str, default="", nargs="?")
    parser.add_argument("--type", "-t", help="conan package user type:[platform|msmp|core|ext|auto]",
                        type=str, default="auto", nargs="?")
    parser.add_argument("--export", "-e", help="export[none|csv]", type=str, default="none", nargs="?")
    #    parser.add_argument("path", help="package root dir", type=str, default=".")
    args = parser.parse_args()
    getLogger().debug("scan path : %s" %(args.scanpath))
    #getLogger().debug("output path : %s" % (args.outputpath))
    getLogger().debug("conan package usertype : %s" % (args.type))

    if (args.scanpath != "") :
        platformAnalyser = ConanPkgAnalyzer(args.scanpath, args.type)
        getLogger().debug("Platform Pkg Analyser begin anlalysing!")
        platformAnalyser.analyse()
        getLogger().debug("Platform Pkg Analyser begin anlalysing!")
        pkgMap = platformAnalyser.getResult()
        dbSerializer = DBSqlite3Serializer()
        dbSerializer.open()
        dbSerializer.set(pkgMap.values())
        dbSerializer.close()

    if (args.export != "none") :
        pass



if __name__ == "__main__" :
    # 初始化日志
    initLogger("pkgscanner")
    logger = getLogger()
    logger.debug("begin process")
    main()
    logger.debug("end process")