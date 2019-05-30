import pymysql

def get_connect():
    db = pymysql.Connect("localhost", "root", "root", "mysql", charset='utf8')
    return db

def close_connect(db):
    db.close()

def add_recogniction(user_id,url,name,time):
    db=get_connect()

    cursor = db.cursor()


    sql = "INSERT INTO RECOGNITION( USER_ID, URL, ANIMAL, DATETIME) VALUES ({},{},{},{});".\
        format(repr(user_id),repr(url),repr(name),repr(time))

    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)

    close_connect(db)

def add_record(name,des,url,count):
    db=get_connect()

    cursor = db.cursor()


    sql = "INSERT INTO RECORD( ANIMAL, DES,URL,NUM) VALUES ({},{},{},{});".\
        format(repr(name),repr(des),repr(url),count)
    print(sql)

    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)

    close_connect(db)

def search_count(user_id,name):
    db=get_connect()
    cursor = db.cursor()
    sql="SELECT COUNT(URL) FROM RECOGNITION WHERE USER_ID="+user_id+" AND ANIMAL="+name
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        return results
        db.commit()
    except:
        db.rollback()
    close_connect(db)

def search_recordBydate(user_id):
    db=get_connect()
    cursor = db.cursor()
    sql="SELECT ANIMAL,URL,DATETIME FROM RECOGNITION WHERE USER_ID="+repr(user_id)
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        return results
        db.commit()
    except:
        db.rollback()
    close_connect(db)

def search_recordBykind(user_id):
    db=get_connect()
    cursor = db.cursor()
    sql = "SELECT ANIMAL,URL,DATETIME FROM RECOGNITION WHERE URL IN " \
          "(SELECT MAX(URL) FROM RECOGNITION WHERE USER_ID = " + repr(user_id) + " GROUP BY ANIMAL)"

    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        return results
        db.commit()
    except:
        db.rollback()
    close_connect(db)

def search_recordBycount():
    db=get_connect()
    cursor = db.cursor()
    sql = "SELECT ANIMAL,URL,NUM FROM RECORD ORDER BY NUM DESC"

    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        return results
        db.commit()
    except:
        db.rollback()
    close_connect(db)

def search_recordByanimal(name):
    db=get_connect()
    cursor = db.cursor()
    sql = "SELECT NUM FROM RECORD WHERE ANIMAL="+repr(name)

    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        return results
        db.commit()
    except:
        db.rollback()
    close_connect(db)


def update_record(name,num):
    db=get_connect()
    cursor = db.cursor()
    sql = "UPDATE RECORD SET NUM ="+repr(num)+" WHERE ANIMAL="+repr(name)

    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        return results
        db.commit()
    except:
        db.rollback()
    close_connect(db)

def search_des(name):
    db=get_connect()
    cursor = db.cursor()
    sql = "SELECT DES FROM RECORD WHERE ANIMAL="+repr(name)

    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        return results
        db.commit()
    except:
        db.rollback()
    close_connect(db)