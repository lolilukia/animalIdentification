import requests
import json
import base64
headers = {'content-type':'application/json'}
url="http://www.animalidentify.top:8888/recognition"   #IP和端口号，注意register后要加/
f = open("test1.jpg", 'rb')
img_str = base64.b64encode(f.read())

data = {
    'user_id':"11",
    'img':str(img_str)
}
print(len(img_str))
if isinstance(data, bytes):
    data=str(data, encoding='utf-8')
r = requests.post(url, data=json.dumps(data),headers=headers)
print(r.text)
