
from flask import Flask,request, redirect, url_for
from werkzeug.utils import secure_filename
from animal import AnimalRecognizer
import database
import pandas as pd
import json,time
import requests

app = Flask(__name__)

@app.route("/recognition",methods=['POST'])
def recognition():
    upload_files =request.files.getlist('file')
    basepath = '/root/user/photo/'
    user_id=request.form.get('name')

    #save img
    for file in upload_files:
        filename = secure_filename(file.filename)
        path=basepath+filename
        file.save(path)
    recognizer = AnimalRecognizer(api_key='IdirM2MKsCLKThwCvS581MFM', secret_key='PSI5UbINOzjNaAg5Ewb5VNlrkUS7FObG')
    animal=recognizer.detect(path)
    name=animal[0]['name']
    date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
    database.add_recogniction(user_id, path, name, date)
    print(json.dumps(animal,ensure_ascii=False))
    return json.dumps(animal,ensure_ascii=False)

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
        json_data = datas.to_json(orient='columns')
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
    json_data = data.to_json(orient='columns')
    json_data = json.loads(json_data)

    return json_data

@app.route("/home",methods=['GET'])
def home():
    user_id = request.args.get('name')

    results = database.search_recordBycount(user_id)
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

    json_data = data.to_json(orient='columns')
    json_data = json.loads(json_data)

    return json_data

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
