#!/usr/bin/python
# -*- coding:utf8 -*-

import argparse
from pylogger import getLogger
from pylogger import initLogger
from package_dot_analyser import ConanPkgDotAnalyzer
from db_sqlite_serializer import DBSqlite3Serializer

def main() :

    getLogger().debug("parsing argument")
    parser = argparse.ArgumentParser()
    parser.add_argument("--scanpath", "-s", help="scan package path", type=str, default="", nargs="?")
    parser.add_argument("--branch", "-b", help="project branch", type=str, default="", nargs="?")
    parser.add_argument("--export", "-e", help="export[none|csv]", type=str, default="none", nargs="?")
    #    parser.add_argument("path", help="package root dir", type=str, default=".")
    args = parser.parse_args()
    getLogger().debug("scan path=%s branch=%s export=%s" %(args.scanpath, args.branch, args.export))
    #getLogger().debug("output path : %s" % (args.outputpath))

    if (args.scanpath != "") :
        platformAnalyser = ConanPkgDotAnalyzer(args.scanpath, args.branch)
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