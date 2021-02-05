# -*- coding: utf-8 -*-

import requests
import urllib.request
import time
import json

accouut=["jumeng","jumeng2","jumeng3","jumeng4","jumeng5","jumeng6"]
for i in accouut:
    url = 'http://121.40.211.118:8080/login'
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
        'Connection': 'keep-alive',
        'Host': '121.40.211.118:8080',
        'Referer': 'http://121.40.211.118:8080/login'

    }
    params = {
        'account': i,
        'passwd': i
    }
    data = json.dumps(params)
    data = bytes(data, 'utf-8')
    request = urllib.request.Request(url=url, data=data, headers=headers, method='POST')
    response = urllib.request.urlopen(request)
    responselate = response.read().decode('utf-8')
    data = json.loads(responselate)
    token = data['token']
    url = 'http://121.40.211.118:8080/business/dataEntity/page'
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
        'Connection': 'keep-alive',
        'Host': '121.40.211.118:8080',
        'Referer': 'http://console.douring.com/',
        'X-Token': token,
        'Origin': 'http://console.douring.com'

    }
    params = {"pageNo": 1, "size": 100, "linkId": "", "channelId": "", "channelType": "", "searchTime": [],
              "orderBy": "date", "descOrAsc": "descending"}
    data = json.dumps(params)
    data = bytes(data, 'utf-8')
    request = urllib.request.Request(url=url, data=data, headers=headers, method='POST')
    response = urllib.request.urlopen(request)
    responselate = response.read().decode('utf-8')
    data = json.loads(responselate)
    data = data['page']['records']
    num = 0
    array = []
    for i in data:
        if (num < 5):
            num = num + 1
            date = i['date']+" 00:00:00"
            date = int(time.mktime(time.strptime(date, "%Y-%m-%d %H:%M:%S")))
            date=int(round(date * 1000))
            params = {'day': date, 'channelName': i['channelName'], 'uv': i['uv'], 'newusers': i['factNum']}
            array.append(params)
    url = "https://www.e-tui.net/ring/getZumaRingData.htm"
    #url = "http://192.168.60.27:8080/yitui.server/ring/getZumaRingData.htm"
    #url="http://192.168.20.2:60001/yitui-server/ring/getZumaRingData.htm"
    data = json.dumps(array)
    print(data)
    res = requests.post(url, data)
    print(res.text)
