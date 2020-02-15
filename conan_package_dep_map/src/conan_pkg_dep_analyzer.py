#!/usr/bin/python
# -*- coding:utf8 -*-

import argparse
from pylogger import getLogger
from pylogger import initLogger
from package_dot_analyser import ConanPkgDotAnalyzer
from db_sqlite_serializer import DBSqlite3Serializer
from package_csv_exporter import CSVExporter

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
    dbSerializer = None
    try :
        dbSerializer = DBSqlite3Serializer()
        dbSerializer.open()
        getLogger().info("open db")
        if (args.scanpath != "") :
            platformAnalyser = ConanPkgDotAnalyzer(args.scanpath, args.branch)
            getLogger().debug("Platform Pkg Analyser Begin !")
            platformAnalyser.analyse()
            getLogger().debug("Platform Pkg Analyser Complete!")
            pkgMap = platformAnalyser.getResult()
            dbSerializer.set(pkgMap.values())
        if (args.export != "none") :
            exporter = CSVExporter(dbSerializer)
            exporter.exportEx()
        dbSerializer.close()
        getLogger().info("close db normally!")
    except:
        dbSerializer.close()
        getLogger().info("close db on exception!")

if __name__ == "__main__" :
    # 初始化日志
    initLogger("pkgscanner")
    logger = getLogger()
    logger.debug("begin process")
    main()
    logger.debug("end process")