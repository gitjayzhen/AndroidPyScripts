# coding=utf-8
"""
封装的mysql部分函数
"""
import pymysql as MySQLdb


class DB:
    def __init__(self, DB_HOST, DB_PORT, DB_USER, DB_PWD, DB_NAME, DB_TABLE):
        self.__DB_HOST = DB_HOST
        self.__DB_PORT = DB_PORT
        self.__DB_USER = DB_USER
        self.__DB_PWD = DB_PWD
        self.__DB_NAME = DB_NAME
        self.__DB_TABLE = DB_TABLE
        self.__conn = self.__getConnection()

    def __getConnection(self):
        return MySQLdb.Connect(
                           host=self.__DB_HOST,  # 设置MYSQL地址
                           port=self.__DB_PORT,  # 设置端口号
                           user=self.__DB_USER,  # 设置用户名
                           passwd=self.__DB_PWD,  # 设置密码
                           db=self.__DB_NAME,  # 数据库名
                           charset='utf8'  # 设置编码
                           )

    def select(self, column_name, id_num):
        column_name = column_name
        id_num = id_num
        sql = str("SELECT "+column_name+" FROM "+self.__DB_TABLE+" WHERE id = "+id_num)
        cursor = self.__conn.cursor()
        cursor.execute(sql)
        returnData = cursor.fetchone()
        cursor.close()
        for i in returnData:
            return "%s" % i
        self.__conn.close()

    def update(self, sqlString):
        cursor = self.__conn.cursor()
        cursor.execute(sqlString)
        self.__conn.commit()
        cursor.close()
        self.__conn.close()

db_eles = DB('192.168.40.31', 3306, 'root', 'root', 'automation', 'elements')
db_riche = DB('192.168.40.31', 3306, 'root', 'root', 'automation', 'riches')
