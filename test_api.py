#coding: UTF-8

import requests
import json


def makeRequest(data, style):
    # proxies = {'https': 'http://127.0.0.1:8000'}
    url = "api.bibify.org"
    # url = "127.0.0.1:8000"
    citeObject = dict()
    citeObject["id"] = "testid"
    citeObject["style"] = style + ".csl"
    citeObject["language"] = "ru"
    citeObject.update(data)

    # data_json = json.dumps(citeObject, ensure_ascii=False,separators=(',', ':'))
    # data_json_dict = json.loads(data_json)
    # print(data_json_dict)
    # data_json=data_json.encode('UTF-8')
    # print(data_json)
    query = "https://" + url +"/api/cite?"
    # query = "https://" + url +"/api/cite?"
    # with open('json.json', 'w') as reader:
    #     reader.write(str(data_json))
    # Further file processing goes here

    # r = requests.get(query, verify=False, proxies=proxies)  
    # r = requests.get(query, data=data_json)  

    r = requests.get(url=query, params=citeObject)  
    print(r.text)

def makeAnotherRequest():
    url = "api.bibify.org"
    r = requests.get("https://api.bibify.org/api/styles?limit=20")  
    print(r.text)

def test():
    proxies = {
    'http': f'http://127.0.0.1:3000/',
    'https': f'http://127.0.0.1:3000/'
    }
    headers = {'Content-type': 'application/json'}
    url = "http://127.0.0.1:3000"
    r = requests.get(url=url, proxies=proxies)
    print(r.text)

citeObject = dict()
citeObject["type"] = "preprint"
citeObject["authors"] = list()
author = dict()
author["type"] = "Person"
author["first"] = "Vladimir"
author["last"] = "Kolodeznikov"
# author["given"] = "Владимир"
# author["family"] = "Колодезников"
citeObject["authors"].append(author)
citeObject["title"] = "Название статьи"
citeObject["year"] = 2020
citeObject["url"] = "https://google.com"
style = "gost-r-7-0-5-2008-numeric"
makeRequest(citeObject, style)
# makeAnotherRequest()
# test()