import requests

headers = {'content-type':'application/json'}
url="https://www.animalidentify.top:5000/record?name=1"   #IP和端口号，注意register后要加/

r = requests.get(url)
print(r.text)
