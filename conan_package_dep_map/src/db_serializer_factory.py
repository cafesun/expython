from db_mysql_serializer import DBMySqlSerializer
from db_sqlite_serializer import DBSqlite3Serializer


class DBSerializerFactory(object):
    '''数据库持久化工厂类'''

    def create(type, args):
        '''创建方法'''
        varInstance = None
        if (type == "MySQL"):
            host = args.get("host")
            host = "" if host == None else host.strip()
            user = args.get("user")
            user = "" if user == None else user.strip()
            passwd = args.get("password")
            passwd = "" if passwd == None else passwd.strip()
            varInstance = DBMySqlSerializer(host, user, passwd)
        elif (type == "SQLite") :
            dbpath = args.get("dbpath")
            dbpath = "" if dbpath == None else dbpath.strip()
            varInstance = DBSqlite3Serializer(dbpath)
        return varInstance