#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import re
import os

name="马赛长颈鹿"
url = r'http://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&word='+str(name)
dirpath = r'static/'

html = requests.get(url).text
urls = re.findall(r'"objURL":"(.*?)"', html)

if not os.path.isdir(dirpath):
    os.mkdir(dirpath)

index = 1
url=urls[0]
print("Downloading:", url)

try:
    res = requests.get(url)
    if str(res.status_code)[0] == "4":
        print("未下载成功：", url)
        continue
except Exception as e:
    print("未下载成功：", url)

filename = os.path.join(dirpath, str(index) + ".jpg")
with open(filename, 'wb') as f: f.write(res.content)
