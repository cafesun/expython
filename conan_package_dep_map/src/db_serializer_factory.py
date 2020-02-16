from db_mysql_serializer import DBMySqlSerializer
from db_sqlite_serializer import DBSqlite3Serializer


class DBSerializerFactory(object):
    '''数据库持久化工厂类'''

    def create(type, args):
        '''创建方法'''
        varInstance = None
        if (type == "MySQL"):
            host = args.get("host")
            user = args.get("user")
            passwd = args.get("password")
            varInstance = DBMySqlSerializer(host, user, passwd)
        elif (type == "SQLite") :
            dbpath = args.get("dbpath")
            if (None == dbpath) :
                dbpath = ""
            varInstance = DBSqlite3Serializer(dbpath)
        return varInstance