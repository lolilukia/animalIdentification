import pymysql 
import database
import pandas as pd
import json,time,datetime

def timestamp_toString(stamp):
    return time.strftime('%Y--%m--%d',time.localtime(stamp))


results = database.search_recordBycount()
animals = []
urls = []
counts = []

for item in results:
    animals.append(item[0])
    urls.append(item[1])
    counts.append(item[2])
data = pd.DataFrame(
    {"animal": animals,
     "url": urls,
     "count": counts})

json_data = data.to_json(orient='table')
json_data = json.loads(json_data)
print(json_data)


