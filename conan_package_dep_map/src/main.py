#!/usr/bin/python
# -*- coding:utf8 -*-

import argparse
import configparser
from pylogger import getLogger
from pylogger import initLogger
from package_dot_analyser import ConanPkgDotAnalyzer
from db_sqlite_serializer import DBSqlite3Serializer
from db_serializer_factory import DBSerializerFactory
from package_csv_exporter import CSVExporter

def main() :

    getLogger().debug("parsing argument")
    parser = argparse.ArgumentParser()
    parser.add_argument("--scanpath", "-s", help="scan package path", type=str, default="", nargs="?")
    parser.add_argument("--branch", "-b", help="project branch", type=str, default="", nargs="?")
    parser.add_argument("--export", "-e", help="export[none|csv]", type=str, default="none", nargs="?")
    parser.add_argument("--config", "-c", help="config file path", type=str, default="", nargs="?")
    #    parser.add_argument("path", help="package root dir", type=str, default=".")
    args = parser.parse_args()
    getLogger().debug("scan path=%s branch=%s export=%s" %(args.scanpath, args.branch, args.export))
    getLogger().debug("config path=%s" %args.config)

    configpath = ""
    if (args.config=="") :
        configpath = "../conf/config.ini"
    config = configparser.ConfigParser()
    config.read(configpath, encoding="utf-8")
    dbtype = config.get("config", "dbtype")
    #getLogger().debug("output path : %s" % (args.outputpath))
    dbParamters = dict(config.items(dbtype))
    dbSerializer = DBSerializerFactory.create(dbtype, dbParamters)
    if (None == dbSerializer) :
        getLogger().error("dbtype=%s can't support!" %dbtype)
        return False
    try :
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
    except BaseException as e:
        getLogger().error("run with exception : %s" %e.message)
        return False
    finally:
        getLogger().info("close db!")
        dbSerializer.close()
        return True

if __name__ == "__main__" :
    # 初始化日志
    initLogger("pkgscanner")
    logger = getLogger()
    logger.debug("begin process")
    bRet = main()
    if (bRet) :
        logger.info("end process normally!")
    else :
        logger.error("end process for something error!")