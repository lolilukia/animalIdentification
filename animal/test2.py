import pymysql 
import database
import pandas as pd
import json,time,datetime

def timestamp_toString(stamp):
    return time.strftime('%Y--%m--%d',time.localtime(stamp))


records=database.search_recordByanimal("猪")
print(len(records))
print(records)


