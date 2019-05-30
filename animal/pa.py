#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
from lxml import html
import xml
import requests
from bs4 import BeautifulSoup
import csv

count=0
def content(url):
    kv = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0"}
    r = requests.get(url, headers=kv, allow_redirects=False)

    #new_url = 'https://baike.baidu.com'+r.headers['Location']
    new_url='https://baike.baidu.com/item/%E9%95%BF%E9%A2%88%E9%B9%BF%E9%A9%AC%E8%B5%9B%E4%BA%9A%E7%A7%8D/14081503?fromtitle=%E9%A9%AC%E8%B5%9B%E9%95%BF%E9%A2%88%E9%B9%BF&fromid=6599990'
    print(new_url)
    res = requests.get(new_url,headers=kv, allow_redirects=True)
    print(res.headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, "html5lib")
    item=soup.find_all("description")
    print(item)



name="马赛长颈鹿"
url = 'https://baike.baidu.com/item/'+str(name)

content(url)
