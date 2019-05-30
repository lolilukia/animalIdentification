import pymysql


db = pymysql.Connect("localhost", "root", "root", "mysql", charset='utf8' )
cursor = db.cursor()


cursor.execute("DROP TABLE IF EXISTS RECOGNITION")


sql = """CREATE TABLE RECOGNITION (
         USER_ID  CHAR(100) character set utf8 NOT NULL ,
         URL  CHAR(100) character set utf8,
         ANIMAL CHAR(20) character set utf8,  
         DATETIME DATE)"""

cursor.execute(sql)

cursor.execute("DROP TABLE IF EXISTS RECORD")

sql = """CREATE TABLE RECORD (
         ANIMAL  CHAR(100) character set utf8 NOT NULL,
         DES TEXT character set utf8,
         URL CHAR(100) character set utf8,
         NUM INT)"""

cursor.execute(sql)


db.close()