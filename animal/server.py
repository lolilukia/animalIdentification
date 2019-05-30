#!/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import Flask,request, redirect, url_for
from werkzeug.utils import secure_filename
from animal import AnimalRecognizer
import database
import pandas as pd
import json,time
import urllib.request
import requests,os,shutil
import re


app = Flask(__name__)

@app.route("/recognition",methods=['POST'])
def recognition():

    upload_files =request.files.getlist('file')
    basepath = 'static/photo/'
    web="https://www.animalidentify.top:5000/"
    user_id=request.form.get('name')

    #save img
    for file in upload_files:
        filename = secure_filename(file.filename)
        path=basepath+filename
        file.save(path)

    recognizer = AnimalRecognizer(api_key='IdirM2MKsCLKThwCvS581MFM', secret_key='PSI5UbINOzjNaAg5Ewb5VNlrkUS7FObG')
    animal=recognizer.detect(path)
    print(animal)
    name = animal[0]['name']
    if(name!="非动物"):
        baidupath = 'static/baidu/' + str(user_id)
        homepath='static/baike/'
        isExists = os.path.exists(baidupath)
        if isExists:
            shutil.rmtree(baidupath)
        os.makedirs(baidupath)

        for i in range(len(animal)):
            urlname=animal[i]['name']

            if (animal[i]["baike_info"].__contains__('image_url')):
                img_url = animal[i]["baike_info"]["image_url"]
                img = urllib.request.urlopen(img_url)
                img = img.read()
                with open(baidupath + '/' + urlname + '.jpg', 'wb') as f:
                    f.write(img)
            else:
                search_name = animal[i]['name']
                url = r'http://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&word=' \
                      + str(search_name)
                dirpath = baidupath+'/'
                html = requests.get(url).text
                urls = re.findall(r'"objURL":"(.*?)"', html)
                url = urls[0]
                try:
                    res = requests.get(url)
                    if str(res.status_code)[0] == "4":
                        print("sucess download from baidu：", url)
                        continue
                except Exception as e:
                    print("fail download from baidu：", url)
                filename = os.path.join(dirpath, urlname + ".jpg")
                img=res.content
                with open(filename, 'wb') as f:
                    f.write(img)

            if(i==0):
                with open(homepath + name + '.jpg', 'wb') as f:
                    f.write(img)

            animal[i]["baike_info"]["image_url"] = web + baidupath + '/' + urlname + '.jpg'

        des=animal[0]['baike_info']['description']
        date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
        database.add_recogniction(user_id, web+path, name, date)
        records=database.search_recordByanimal(name)
        if(len(records)==0):
            database.add_record(name,des,web + homepath + name + '.jpg',1)
        else:
            database.update_record(name,str(records[0][0]))

        json_data={"url":web+path,"list":animal,"result":"1"}
    else:
        json_data={"url":web+path,"list":animal,"result":"0"}
    return json.dumps(json_data,ensure_ascii=False)

@app.route("/detail",methods=['GET'])
def detail():
    name = request.args.get('name')
    result=database.search_des(name)
    des=result[0][0]
    json_data={"des":des}
    return json.dumps(json_data,ensure_ascii=False)

@app.route("/record",methods=['GET'])
def record():

    user_id=request.args.get('name')
    print(user_id)

    results = database.search_recordBydate(user_id)
    animals = []
    urls = []
    dates = []
    json_list=[]

    for item in results:
        animals.append(item[0])
        urls.append(item[1])
        dates.append(item[2])
    data = pd.DataFrame(
        {"animal": animals,
         "url": urls,
         "date": dates})

    data = list(
        data.groupby([data["date"].apply(lambda x: x.year), data["date"].apply(lambda x: x.month)], as_index=False))
    length = len(data)
    for i in range(length):
        datas = data[i][1]
        datas = datas.sort_values(["date"], ascending=False)
        datas = datas.reset_index()
        datas = datas.drop('date', 1)
        datas = datas.drop('index', 1)
        json_data = datas.to_json(orient='table')
        json_data = json.loads(json_data)
        date = str(data[0][0]).replace(', ', '-')
        date = date[1:len(date) - 1]
        json_data["date"] = date
        json_list.append(json_data)

    return json.dumps(json_list,ensure_ascii=False)

@app.route("/record_kind",methods=['GET'])
def record_kind():
    user_id = request.args.get('name')

    results = database.search_recordBykind(user_id)
    animals = []
    urls = []
    dates = []

    for item in results:
        animals.append(item[0])
        urls.append(item[1])
        dates.append(item[2])
    data = pd.DataFrame(
        {"animal": animals,
         "url": urls,
         "date": dates})

    data = data.sort_values(["date"], ascending=False)
    data = data.reset_index()
    data = data.drop('date', 1)
    data = data.drop('index', 1)
    json_data = data.to_json(orient='table')
    json_data = json.loads(json_data)
    print(json_data)

    return json.dumps(json_data['data'])

@app.route("/home",methods=['GET'])
def home():


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
    return json.dumps(json_data['data'])

@app.route("/session",methods=['GET'])
def session():
    appid = request.args.get('appid')
    secret = request.args.get('secret')
    code = request.args.get('code')
    url='https://api.weixin.qq.com/sns/jscode2session?appid=' + appid + '&secret=' + secret + '&js_code=' + code + '&grant_type=authorization_code'
    r = requests.get(url)
    return r.text



if __name__ == "__main__":
    context = ('p.crt', '1.key')
    app.run(host='0.0.0.0', threaded=True, ssl_context=context)
