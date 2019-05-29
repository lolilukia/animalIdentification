import pymysql 
import database
import pandas as pd
import json,time,datetime

def timestamp_toString(stamp):
    return time.strftime('%Y--%m--%d',time.localtime(stamp))


results=database.search_recordBykind("1")
animals=[]
urls=[]
dates=[]


for item in results:
    animals.append(item[0])
    urls.append(item[1])
    dates.append(item[2])
data = pd.DataFrame(
        {"animal": animals,
         "url": urls,
         "date": dates})

data=list(data.groupby([data["date"].apply(lambda x:x.year),data["date"].apply(lambda x:x.month)],as_index=False))
length=len(data)
datas=data[0][1]
datas=datas.sort_values(["date"], ascending=False)
datas=datas.drop('date', 1)
json_data=datas.to_json(orient='columns')
json_data=json.loads(json_data)
date=str(data[0][0]).replace(', ','-')
date=date[1:len(date)-1]
json_data["date"]=date 
print(json_data)

